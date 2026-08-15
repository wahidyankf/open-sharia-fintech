// => this directive is part of the source interface
#include "item.h"
// => this line makes the program's state or output explicit
int total(const struct Item items[], size_t count) {
  int result = 0;
  for (size_t i = 0; i < count; ++i)
    result += items[i].quantity;
  return result;
}
