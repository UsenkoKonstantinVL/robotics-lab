# Development environment

This directory contains the shared development image and small workflow
scripts. It should describe a reproducible toolchain, not hold source code or
machine-specific editor settings.

The image includes the pinned MuJoCo native SDK and matching Python bindings.
It supports Docker's `linux/amd64` and `linux/arm64` platforms.

Use Docker Compose from the repository root:

```bash
docker compose -f dev/compose.yaml build
docker compose -f dev/compose.yaml run --rm lab
```

Inside the container, run `dev/scripts/check.sh` to configure, build, and test.

MuJoCo is installed at `/opt/mujoco`, exposed through `MUJOCO_HOME`, and its
tools are available on `PATH`. Python uses the image-managed virtual environment
at `/opt/robotics-lab/venv`.
