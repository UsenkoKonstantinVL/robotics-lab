# DDS control example

This example demonstrates an end-to-end manual control path over Cyclone DDS.
It owns all of its pieces:

- `ControlCommand.idl` defines a normalized floating-point command.
- `cpp/control_tui.cpp` publishes commands from an interactive terminal.
- `python/mujoco_viewer.py` subscribes and applies commands to a MuJoCo
  actuator.

The processes communicate on `robotics_lab.control.command`. The viewer drives
the actuator named `forward` by default, clamps commands to its control range,
and applies zero if no sample arrives for 500 ms.

Build the development image and project:

```bash
dev/dev.sh build
dev/dev.sh start
dev/dev.sh exec dev/scripts/check.sh
```

Start the viewer:

```bash
dev/dev.sh exec env \
  PYTHONPATH=build/dev/modules/examples/control_dds/python_types \
  python3 modules/examples/control_dds/python/mujoco_viewer.py \
  models/car/car.xml
```

In another terminal, start the controller:

```bash
dev/dev.sh exec \
  build/dev/modules/examples/control_dds/robotics_lab_control_dds_tui
```

Controller keys:

- Up publishes the selected positive maximum.
- Down publishes the selected negative maximum.
- Left and Right decrease or increase the maximum in steps of `0.1`.
- A publish cycle without a new Up or Down event sends zero.
- `q` exits and publishes a final zero command.

Use `--actuator NAME` or `--topic NAME` on the viewer to connect another model
actuator or DDS topic. The supplied model may be MJCF, URDF, a scene XML, or a
compiled MJB file.
