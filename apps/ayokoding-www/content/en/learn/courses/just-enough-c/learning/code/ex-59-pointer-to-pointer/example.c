// => this directive is part of the source interface
#include <stdio.h>
// => this line makes the program's state or output explicit
int main(void) {
  // => this line makes the program's state or output explicit
  int value = 4;
  // => this line makes the program's state or output explicit
  int *pointer = &value;
  // => this line makes the program's state or output explicit
  int **double_pointer = &pointer;
  // => this line makes the program's state or output explicit
  printf("value=%d\n", **double_pointer);
  // => this line makes the program's state or output explicit
  return 0;
  // => this line makes the program's state or output explicit
}
