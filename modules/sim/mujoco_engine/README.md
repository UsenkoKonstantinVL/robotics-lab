# MuJoCo engine meta module

This interface-only module exposes the native MuJoCo C SDK to other C++ modules.
Consumers link `RoboticsLab::mujoco_engine` and receive the MuJoCo public include
directory and shared library transitively.

Keep simulation behavior and MuJoCo-specific wrappers in separate implementation
modules. This module owns dependency discovery only.
