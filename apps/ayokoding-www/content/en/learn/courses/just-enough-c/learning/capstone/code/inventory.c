// => import the declaration shared by this translation unit
#include "item.h"
// => sum quantities without taking ownership of the caller's fixed array
int inventory_total(const struct Item items[], size_t count) {
  // => total starts as the additive identity
  int total = 0;
  // => each index stays inside the array's supplied count
  for (size_t index = 0; index < count; ++index) {
    // => access the current struct through the array
    total += items[index].quantity;
  }
  // => return the computed summary to main
  return total;
}
