# Development environment

This directory contains the shared development image and small workflow
scripts. It should describe a reproducible toolchain, not hold source code or
machine-specific editor settings.

The image includes the pinned MuJoCo native SDK and matching Python bindings.
It supports Docker's `linux/amd64` and `linux/arm64` platforms.

Use the development helper from the repository root:

```bash
dev/dev.sh build
dev/dev.sh start
dev/dev.sh exec
```

`build` creates the development image, `start` starts the `lab` service in the
background, and `exec` opens Bash in the running container. Pass arguments to
`exec` to run a specific command, for example
`dev/dev.sh exec dev/scripts/check.sh`.

Inside the container, run `dev/scripts/check.sh` to configure, build, and test.

On a Linux desktop using X11 or XWayland, Compose forwards `DISPLAY`, the X11
socket, and the current `XAUTHORITY` file so GUI tools such as the MuJoCo viewer
can open windows on the host. For example:

```bash
dev/dev.sh exec \
  python3 modules/examples/mujoco_viewer/mujoco_viewer.py models/car/car.xml
```

MuJoCo is installed at `/opt/mujoco`, exposed through `MUJOCO_HOME`, and its
tools are available on `PATH`. Python uses the image-managed virtual environment
at `/opt/robotics-lab/venv`.
