// => this directive is part of the source interface
#ifndef ITEM_H
// => this directive is part of the source interface
#define ITEM_H
// => this directive is part of the source interface
#include <stddef.h>
// => this line makes the program's state or output explicit
struct Item {
  const char *name;
  int quantity;
};
// => this line makes the program's state or output explicit
int total(const struct Item items[], size_t count);
// => this directive is part of the source interface
#endif
