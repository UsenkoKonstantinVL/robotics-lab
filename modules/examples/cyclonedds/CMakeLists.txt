find_package(CycloneDDS-CXX 11.0.1 REQUIRED)
find_package(Python3 3.11 REQUIRED COMPONENTS Interpreter)

idlcxx_generate(
  TARGET robotics_lab_cyclonedds_example_types
  FILES HelloMessage.idl
  WARNINGS no-implicit-extensibility
)

add_executable(robotics_lab_cyclonedds_cpp_publisher
  cpp/publisher.cpp
)
target_link_libraries(robotics_lab_cyclonedds_cpp_publisher
  PRIVATE
    RoboticsLab::cyclonedds_engine
    robotics_lab_cyclonedds_example_types
)
target_compile_features(robotics_lab_cyclonedds_cpp_publisher PRIVATE cxx_std_20)

add_executable(robotics_lab_cyclonedds_cpp_subscriber
  cpp/subscriber.cpp
)
target_link_libraries(robotics_lab_cyclonedds_cpp_subscriber
  PRIVATE
    RoboticsLab::cyclonedds_engine
    robotics_lab_cyclonedds_example_types
)
target_compile_features(robotics_lab_cyclonedds_cpp_subscriber PRIVATE cxx_std_20)

set(cyclonedds_python_output_dir "${CMAKE_CURRENT_BINARY_DIR}/python")
set(cyclonedds_python_package_dir
  "${cyclonedds_python_output_dir}/robotics_lab_examples"
)
set(cyclonedds_python_outputs
  "${cyclonedds_python_package_dir}/__init__.py"
  "${cyclonedds_python_package_dir}/_HelloMessage.py"
)

add_custom_command(
  OUTPUT ${cyclonedds_python_outputs}
  COMMAND
    "${CMAKE_COMMAND}" -E make_directory "${cyclonedds_python_output_dir}"
  COMMAND
    CycloneDDS::idlc -l py
    "${CMAKE_CURRENT_SOURCE_DIR}/HelloMessage.idl"
  DEPENDS HelloMessage.idl
  WORKING_DIRECTORY "${cyclonedds_python_output_dir}"
  COMMENT "Generating Cyclone DDS Python types"
  VERBATIM
)

add_custom_target(robotics_lab_cyclonedds_python_types ALL
  DEPENDS ${cyclonedds_python_outputs}
)

if(BUILD_TESTING)
  add_test(
    NAME examples.cyclonedds.python_publisher_cli
    COMMAND
      "${CMAKE_COMMAND}" -E env
      "PYTHONPATH=${cyclonedds_python_output_dir}"
      "${Python3_EXECUTABLE}"
      "${CMAKE_CURRENT_SOURCE_DIR}/python/publisher.py"
      --help
  )
  add_test(
    NAME examples.cyclonedds.python_subscriber_cli
    COMMAND
      "${CMAKE_COMMAND}" -E env
      "PYTHONPATH=${cyclonedds_python_output_dir}"
      "${Python3_EXECUTABLE}"
      "${CMAKE_CURRENT_SOURCE_DIR}/python/subscriber.py"
      --help
  )
endif()
