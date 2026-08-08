find_package(CppTui REQUIRED)

add_executable(robotics_lab_control_tui
  src/main.cpp
)
target_link_libraries(robotics_lab_control_tui
  PRIVATE
    RoboticsLab::cyclonedds_engine
    RoboticsLab::types
    cpp-tui::cpptui
)
target_compile_features(robotics_lab_control_tui PRIVATE cxx_std_20)
