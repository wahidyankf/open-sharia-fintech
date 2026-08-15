// => preprocessor directive needed by this translation unit
#include <stdio.h>
// => this executable statement makes the example observable
int main(void) {
  // => this executable statement makes the example observable
  int remaining = 3;
  // => this executable statement makes the example observable
  while (remaining > 0) {
    // => this executable statement makes the example observable
    printf("%d%s", remaining, remaining == 1 ? "\n" : " ");
    // => this executable statement makes the example observable
    --remaining;
    // => this executable statement makes the example observable
  }
  // => this executable statement makes the example observable
  return 0;
  // => this executable statement makes the example observable
}
