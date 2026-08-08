cmake_minimum_required(VERSION 3.24)

project(
  RoboticsLab
  VERSION 0.1.0
  DESCRIPTION "An experimental robotics framework"
  LANGUAGES CXX
)

include(CTest)

set(CMAKE_CXX_EXTENSIONS OFF)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

add_subdirectory(modules)
