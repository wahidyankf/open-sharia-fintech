// => this directive makes a declaration available
#include <stdio.h>
// => this line is part of the complete runnable program
int main(void) {
  // => this line is part of the complete runnable program
  int value = 9;
  // => this line is part of the complete runnable program
  int *address = &value;
  // => this line is part of the complete runnable program
  printf("address-captured=%d\n", address == &value);
  // => this line is part of the complete runnable program
  return 0;
  // => this line is part of the complete runnable program
}
