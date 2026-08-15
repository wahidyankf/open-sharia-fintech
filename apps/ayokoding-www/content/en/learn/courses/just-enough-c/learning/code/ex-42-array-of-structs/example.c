// => this directive makes a declaration available
#include <stdio.h>
// => this line is part of the complete runnable program
struct Item {
  int quantity;
};
// => this line is part of the complete runnable program
int main(void) {
  // => this line is part of the complete runnable program
  struct Item items[] = {{1}, {2}};
  // => this line is part of the complete runnable program
  int total = 0;
  // => this line is part of the complete runnable program
  for (size_t index = 0; index < 2; ++index) {
    // => this line is part of the complete runnable program
    total += items[index].quantity;
    // => this line is part of the complete runnable program
  }
  // => this line is part of the complete runnable program
  printf("total=%d\n", total);
  // => this line is part of the complete runnable program
  return 0;
  // => this line is part of the complete runnable program
}
