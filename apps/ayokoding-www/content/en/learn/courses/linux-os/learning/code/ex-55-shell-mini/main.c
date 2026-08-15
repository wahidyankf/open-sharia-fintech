#define _POSIX_C_SOURCE 200809L
#include <stdio.h>
#include <unistd.h>
/* shell-mini: exec replaces this process image; a successful exec does not
 * return. */
int main(void) {
  printf("before exec: shell-mini pid=%ld\n", (long)getpid());
  execl("/bin/echo", "echo", "after-exec shell-mini", (char *)NULL);
  return 1;
}
