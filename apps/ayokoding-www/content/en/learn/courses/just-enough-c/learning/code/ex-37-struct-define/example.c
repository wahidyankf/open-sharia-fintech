// => this directive makes a declaration available
#include <stdio.h>
// => this line is part of the complete runnable program
struct User {
  const char *name;
  int id;
};
// => this line is part of the complete runnable program
int main(void) {
  // => this line is part of the complete runnable program
  struct User user = {"Ada", 7};
  // => this line is part of the complete runnable program
  printf("%s %d\n", user.name, user.id);
  // => this line is part of the complete runnable program
  return 0;
  // => this line is part of the complete runnable program
}
