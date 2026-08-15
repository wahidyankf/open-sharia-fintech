// => this directive makes a declaration available
#include <stdio.h>
// => this line is part of the complete runnable program
static int first(const int values[]) {
  // => this line is part of the complete runnable program
  return values[0];
  // => this line is part of the complete runnable program
}
// => this line is part of the complete runnable program
int main(void) {
  // => this line is part of the complete runnable program
  int values[] = {4, 5};
  // => this line is part of the complete runnable program
  printf("first=%d\n", first(values));
  // => this line is part of the complete runnable program
  return 0;
  // => this line is part of the complete runnable program
}
