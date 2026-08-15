// => portable include guards prevent this declaration from appearing twice
#ifndef ITEM_H
// => define the guard name for subsequent includes
#define ITEM_H
// => size_t names a count of array elements
#include <stddef.h>
// => this record shares each inventory item's data between source files
struct Item {
  const char *name;
  int quantity;
};
// => this declaration lets main call the definition in inventory.c
int inventory_total(const struct Item items[], size_t count);
// => closes the portable include guard
#endif
