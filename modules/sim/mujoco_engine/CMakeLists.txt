find_package(MuJoCo 3.11.0 REQUIRED)

add_library(robotics_lab_mujoco_engine INTERFACE)
add_library(RoboticsLab::mujoco_engine ALIAS robotics_lab_mujoco_engine)

target_link_libraries(robotics_lab_mujoco_engine
  INTERFACE
    MuJoCo::MuJoCo
)

if(BUILD_TESTING)
  add_executable(robotics_lab_mujoco_engine_tests
    tests/dependency_test.cpp
  )
  target_link_libraries(robotics_lab_mujoco_engine_tests
    PRIVATE
      RoboticsLab::mujoco_engine
  )
  add_test(
    NAME mujoco_engine.dependency
    COMMAND robotics_lab_mujoco_engine_tests
  )
endif()
