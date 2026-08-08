# 0001: Use MuJoCo as the first simulation engine

- Status: accepted
- Date: 2026-08-08

## Context

The first experiment requires simulation and control nodes for a mobile
platform. The engine must support C++ and Python development, headless
execution, and parallel environments for reinforcement learning. The framework
is expected to support other simulation engines in the future.

## Decision

Use MuJoCo as the simulation engine for the first implementation. Keep MuJoCo
types and lifecycle management inside a MuJoCo adapter; framework-facing control
and simulation interfaces must use engine-independent types.

Pin the development image's native SDK and Python bindings to the same MuJoCo
version.

## Consequences

- The first simulator can use MuJoCo's compact native API and Python bindings.
- Parallel learning environments can use independent simulation state without
  defining that execution model as a framework requirement.
- Engine-specific model files and implementation details remain isolated from
  control nodes.
- Adding another engine requires a new adapter and model representation, not a
  rewrite of control components.
- Mobile-platform contact and wheel behavior must be validated against physical
  measurements before relying on simulation fidelity.
