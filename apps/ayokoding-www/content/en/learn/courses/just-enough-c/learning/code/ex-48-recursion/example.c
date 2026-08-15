// => this directive makes a declaration available
#include <stdio.h>
// => this line is part of the complete runnable program
static int factorial(int value) {
  // => this line is part of the complete runnable program
  return value <= 1 ? 1 : value * factorial(value - 1);
  // => this line is part of the complete runnable program
}
// => this line is part of the complete runnable program
int main(void) {
  // => this line is part of the complete runnable program
  printf("factorial=%d\n", factorial(5));
  // => this line is part of the complete runnable program
  return 0;
  // => this line is part of the complete runnable program
}
