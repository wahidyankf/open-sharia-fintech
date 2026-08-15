// => this directive makes a declaration available
#include <stdio.h>
// => this line is part of the complete runnable program
int main(void) {
  // => this line is part of the complete runnable program
  int value = 0;
  // => this line is part of the complete runnable program
  int *pointer = &value;
  // => this line is part of the complete runnable program
  *pointer = 5;
  // => this line is part of the complete runnable program
  printf("value=%d\n", value);
  // => this line is part of the complete runnable program
  return 0;
  // => this line is part of the complete runnable program
}
