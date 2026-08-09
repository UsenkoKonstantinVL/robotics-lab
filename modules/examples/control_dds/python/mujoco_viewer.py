#!/usr/bin/env python3
"""Run a MuJoCo model and apply control commands received through Cyclone DDS."""

from __future__ import annotations

import argparse
import time
from pathlib import Path
from typing import Callable, Sequence


SUPPORTED_SUFFIXES = {".mjb", ".urdf", ".xml"}
DEFAULT_TOPIC = "robotics_lab.control.command"
DEFAULT_ACTUATOR = "forward"
COMMAND_TIMEOUT_SECONDS = 0.5


def model_path(value: str) -> Path:
    """Resolve and validate a model or scene path supplied on the command line."""
    path = Path(value).expanduser().resolve()

    if not path.is_file():
        raise argparse.ArgumentTypeError(f"model or scene does not exist: {path}")
    if path.suffix.lower() not in SUPPORTED_SUFFIXES:
        supported = ", ".join(sorted(SUPPORTED_SUFFIXES))
        raise argparse.ArgumentTypeError(
            f"unsupported model format '{path.suffix}'; expected one of: {supported}"
        )

    return path


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run a MuJoCo model controlled through Cyclone DDS."
    )
    parser.add_argument(
        "path",
        type=model_path,
        help="path to an MJCF/URDF XML model, scene XML, or compiled MJB model",
    )
    parser.add_argument(
        "--actuator",
        default=DEFAULT_ACTUATOR,
        help=f"actuator driven by ControlCommand (default: {DEFAULT_ACTUATOR})",
    )
    parser.add_argument(
        "--topic",
        default=DEFAULT_TOPIC,
        help=f"DDS control topic (default: {DEFAULT_TOPIC})",
    )
    return parser.parse_args(argv)


def clamp_command(value: float, lower: float, upper: float) -> float:
    """Clamp a received command to an actuator's declared control range."""
    return min(max(value, lower), upper)


def run_simulation(path: Path, actuator_name: str, topic_name: str) -> None:
    try:
        import mujoco
        from mujoco import viewer
    except ImportError as error:
        raise RuntimeError(
            "MuJoCo's Python package is required; use the development container "
            "or install the pinned project dependency"
        ) from error

    try:
        from cyclonedds.domain import DomainParticipant
        from cyclonedds.sub import DataReader
        from cyclonedds.topic import Topic
        from robotics_lab_control_dds import ControlCommand
    except ImportError as error:
        raise RuntimeError(
            "Cyclone DDS and the generated robotics_lab_control_dds Python "
            "package are required; build the project and add its generated types "
            "to PYTHONPATH"
        ) from error

    if path.suffix.lower() == ".mjb":
        model = mujoco.MjModel.from_binary_path(str(path))
    else:
        model = mujoco.MjModel.from_xml_path(str(path))
    data = mujoco.MjData(model)

    actuator_id = mujoco.mj_name2id(
        model, mujoco.mjtObj.mjOBJ_ACTUATOR, actuator_name
    )
    if actuator_id < 0:
        raise ValueError(f"model has no actuator named '{actuator_name}'")

    control_range = model.actuator_ctrlrange[actuator_id]
    participant = DomainParticipant()
    topic = Topic(participant, topic_name, ControlCommand)
    reader = DataReader(participant, topic)

    command = 0.0
    last_command_time: float | None = None
    with viewer.launch_passive(model, data) as simulation_viewer:
        while simulation_viewer.is_running():
            step_started = time.monotonic()
            for sample in reader.take():
                command = float(sample.value)
                last_command_time = step_started

            if (
                last_command_time is None
                or step_started - last_command_time > COMMAND_TIMEOUT_SECONDS
            ):
                command = 0.0

            data.ctrl[actuator_id] = clamp_command(
                command, float(control_range[0]), float(control_range[1])
            )
            mujoco.mj_step(model, data)
            simulation_viewer.sync()

            remaining = model.opt.timestep - (time.monotonic() - step_started)
            if remaining > 0:
                time.sleep(remaining)


def launch(
    path: Path,
    actuator_name: str = DEFAULT_ACTUATOR,
    topic_name: str = DEFAULT_TOPIC,
    runner: Callable[[Path, str, str], None] | None = None,
) -> None:
    if runner is None:
        runner = run_simulation
    runner(path, actuator_name, topic_name)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    launch(args.path, args.actuator, args.topic)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
