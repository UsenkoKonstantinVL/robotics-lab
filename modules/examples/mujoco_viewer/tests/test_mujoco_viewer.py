from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock


MODULE_DIRECTORY = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(MODULE_DIRECTORY))

import mujoco_viewer  # noqa: E402


class MujocoViewerTest(unittest.TestCase):
    def test_model_path_accepts_xml_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory, "scene.xml")
            path.touch()

            self.assertEqual(mujoco_viewer.model_path(str(path)), path.resolve())

    def test_model_path_rejects_missing_file(self) -> None:
        with self.assertRaisesRegex(
            mujoco_viewer.argparse.ArgumentTypeError, "does not exist"
        ):
            mujoco_viewer.model_path("missing.xml")

    def test_model_path_accepts_urdf_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory, "model.urdf")
            path.touch()

            self.assertEqual(mujoco_viewer.model_path(str(path)), path.resolve())

    def test_model_path_rejects_unsupported_format(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory, "model.txt")
            path.touch()

            with self.assertRaisesRegex(
                mujoco_viewer.argparse.ArgumentTypeError, "unsupported model format"
            ):
                mujoco_viewer.model_path(str(path))

    def test_launch_passes_configuration_to_runner(self) -> None:
        runner = Mock()
        path = Path("/tmp/scene.xml")

        mujoco_viewer.launch(path, "motor", "control.topic", runner)

        runner.assert_called_once_with(path, "motor", "control.topic")

    def test_clamp_command_uses_actuator_range(self) -> None:
        self.assertEqual(mujoco_viewer.clamp_command(2.0, -1.0, 1.0), 1.0)
        self.assertEqual(mujoco_viewer.clamp_command(-2.0, -1.0, 1.0), -1.0)
        self.assertEqual(mujoco_viewer.clamp_command(0.25, -1.0, 1.0), 0.25)


if __name__ == "__main__":
    unittest.main()
