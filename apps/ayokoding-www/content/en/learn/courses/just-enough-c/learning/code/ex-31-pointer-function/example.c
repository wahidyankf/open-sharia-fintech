// => this directive makes a declaration available
#include <stdio.h>
// => this line is part of the complete runnable program
static void increment(int *value) {
  // => this line is part of the complete runnable program
  *value += 1;
  // => this line is part of the complete runnable program
}
// => this line is part of the complete runnable program
int main(void) {
  // => this line is part of the complete runnable program
  int value = 10;
  // => this line is part of the complete runnable program
  increment(&value);
  // => this line is part of the complete runnable program
  printf("value=%d\n", value);
  // => this line is part of the complete runnable program
  return 0;
  // => this line is part of the complete runnable program
}
