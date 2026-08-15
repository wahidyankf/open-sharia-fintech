// => this directive is part of the source interface
#include <stdio.h>
// => this line makes the program's state or output explicit
struct Record {
  char tag;
  int id;
};
// => this line makes the program's state or output explicit
int main(void) {
  // => this line makes the program's state or output explicit
  printf("record-bytes=%zu\n", sizeof(struct Record));
  // => this line makes the program's state or output explicit
  return 0;
  // => this line makes the program's state or output explicit
}
