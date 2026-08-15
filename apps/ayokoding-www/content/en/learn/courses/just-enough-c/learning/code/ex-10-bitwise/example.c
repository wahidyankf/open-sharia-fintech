// => preprocessor directive needed by this translation unit
#include <stdio.h>
// => this executable statement makes the example observable
int main(void) {
  // => this executable statement makes the example observable
  unsigned int mask = (1u << 0) | (1u << 2);
  // => this executable statement makes the example observable
  printf("mask=%u\n", mask);
  // => this executable statement makes the example observable
  return 0;
  // => this executable statement makes the example observable
}
