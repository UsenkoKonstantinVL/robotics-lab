# Cyclone DDS engine

This meta module exposes the Cyclone DDS C and C++ libraries through the
`RoboticsLab::cyclonedds_engine` CMake target. It owns dependency discovery only;
framework communication APIs should not expose Cyclone DDS native types.

Cyclone DDS 11.0.1 is the minimum supported version and is pinned in the
development image together with its C++ and Python bindings.
