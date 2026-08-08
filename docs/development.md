# Development

## Local build

Required tools:

- CMake 3.24 or newer
- Ninja
- A compiler with C++20 support
- MuJoCo 3.11 or newer, with `MUJOCO_HOME` set when installed outside a standard
  system prefix
- Python 3.11 or newer for scripts and future Python modules

Run:

```bash
cmake --preset dev
cmake --build --preset dev
ctest --preset dev
```

Build output is written to `build/dev/`.

## Development container

Build and enter the development image with Docker Compose:

```bash
docker compose -f dev/compose.yaml build
docker compose -f dev/compose.yaml run --rm lab
```

The repository is mounted at `/workspace/robotics-lab`. Build output remains in
the repository's ignored `build/` directory.

The image includes MuJoCo 3.11.0 in two forms:

- The native SDK is installed at `/opt/mujoco`. `MUJOCO_HOME`, `PATH`, and
  `LD_LIBRARY_PATH` are configured for its headers, tools, and shared library.
- The matching `mujoco` Python package is installed in the image-managed virtual
  environment at `/opt/robotics-lab/venv`, which is active through `PATH`.

The Dockerfile verifies the downloaded native archive against a pinned SHA-256
checksum and performs a Python model-loading smoke test during the image build.

## Adding a module

Create `modules/<name>/` with its own `CMakeLists.txt`, `README.md`, sources,
public headers, and tests as applicable. Register it in `modules/CMakeLists.txt`.
Do not add a new module solely to create a namespace or directory layer.
