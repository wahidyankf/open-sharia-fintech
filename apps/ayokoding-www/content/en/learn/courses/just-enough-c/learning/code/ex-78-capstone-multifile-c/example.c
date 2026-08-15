// => this directive is part of the source interface
#include <stdio.h>
// => this directive is part of the source interface
#include "item.h"
// => this line makes the program's state or output explicit
int main(void) {
  // => this line makes the program's state or output explicit
  const struct Item items[] = {{"a", 3}, {"b", 4}};
  // => this line makes the program's state or output explicit
  printf("items=2 total=%d\n", total(items, 2));
  // => this line makes the program's state or output explicit
  return 0;
  // => this line makes the program's state or output explicit
}
