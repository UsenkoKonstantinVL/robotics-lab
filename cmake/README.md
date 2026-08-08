# CMake support

Reusable CMake functions, platform configuration, and toolchain files belong
here. Module-specific build logic should remain in the module that uses it.

Avoid placing generated files or third-party source code in this directory.

`FindMuJoCo.cmake` discovers the native MuJoCo SDK installed in the development
image and exposes it as `MuJoCo::MuJoCo`.

`FindCppTui.cmake` discovers the cpp-tui single-header library and exposes it as
`cpp-tui::cpptui`.
