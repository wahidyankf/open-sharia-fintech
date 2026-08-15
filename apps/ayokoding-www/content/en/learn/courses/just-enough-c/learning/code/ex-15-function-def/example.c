// => preprocessor directive needed by this translation unit
#include <stdio.h>
// => this executable statement makes the example observable
static int square(int value) {
  // => this executable statement makes the example observable
  return value * value;
  // => this executable statement makes the example observable
}
// => this executable statement makes the example observable
int main(void) {
  // => this executable statement makes the example observable
  printf("%d\n", square(3));
  // => this executable statement makes the example observable
  return 0;
  // => this executable statement makes the example observable
}
