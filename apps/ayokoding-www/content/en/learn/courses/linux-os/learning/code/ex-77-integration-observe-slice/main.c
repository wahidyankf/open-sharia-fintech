#if defined(__APPLE__)
#define _DARWIN_C_SOURCE
#endif
#define _DEFAULT_SOURCE
#define _POSIX_C_SOURCE 200809L
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>
#ifndef MAP_ANONYMOUS
#define MAP_ANONYMOUS MAP_ANON
#endif
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>

struct shared_state {
  char message[32];
};
static volatile sig_atomic_t signal_seen = 0;
static void on_usr1(int ignored) {
  (void)ignored;
  signal_seen = 1;
}

int main(void) {
  /* Parent setup: a signal handler, one pipe, and one shared anonymous mapping.
   */
  int fd[2];
  struct shared_state *shared;
  pid_t child;
  int status;
  char pipe_message[32] = {0};
  struct sigaction action = {0};
  action.sa_handler = on_usr1;
  action.sa_flags = SA_RESTART;
  sigemptyset(&action.sa_mask);
  if (sigaction(SIGUSR1, &action, NULL) == -1 || pipe(fd) == -1)
    return 1;
  shared = mmap(NULL, sizeof(*shared), PROT_READ | PROT_WRITE,
                MAP_SHARED | MAP_ANONYMOUS, -1, 0);
  if (shared == MAP_FAILED)
    return 1;
  child = fork();
  if (child == -1)
    return 1;
  if (child == 0) {
    /* Child publishes through two channels, then exec replaces its image. */
    close(fd[0]);
    strcpy(shared->message, "shared-state");
    write(fd[1], "pipe-ready", 11);
    kill(getppid(), SIGUSR1);
    close(fd[1]);
    execlp("true", "true", (char *)NULL);
    _exit(127);
  }
  /* Parent consumes the pipe, observes signal delivery, and reaps
   * deterministically. */
  close(fd[1]);
  read(fd[0], pipe_message, sizeof(pipe_message) - 1);
  close(fd[0]);
  waitpid(child, &status, 0);
  printf("child=%ld pipe=%s shared=%s signal=%d exit=%d\n", (long)child,
         pipe_message, shared->message, signal_seen,
         WIFEXITED(status) ? WEXITSTATUS(status) : -1);
  munmap(shared, sizeof(*shared));
  return 0;
}
