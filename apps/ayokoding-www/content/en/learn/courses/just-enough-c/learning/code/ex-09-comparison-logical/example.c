// => preprocessor directive needed by this translation unit
#include <stdio.h>
// => this executable statement makes the example observable
int main(void) {
  // => this executable statement makes the example observable
  int age = 20;
  // => this executable statement makes the example observable
  int allowed = age >= 18 && age < 65;
  // => this executable statement makes the example observable
  printf("allowed=%d\n", allowed);
  // => this executable statement makes the example observable
  return 0;
  // => this executable statement makes the example observable
}
