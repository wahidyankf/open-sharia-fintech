// => this directive is part of the source interface
#include <stdio.h>
// => this directive is part of the source interface
#include "worker.h"
// => this line makes the program's state or output explicit
int main(void) {
  // => this line makes the program's state or output explicit
  struct Worker worker = {7};
  // => this line makes the program's state or output explicit
  printf("worker=%d\n", worker_id(&worker));
  // => this line makes the program's state or output explicit
  return 0;
  // => this line makes the program's state or output explicit
}
