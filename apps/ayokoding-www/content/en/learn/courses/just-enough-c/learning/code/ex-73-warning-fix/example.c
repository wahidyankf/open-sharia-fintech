// => this directive is part of the source interface
#include <stdio.h>
// => this directive is part of the source interface
#include <string.h>
// => this line makes the program's state or output explicit
int main(void) {
  // => this line makes the program's state or output explicit
  const char *word = "cat";
  // => this line makes the program's state or output explicit
  size_t length = strlen(word);
  // => this line makes the program's state or output explicit
  printf("length=%zu\n", length);
  // => this line makes the program's state or output explicit
  return 0;
  // => this line makes the program's state or output explicit
}
