# MuJoCo viewer example

This example opens a local model or scene in MuJoCo's interactive Simulate GUI.
The supplied file may be an MJCF or URDF XML file, a scene XML that includes
other models, or a compiled MJB model. Relative asset paths are resolved by
MuJoCo relative to the loaded XML file.

From the repository root, run:

```bash
python3 modules/examples/mujoco_viewer/mujoco_viewer.py models/car/car.xml
```

The development image provides the pinned `mujoco` Python package. A local
environment must provide the same package independently. The process blocks
until the viewer window is closed.

The argument is a local filesystem path. Downloading models from the network is
intentionally outside this example so model provenance, licensing, and asset
sets remain explicit.
