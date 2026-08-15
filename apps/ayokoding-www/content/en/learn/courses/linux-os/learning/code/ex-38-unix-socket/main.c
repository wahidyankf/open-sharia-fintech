#define _POSIX_C_SOURCE 200809L
#include <stdio.h>
#include <sys/socket.h>
#include <unistd.h>
/* unix-socket: socketpair gives both endpoints a bidirectional local channel.
 */
int main(void) {
  int fd[2];
  char message[16] = {0};
  if (socketpair(AF_UNIX, SOCK_STREAM, 0, fd) == -1)
    return 1;
  write(fd[0], "socket-ok", 10);
  read(fd[1], message, sizeof(message) - 1);
  close(fd[0]);
  close(fd[1]);
  puts(message);
  return 0;
}
