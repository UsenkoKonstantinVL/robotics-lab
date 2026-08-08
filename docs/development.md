# Development

## Local build

Required tools:

- CMake 3.24 or newer
- Ninja
- A compiler with C++20 support
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

## Adding a module

Create `modules/<name>/` with its own `CMakeLists.txt`, `README.md`, sources,
public headers, and tests as applicable. Register it in `modules/CMakeLists.txt`.
Do not add a new module solely to create a namespace or directory layer.
