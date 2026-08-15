#define _POSIX_C_SOURCE 200809L
#include <stdio.h>
#include <unistd.h>
/* exec-basic: exec replaces this process image; a successful exec does not
 * return. */
int main(void) {
  printf("before exec: exec-basic pid=%ld\n", (long)getpid());
  execl("/bin/echo", "echo", "after-exec exec-basic", (char *)NULL);
  return 1;
}
