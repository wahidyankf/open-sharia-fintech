// => this directive makes a declaration available
#include <stdio.h>
// => this line is part of the complete runnable program
struct Service {
  const char *name;
};
// => this line is part of the complete runnable program
int main(void) {
  // => this line is part of the complete runnable program
  struct Service service = {.name = "api"};
  // => this line is part of the complete runnable program
  printf("service=%s\n", service.name);
  // => this line is part of the complete runnable program
  return 0;
  // => this line is part of the complete runnable program
}
