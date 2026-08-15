// => this directive makes a declaration available
#include <stdio.h>
// => this line is part of the complete runnable program
static int volume(int width, int height, int depth) {
  // => this line is part of the complete runnable program
  return width * height * depth;
  // => this line is part of the complete runnable program
}
// => this line is part of the complete runnable program
int main(void) {
  // => this line is part of the complete runnable program
  printf("volume=%d\n", volume(2, 3, 4));
  // => this line is part of the complete runnable program
  return 0;
  // => this line is part of the complete runnable program
}
