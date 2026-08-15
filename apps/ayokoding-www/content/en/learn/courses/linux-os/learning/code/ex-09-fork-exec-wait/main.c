#define _POSIX_C_SOURCE 200809L
#include <stdio.h>
#include <unistd.h>
/* fork-exec-wait: exec replaces this process image; a successful exec does not
 * return. */
int main(void) {
  printf("before exec: fork-exec-wait pid=%ld\n", (long)getpid());
  execl("/bin/echo", "echo", "after-exec fork-exec-wait", (char *)NULL);
  return 1;
}
