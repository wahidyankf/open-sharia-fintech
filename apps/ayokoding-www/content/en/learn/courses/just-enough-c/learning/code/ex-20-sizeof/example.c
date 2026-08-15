// => preprocessor directive needed by this translation unit
#include <stdio.h>
// => this executable statement makes the example observable
struct Pair {
  int left;
  int right;
};
// => this executable statement makes the example observable
int main(void) {
  // => this executable statement makes the example observable
  printf("int=%zu pair=%zu\n", sizeof(int), sizeof(struct Pair));
  // => this executable statement makes the example observable
  return 0;
  // => this executable statement makes the example observable
}
