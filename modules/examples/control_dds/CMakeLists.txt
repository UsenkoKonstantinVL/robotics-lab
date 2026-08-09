find_package(CppTui REQUIRED)
find_package(CycloneDDS-CXX 11.0.1 REQUIRED)
find_package(Python3 3.11 REQUIRED COMPONENTS Interpreter)

idlcxx_generate(
  TARGET robotics_lab_control_dds_types
  FILES ControlCommand.idl
  WARNINGS no-implicit-extensibility
)

add_executable(robotics_lab_control_dds_tui
  cpp/control_tui.cpp
)
target_link_libraries(robotics_lab_control_dds_tui
  PRIVATE
    RoboticsLab::cyclonedds_engine
    cpp-tui::cpptui
    robotics_lab_control_dds_types
)
target_compile_features(robotics_lab_control_dds_tui PRIVATE cxx_std_20)

set(control_dds_python_types_dir "${CMAKE_CURRENT_BINARY_DIR}/python_types")
set(control_dds_python_package_dir
  "${control_dds_python_types_dir}/robotics_lab_control_dds"
)
set(control_dds_python_outputs
  "${control_dds_python_package_dir}/__init__.py"
  "${control_dds_python_package_dir}/_ControlCommand.py"
)

add_custom_command(
  OUTPUT ${control_dds_python_outputs}
  COMMAND "${CMAKE_COMMAND}" -E make_directory "${control_dds_python_types_dir}"
  COMMAND CycloneDDS::idlc -l py "${CMAKE_CURRENT_SOURCE_DIR}/ControlCommand.idl"
  DEPENDS ControlCommand.idl
  WORKING_DIRECTORY "${control_dds_python_types_dir}"
  COMMENT "Generating control DDS example Python types"
  VERBATIM
)

add_custom_target(robotics_lab_control_dds_python_types ALL
  DEPENDS ${control_dds_python_outputs}
)

add_custom_target(robotics_lab_control_dds_mujoco_viewer
  SOURCES python/mujoco_viewer.py
)

if(BUILD_TESTING)
  add_test(
    NAME examples.control_dds.mujoco_viewer
    COMMAND
      "${CMAKE_COMMAND}" -E env
      "PYTHONPATH=${control_dds_python_types_dir}"
      "${Python3_EXECUTABLE}" -m unittest discover
      -s "${CMAKE_CURRENT_SOURCE_DIR}/tests"
      -p "test_*.py"
  )
endif()
