#define _POSIX_C_SOURCE 200809L
#include <fcntl.h>
#include <stdio.h>
#include <unistd.h>
/* ps-tree: /proc is Linux's live process/filesystem observation interface. */
int main(void) {
  int fd = open("/proc/self/status", O_RDONLY);
  char buffer[81] = {0};
  if (fd == -1)
    return 1;
  read(fd, buffer, sizeof(buffer) - 1);
  close(fd);
  printf("ps-tree pid=%ld\\n%.80s\\n", (long)getpid(), buffer);
  return 0;
}
