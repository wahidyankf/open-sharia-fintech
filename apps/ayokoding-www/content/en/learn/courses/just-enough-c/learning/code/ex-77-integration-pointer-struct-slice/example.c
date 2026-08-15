// => this directive is part of the source interface
#include <stdio.h>
// => this directive is part of the source interface
#include <stdlib.h>
// => this line makes the program's state or output explicit
struct Slice {
  const char *name;
};
// => this line makes the program's state or output explicit
int main(void) {
  // => this line makes the program's state or output explicit
  struct Slice *slice = malloc(sizeof *slice);
  // => this line makes the program's state or output explicit
  if (slice == NULL)
    return 1;
  // => this line makes the program's state or output explicit
  slice->name = "systems";
  // => this line makes the program's state or output explicit
  printf("slice=%s\n", slice->name);
  // => this line makes the program's state or output explicit
  free(slice);
  // => this line makes the program's state or output explicit
  return 0;
  // => this line makes the program's state or output explicit
}
