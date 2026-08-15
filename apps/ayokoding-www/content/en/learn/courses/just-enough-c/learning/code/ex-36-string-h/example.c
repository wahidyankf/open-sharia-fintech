// => this directive makes a declaration available
#include <stdio.h>
// => this directive makes a declaration available
#include <string.h>
// => this line is part of the complete runnable program
int main(void) {
  // => this line is part of the complete runnable program
  char copy[8];
  // => this line is part of the complete runnable program
  strcpy(copy, "cat");
  // => this line is part of the complete runnable program
  printf("copy=%s length=%zu\n", copy, strlen(copy));
  // => this line is part of the complete runnable program
  return 0;
  // => this line is part of the complete runnable program
}
