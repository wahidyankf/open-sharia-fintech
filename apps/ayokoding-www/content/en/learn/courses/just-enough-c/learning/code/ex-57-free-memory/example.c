// => this directive is part of the source interface
#include <stdio.h>
// => this directive is part of the source interface
#include <stdlib.h>
// => this line makes the program's state or output explicit
int main(void) {
  // => this line makes the program's state or output explicit
  int *value = malloc(sizeof *value);
  // => this line makes the program's state or output explicit
  if (value == NULL)
    return 1;
  // => this line makes the program's state or output explicit
  *value = 1;
  // => this line makes the program's state or output explicit
  free(value);
  // => this line makes the program's state or output explicit
  puts("released");
  // => this line makes the program's state or output explicit
  return 0;
  // => this line makes the program's state or output explicit
}
