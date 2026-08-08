# Working instructions

## Project intent

Robotics Lab is an experimental robotics framework. Do not introduce ROS or a
large framework dependency unless an accepted design decision explicitly calls
for it. Prefer small, replaceable components and standard protocols.

## Change guidelines

- Organize modules by robotics capability, not by implementation language.
- Keep public C++ headers under a module's `include/robotics_lab/<module>/`.
- Keep implementation details under the module's `src/` directory.
- Place module tests next to their module in `tests/`.
- Document architectural decisions in `docs/decisions/`.
- Avoid global mutable state and hidden hardware access.
- Design hardware-facing code behind interfaces so it can be tested without a
  physical robot.
- Add dependencies only for a demonstrated requirement.

## Before finishing a change

Configure, build, and run tests with the checked-in CMake presets. Update the
relevant documentation when behavior or architecture changes.
