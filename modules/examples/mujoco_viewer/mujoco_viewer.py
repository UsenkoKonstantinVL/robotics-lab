#!/usr/bin/env python3
"""Open a local MuJoCo model or scene in the interactive viewer."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Callable, Sequence


SUPPORTED_SUFFIXES = {".mjb", ".urdf", ".xml"}


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
        description="Open an MJCF model or scene in MuJoCo's Simulate GUI."
    )
    parser.add_argument(
        "path",
        type=model_path,
        help="path to an MJCF/URDF XML model, scene XML, or compiled MJB model",
    )
    return parser.parse_args(argv)


def launch(path: Path, launcher: Callable[[str], None] | None = None) -> None:
    if launcher is None:
        try:
            from mujoco import viewer
        except ImportError as error:
            raise RuntimeError(
                "MuJoCo's Python package is required; use the development container "
                "or install the pinned project dependency"
            ) from error
        launcher = viewer.launch_from_path

    launcher(str(path))


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    launch(args.path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
