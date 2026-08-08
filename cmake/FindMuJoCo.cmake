#[=======================================================================[.rst:
FindMuJoCo
----------

Find the native MuJoCo C SDK.

Imported Targets
^^^^^^^^^^^^^^^^

``MuJoCo::MuJoCo``
  The MuJoCo shared library and its public include directory.

Result Variables
^^^^^^^^^^^^^^^^

``MuJoCo_FOUND``
  True when both the library and public headers are available.
``MuJoCo_INCLUDE_DIR``
  Directory containing ``mujoco/mujoco.h``.
``MuJoCo_LIBRARY``
  Path to the MuJoCo shared library.
``MuJoCo_VERSION``
  Version read from the public MuJoCo header.

Set ``MUJOCO_HOME`` to provide an installation hint.
#]=======================================================================]

find_path(MuJoCo_INCLUDE_DIR
  NAMES mujoco/mujoco.h
  HINTS "$ENV{MUJOCO_HOME}"
  PATH_SUFFIXES include
)

find_library(MuJoCo_LIBRARY
  NAMES mujoco
  HINTS "$ENV{MUJOCO_HOME}"
  PATH_SUFFIXES lib bin
)

if(MuJoCo_INCLUDE_DIR)
  file(STRINGS "${MuJoCo_INCLUDE_DIR}/mujoco/mujoco.h"
    _MuJoCo_VERSION_LINE
    REGEX "^#define mjVERSION_HEADER [0-9]+$"
  )
  string(REGEX REPLACE ".* ([0-9]+)$" "\\1"
    _MuJoCo_VERSION_NUMBER
    "${_MuJoCo_VERSION_LINE}"
  )

  if(_MuJoCo_VERSION_NUMBER MATCHES "^[0-9]+$")
    math(EXPR _MuJoCo_VERSION_MAJOR "${_MuJoCo_VERSION_NUMBER} / 1000000")
    math(EXPR _MuJoCo_VERSION_MINOR
      "(${_MuJoCo_VERSION_NUMBER} % 1000000) / 1000"
    )
    math(EXPR _MuJoCo_VERSION_PATCH "${_MuJoCo_VERSION_NUMBER} % 1000")
    set(MuJoCo_VERSION
      "${_MuJoCo_VERSION_MAJOR}.${_MuJoCo_VERSION_MINOR}.${_MuJoCo_VERSION_PATCH}"
    )
  endif()
endif()

include(FindPackageHandleStandardArgs)
find_package_handle_standard_args(MuJoCo
  REQUIRED_VARS
    MuJoCo_INCLUDE_DIR
    MuJoCo_LIBRARY
  VERSION_VAR MuJoCo_VERSION
)

if(MuJoCo_FOUND AND NOT TARGET MuJoCo::MuJoCo)
  add_library(MuJoCo::MuJoCo UNKNOWN IMPORTED)
  set_target_properties(MuJoCo::MuJoCo PROPERTIES
    IMPORTED_LOCATION "${MuJoCo_LIBRARY}"
    INTERFACE_INCLUDE_DIRECTORIES "${MuJoCo_INCLUDE_DIR}"
  )
endif()

mark_as_advanced(
  MuJoCo_INCLUDE_DIR
  MuJoCo_LIBRARY
)
