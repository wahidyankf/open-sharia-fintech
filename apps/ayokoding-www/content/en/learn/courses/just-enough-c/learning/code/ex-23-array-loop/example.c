// => preprocessor directive needed by this translation unit
#include <stdio.h>
// => this executable statement makes the example observable
int main(void) {
  // => this executable statement makes the example observable
  int values[] = {1, 2, 3};
  // => this executable statement makes the example observable
  int sum = 0;
  // => this executable statement makes the example observable
  for (size_t index = 0; index < 3; ++index) {
    // => this executable statement makes the example observable
    sum += values[index];
    // => this executable statement makes the example observable
  }
  // => this executable statement makes the example observable
  printf("sum=%d\n", sum);
  // => this executable statement makes the example observable
  return 0;
  // => this executable statement makes the example observable
}
