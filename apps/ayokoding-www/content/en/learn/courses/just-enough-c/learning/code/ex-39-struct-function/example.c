// => this directive makes a declaration available
#include <stdio.h>
// => this line is part of the complete runnable program
struct Score {
  int value;
};
// => this line is part of the complete runnable program
static void raise_copy(struct Score score) {
  // => this line is part of the complete runnable program
  score.value = 9;
  // => this line is part of the complete runnable program
  printf("inside=%d ", score.value);
  // => this line is part of the complete runnable program
}
// => this line is part of the complete runnable program
int main(void) {
  // => this line is part of the complete runnable program
  struct Score score = {3};
  // => this line is part of the complete runnable program
  raise_copy(score);
  // => this line is part of the complete runnable program
  printf("outside=%d\n", score.value);
  // => this line is part of the complete runnable program
  return 0;
  // => this line is part of the complete runnable program
}
