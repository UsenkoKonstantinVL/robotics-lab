# MuJoCo viewer example

This example runs a local model or scene in MuJoCo's passive viewer and applies
`ControlCommand` samples received on `robotics_lab.control.command`. By default,
the command drives the actuator named `forward`. Incoming values are clamped to
that actuator's control range, and the actuator is set to zero if no sample
arrives for 500 ms.

Build the development image and project, then start the viewer:

```bash
dev/dev.sh build
dev/dev.sh start
dev/dev.sh exec dev/scripts/check.sh
dev/dev.sh exec env \
  PYTHONPATH=build/dev/modules/types/python \
  python3 modules/examples/mujoco_viewer/mujoco_viewer.py models/car/car.xml
```

In another terminal, launch the controller:

```bash
dev/dev.sh exec build/dev/modules/control/control_tui/robotics_lab_control_tui
```

Use `--actuator NAME` or `--topic NAME` to connect a different model actuator
or DDS topic. The supplied file may be MJCF, URDF, a scene XML, or a compiled
MJB model. Relative assets are resolved by MuJoCo relative to the loaded file.
