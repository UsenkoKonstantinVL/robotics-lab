find_path(
  CppTui_INCLUDE_DIR
  NAMES cpptui.hpp
  HINTS ENV CPP_TUI_HOME
  PATH_SUFFIXES include
)

include(FindPackageHandleStandardArgs)
find_package_handle_standard_args(CppTui REQUIRED_VARS CppTui_INCLUDE_DIR)

if(CppTui_FOUND AND NOT TARGET cpp-tui::cpptui)
  add_library(cpp-tui::cpptui INTERFACE IMPORTED)
  set_target_properties(cpp-tui::cpptui PROPERTIES
    INTERFACE_INCLUDE_DIRECTORIES "${CppTui_INCLUDE_DIR}"
  )
endif()

mark_as_advanced(CppTui_INCLUDE_DIR)
