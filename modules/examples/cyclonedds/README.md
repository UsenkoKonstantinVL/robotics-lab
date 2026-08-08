# Cyclone DDS examples

These examples exchange `HelloMessage` samples on the
`robotics_lab.examples.hello` topic. [`HelloMessage.idl`](HelloMessage.idl) is
the source of truth for both languages: CMake generates C++ and Python types
during the build.

Build and start the development container from the repository root:

```bash
dev/dev.sh build
dev/dev.sh start
dev/dev.sh exec dev/scripts/check.sh
```

Start a subscriber in one terminal and a publisher in another. Each program
accepts an optional message count and defaults to five.

## C++ to C++

```bash
dev/dev.sh exec \
  build/dev/modules/examples/cyclonedds/robotics_lab_cyclonedds_cpp_subscriber

dev/dev.sh exec \
  build/dev/modules/examples/cyclonedds/robotics_lab_cyclonedds_cpp_publisher
```

## Python to Python

The generated Python package must be on `PYTHONPATH`:

```bash
dev/dev.sh exec env \
  PYTHONPATH=build/dev/modules/examples/cyclonedds/python \
  python3 modules/examples/cyclonedds/python/subscriber.py

dev/dev.sh exec env \
  PYTHONPATH=build/dev/modules/examples/cyclonedds/python \
  python3 modules/examples/cyclonedds/python/publisher.py
```

The publishers and subscribers are wire-compatible across languages. For
example, run the Python subscriber command followed by the C++ publisher
command, or the C++ subscriber followed by the Python publisher.

All examples use the default DDS domain. Set `CYCLONEDDS_URI` when a specific
network interface, domain, peer list, or other Cyclone DDS configuration is
required.
