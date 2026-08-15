// => this directive makes a declaration available
#include <stdio.h>
// => this line is part of the complete runnable program
struct Server {
  int port;
};
// => this line is part of the complete runnable program
int main(void) {
  // => this line is part of the complete runnable program
  struct Server server = {80};
  // => this line is part of the complete runnable program
  struct Server *pointer = &server;
  // => this line is part of the complete runnable program
  printf("port=%d\n", pointer->port);
  // => this line is part of the complete runnable program
  return 0;
  // => this line is part of the complete runnable program
}
