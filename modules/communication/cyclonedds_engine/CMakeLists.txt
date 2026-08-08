find_package(CycloneDDS 11.0.1 REQUIRED)
find_package(CycloneDDS-CXX 11.0.1 REQUIRED)

add_library(robotics_lab_cyclonedds_engine INTERFACE)
add_library(RoboticsLab::cyclonedds_engine ALIAS robotics_lab_cyclonedds_engine)

target_link_libraries(robotics_lab_cyclonedds_engine
  INTERFACE
    CycloneDDS::ddsc
    CycloneDDS-CXX::ddscxx
)

if(BUILD_TESTING)
  add_executable(robotics_lab_cyclonedds_engine_tests
    tests/dependency_test.cpp
  )
  target_link_libraries(robotics_lab_cyclonedds_engine_tests
    PRIVATE
      RoboticsLab::cyclonedds_engine
  )
  add_test(
    NAME cyclonedds_engine.dependency
    COMMAND robotics_lab_cyclonedds_engine_tests
  )
endif()
