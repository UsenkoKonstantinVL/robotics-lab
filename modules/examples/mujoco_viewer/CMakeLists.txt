find_package(Python3 3.11 REQUIRED COMPONENTS Interpreter)

add_custom_target(robotics_lab_mujoco_viewer
  SOURCES
    mujoco_viewer.py
)

if(BUILD_TESTING)
  add_test(
    NAME examples.mujoco_viewer
    COMMAND
      "${Python3_EXECUTABLE}" -m unittest discover
      -s "${CMAKE_CURRENT_SOURCE_DIR}/tests"
      -p "test_*.py"
  )
endif()
