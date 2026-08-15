#define _POSIX_C_SOURCE 200809L
#include <stdio.h>
#include <unistd.h>
/* getpid: a minimal runnable Linux process probe; extend it using this
 * section's command. */
int main(void) {
  printf("getpid pid=%ld\\n", (long)getpid());
  return 0;
}
