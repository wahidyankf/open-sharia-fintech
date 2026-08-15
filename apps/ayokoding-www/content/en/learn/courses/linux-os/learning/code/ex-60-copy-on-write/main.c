#define _POSIX_C_SOURCE 200809L
#include <stdio.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>
/* copy-on-write: fork creates a child; the parent reaps it to avoid a zombie.
 */
int main(void) {
  pid_t child = fork();
  int status = 0;
  if (child < 0)
    return 1;
  if (child == 0) {
    printf("child pid=%ld ppid=%ld\n", (long)getpid(), (long)getppid());
    _exit(7);
  }
  waitpid(child, &status, 0);
  printf("parent pid=%ld child=%ld status=%d\n", (long)getpid(), (long)child,
         WEXITSTATUS(status));
  return 0;
}
