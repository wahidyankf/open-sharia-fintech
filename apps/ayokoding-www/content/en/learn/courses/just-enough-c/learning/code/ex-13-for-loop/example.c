// => preprocessor directive needed by this translation unit
#include <stdio.h>
// => this executable statement makes the example observable
int main(void) {
  // => this executable statement makes the example observable
  for (int index = 0; index < 3; ++index) {
    // => this executable statement makes the example observable
    printf("%d%s", index, index == 2 ? "\n" : " ");
    // => this executable statement makes the example observable
  }
  // => this executable statement makes the example observable
  return 0;
  // => this executable statement makes the example observable
}
