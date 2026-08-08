add_library(robotics_lab_core
  src/version.cpp
)

add_library(RoboticsLab::core ALIAS robotics_lab_core)

target_compile_features(robotics_lab_core PUBLIC cxx_std_20)

target_include_directories(robotics_lab_core
  PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    $<INSTALL_INTERFACE:include>
)

if(BUILD_TESTING)
  add_executable(robotics_lab_core_tests
    tests/version_test.cpp
  )
  target_link_libraries(robotics_lab_core_tests PRIVATE RoboticsLab::core)
  add_test(NAME core.version COMMAND robotics_lab_core_tests)
endif()
