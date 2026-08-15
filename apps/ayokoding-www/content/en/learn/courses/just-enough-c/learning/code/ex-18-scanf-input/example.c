// => preprocessor directive needed by this translation unit
#include <stdio.h>
// => this executable statement makes the example observable
int main(void) {
  // => this executable statement makes the example observable
  int value = 0;
  // => this executable statement makes the example observable
  if (scanf("%d", &value) == 1) {
    // => this executable statement makes the example observable
    printf("doubled=%d\n", value * 2);
    // => this executable statement makes the example observable
  }
  // => this executable statement makes the example observable
  return 0;
  // => this executable statement makes the example observable
}
