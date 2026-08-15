// => printf is declared by this standard header
#include <stdio.h>
// => import the shared struct and function declaration
#include "item.h"
// => main owns a fixed array and reports a normal process exit
int main(void) {
  // => two structs live in this translation unit; no heap ownership exists
  const struct Item items[] = {{"kernel", 3}, {"tools", 4}};
  // => compute the element count instead of hard-coding it
  size_t count = sizeof items / sizeof items[0];
  // => pass the array and its count to the other translation unit
  printf("items=%zu total=%d\n", count, inventory_total(items, count));
  // => zero reports successful completion
  return 0;
}
