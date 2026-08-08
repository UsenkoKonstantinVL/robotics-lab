#include "robotics_lab/core/version.hpp"

#include <iostream>

int main() {
  const auto version = robotics_lab::core::version();
  if (version.empty()) {
    std::cerr << "Project version must not be empty\n";
    return 1;
  }
  return 0;
}
