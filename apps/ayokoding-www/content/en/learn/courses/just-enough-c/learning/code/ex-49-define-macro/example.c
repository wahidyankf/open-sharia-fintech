// => this directive makes a declaration available
#include <stdio.h>
// => this directive makes a declaration available
#define SQUARE(value) ((value) * (value))
// => this line is part of the complete runnable program
int main(void) {
  // => this line is part of the complete runnable program
  printf("square=%d\n", SQUARE(5));
  // => this line is part of the complete runnable program
  return 0;
  // => this line is part of the complete runnable program
}
