// => this directive makes a declaration available
#include <stdio.h>
// => this line is part of the complete runnable program
struct Counter {
  int count;
};
// => this line is part of the complete runnable program
static void increment(struct Counter *counter) {
  // => this line is part of the complete runnable program
  counter->count += 1;
  // => this line is part of the complete runnable program
}
// => this line is part of the complete runnable program
int main(void) {
  // => this line is part of the complete runnable program
  struct Counter counter = {1};
  // => this line is part of the complete runnable program
  increment(&counter);
  // => this line is part of the complete runnable program
  printf("count=%d\n", counter.count);
  // => this line is part of the complete runnable program
  return 0;
  // => this line is part of the complete runnable program
}
