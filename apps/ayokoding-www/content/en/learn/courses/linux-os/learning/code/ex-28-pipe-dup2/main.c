#define _POSIX_C_SOURCE 200809L
#include <stdio.h>
#include <sys/wait.h>
#include <unistd.h>
/* pipe-dup2: one pipe endpoint is closed on each side so EOF has a clear owner.
 */
int main(void) {
  int fd[2];
  char message[32] = {0};
  pid_t child;
  if (pipe(fd) == -1 || (child = fork()) == -1)
    return 1;
  if (child == 0) {
    close(fd[0]);
    write(fd[1], "pipe-byte-stream", 17);
    close(fd[1]);
    _exit(0);
  }
  close(fd[1]);
  read(fd[0], message, sizeof(message) - 1);
  close(fd[0]);
  waitpid(child, NULL, 0);
  printf("%s\n", message);
  return 0;
}
