find_package(CycloneDDS-CXX 11.0.1 REQUIRED)

idlcxx_generate(
  TARGET robotics_lab_types
  FILES ControlCommand.idl
  WARNINGS no-implicit-extensibility
)

add_library(RoboticsLab::types ALIAS robotics_lab_types)

set(robotics_lab_python_types_dir "${CMAKE_CURRENT_BINARY_DIR}/python")
set(robotics_lab_python_types_package_dir
  "${robotics_lab_python_types_dir}/robotics_lab_types"
)
set(robotics_lab_python_types_outputs
  "${robotics_lab_python_types_package_dir}/__init__.py"
  "${robotics_lab_python_types_package_dir}/_ControlCommand.py"
)

add_custom_command(
  OUTPUT ${robotics_lab_python_types_outputs}
  COMMAND "${CMAKE_COMMAND}" -E make_directory "${robotics_lab_python_types_dir}"
  COMMAND CycloneDDS::idlc -l py "${CMAKE_CURRENT_SOURCE_DIR}/ControlCommand.idl"
  DEPENDS ControlCommand.idl
  WORKING_DIRECTORY "${robotics_lab_python_types_dir}"
  COMMENT "Generating shared Cyclone DDS Python types"
  VERBATIM
)

add_custom_target(robotics_lab_python_types ALL
  DEPENDS ${robotics_lab_python_types_outputs}
)

set(ROBOTICS_LAB_PYTHON_TYPES_DIR
  "${robotics_lab_python_types_dir}"
  PARENT_SCOPE
)
