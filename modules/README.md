# Modules

Each directory here represents one cohesive framework capability. Modules own
their public API, implementation, tests, and focused documentation.

The initial `core` module is deliberately tiny. It proves that the C++ build,
include layout, and test pipeline work without prematurely defining the full
framework.

Simulation integrations live under `sim/`. Engine meta modules expose external
SDKs to implementation modules without leaking dependency-discovery logic.

Runnable demonstrations live under `examples/`. They show focused workflows
without becoming part of the framework's public API.
