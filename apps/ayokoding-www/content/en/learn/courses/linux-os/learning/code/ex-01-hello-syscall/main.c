#define _POSIX_C_SOURCE 200809L
#include <stdio.h>
#include <unistd.h>
/* hello-syscall: a minimal runnable Linux process probe; extend it using this
 * section's command. */
int main(void) {
  printf("hello-syscall pid=%ld\\n", (long)getpid());
  return 0;
}
