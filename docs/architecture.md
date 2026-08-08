# Initial architecture

Robotics Lab is a collection of independently testable modules rather than one
monolithic runtime. The architecture should eventually support different robot
forms, computers, sensors, actuators, and transports without making one of them
the default assumption.

## Intended boundaries

The following boundaries are directions, not implemented packages:

- **Core:** time, lifecycle, errors, configuration, and common value types.
- **Messaging:** typed data exchange inside a process and across processes.
- **Hardware:** interfaces and adapters for sensors, actuators, and buses.
- **Control:** reusable controllers and real-time-safe execution primitives.
- **Models:** robot geometry, kinematics, and dynamics.
- **Simulation:** deterministic test doubles and simulator adapters.
- **Tools:** inspection, recording, replay, diagnostics, and visualization.

New modules should be introduced only when an experiment needs one of these
boundaries. Hardware adapters depend on stable abstractions; core abstractions
must not depend on particular hardware.

## Language strategy

C++ is intended for deterministic, performance-sensitive, and hardware-facing
code. Python is intended for experiments, orchestration, analysis, and tooling.
Bindings should be explicit module APIs, not access to internal C++ details.

## Early design principles

1. Make time and scheduling explicit.
2. Separate algorithms from I/O.
3. Make components runnable in tests without hardware.
4. Prefer typed, versionable messages at module boundaries.
5. Measure latency and resource use before optimizing.
