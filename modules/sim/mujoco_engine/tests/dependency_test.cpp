#include <mujoco/mujoco.h>

#include <iostream>

int main() {
  const int runtime_version = mj_version();
  if (runtime_version != mjVERSION_HEADER) {
    std::cerr << "MuJoCo header/runtime version mismatch: header="
              << mjVERSION_HEADER << ", runtime=" << runtime_version << '\n';
    return 1;
  }

  return 0;
}
