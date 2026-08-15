#define _POSIX_C_SOURCE 200809L
#include <signal.h>
#include <stdio.h>
#include <unistd.h>
/* shell-signal: sigaction installs a handler; handler work is intentionally
 * minimal. */
static volatile sig_atomic_t seen = 0;
static void handler(int signal_number) { seen = signal_number; }
int main(void) {
  struct sigaction action = {0};
  action.sa_handler = handler;
  sigemptyset(&action.sa_mask);
  if (sigaction(SIGUSR1, &action, NULL) == -1)
    return 1;
  raise(SIGUSR1);
  printf("signal=%d pid=%ld\n", (int)seen, (long)getpid());
  return seen == SIGUSR1 ? 0 : 1;
}
