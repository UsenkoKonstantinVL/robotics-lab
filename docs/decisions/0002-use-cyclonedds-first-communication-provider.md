# 0002: Use Cyclone DDS as the first communication provider

- Status: accepted
- Date: 2026-08-08

## Context

Independent robotics nodes need typed publish/subscribe communication across
process and machine boundaries. Both C++ and Python must be first-class node
languages. The framework should own its public node API and remain able to
support other communication providers in the future.

Cyclone DDS, Fast DDS, and RTI Connext DDS were considered. Cyclone DDS offers
a compact native core, official C++ and Python bindings, standard IDL code
generation, and an open implementation suitable for local experiments.

## Decision

Use Cyclone DDS 11.0.1 as the first communication provider. Define shared wire
types in IDL and generate language-specific representations. Keep Cyclone DDS
entities and QoS objects inside its adapter; future framework-facing node,
publisher, and subscriber APIs must use provider-independent types.

Pin the native C library, C++ binding, Python binding, and IDL compiler to the
same version in the development image.

## Consequences

- C++ and Python nodes can communicate directly through DDS/RTPS.
- IDL becomes the source of truth for cross-language message schemas.
- DDS discovery and QoS provide a capable transport foundation without ROS.
- Provider-specific types must not leak into control, hardware, or simulation
  APIs.
- Supporting another provider requires a new adapter and compatible schema
  mapping rather than changes to node implementations.
- Shared memory, security, discovery configuration, and schema evolution need
  separate experiments before becoming framework guarantees.
