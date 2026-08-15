// => this directive is part of the source interface
#include <stdio.h>
// => this line makes the program's state or output explicit
int add(int left, int right);
// => this line makes the program's state or output explicit
int main(void) {
  // => this line makes the program's state or output explicit
  puts("multi-file build");
  // => this line makes the program's state or output explicit
  return add(1, 1) == 2 ? 0 : 1;
  // => this line makes the program's state or output explicit
}
