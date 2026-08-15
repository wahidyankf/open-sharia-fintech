// => this directive is part of the source interface
#include <stdio.h>
// => this line makes the program's state or output explicit
int main(void) {
  // => this line makes the program's state or output explicit
  int value = 0;
  // => this line makes the program's state or output explicit
  int sum = 0;
  // => this line makes the program's state or output explicit
  while (scanf("%d", &value) == 1) {
    // => this line makes the program's state or output explicit
    sum += value;
    // => this line makes the program's state or output explicit
  }
  // => this line makes the program's state or output explicit
  printf("sum=%d\n", sum);
  // => this line makes the program's state or output explicit
  return 0;
  // => this line makes the program's state or output explicit
}
