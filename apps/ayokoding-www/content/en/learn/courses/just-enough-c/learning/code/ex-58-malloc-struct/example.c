// => this directive is part of the source interface
#include <stdio.h>
// => this directive is part of the source interface
#include <stdlib.h>
// => this line makes the program's state or output explicit
struct Server {
  int port;
};
// => this line makes the program's state or output explicit
int main(void) {
  // => this line makes the program's state or output explicit
  struct Server *server = malloc(sizeof *server);
  // => this line makes the program's state or output explicit
  if (server == NULL)
    return 1;
  // => this line makes the program's state or output explicit
  server->port = 443;
  // => this line makes the program's state or output explicit
  printf("port=%d\n", server->port);
  // => this line makes the program's state or output explicit
  free(server);
  // => this line makes the program's state or output explicit
  return 0;
  // => this line makes the program's state or output explicit
}
