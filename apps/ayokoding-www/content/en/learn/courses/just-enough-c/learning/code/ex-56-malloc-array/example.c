// => this directive is part of the source interface
#include <stdio.h>
// => this directive is part of the source interface
#include <stdlib.h>
// => this line makes the program's state or output explicit
int main(void) {
  // => this line makes the program's state or output explicit
  int *values = malloc(3 * sizeof *values);
  // => this line makes the program's state or output explicit
  if (values == NULL)
    return 1;
  // => this line makes the program's state or output explicit
  values[0] = 1;
  values[1] = 2;
  values[2] = 3;
  // => this line makes the program's state or output explicit
  printf("sum=%d\n", values[0] + values[1] + values[2]);
  // => this line makes the program's state or output explicit
  free(values);
  // => this line makes the program's state or output explicit
  return 0;
  // => this line makes the program's state or output explicit
}
