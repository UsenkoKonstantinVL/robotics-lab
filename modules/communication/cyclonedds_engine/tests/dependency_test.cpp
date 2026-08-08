#include <dds/dds.h>
#include <dds/dds.hpp>

int main() {
  static_assert(sizeof(dds_entity_t) > 0);
  return 0;
}
