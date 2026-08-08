# Shared types

This module contains provider-neutral wire schemas shared by applications and
robotics modules. IDL is the source of truth; the build generates matching C++
and Python types with Cyclone DDS.

`ControlCommand` contains one normalized floating-point value. A value of `1`
requests maximum forward actuation, `-1` requests maximum reverse actuation,
and `0` requests a stop.
