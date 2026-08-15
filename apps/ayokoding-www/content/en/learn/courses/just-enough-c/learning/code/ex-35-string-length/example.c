// => this directive makes a declaration available
#include <stdio.h>
// => this line is part of the complete runnable program
int main(void) {
  // => this line is part of the complete runnable program
  const char *word = "cat";
  // => this line is part of the complete runnable program
  size_t length = 0;
  // => this line is part of the complete runnable program
  while (word[length] != '\0') {
    // => this line is part of the complete runnable program
    ++length;
    // => this line is part of the complete runnable program
  }
  // => this line is part of the complete runnable program
  printf("length=%zu\n", length);
  // => this line is part of the complete runnable program
  return 0;
  // => this line is part of the complete runnable program
}
