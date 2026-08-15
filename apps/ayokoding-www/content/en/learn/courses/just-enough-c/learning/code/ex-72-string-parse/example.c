// => this directive is part of the source interface
#include <stdio.h>
// => this line makes the program's state or output explicit
int main(void) {
  // => this line makes the program's state or output explicit
  char name[16];
  // => this line makes the program's state or output explicit
  int age = 0;
  // => this line makes the program's state or output explicit
  if (sscanf("ada:37", "%15[^:]:%d", name, &age) != 2)
    return 1;
  // => this line makes the program's state or output explicit
  printf("name=%s age=%d\n", name, age);
  // => this line makes the program's state or output explicit
  return 0;
  // => this line makes the program's state or output explicit
}
