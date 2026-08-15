#if defined(__APPLE__)
#define _DARWIN_C_SOURCE
#endif
#define _DEFAULT_SOURCE
#define _POSIX_C_SOURCE 200809L
#include <stdio.h>
#include <string.h>
#include <sys/mman.h>
#ifndef MAP_ANONYMOUS
#define MAP_ANONYMOUS MAP_ANON
#endif
/* mmap-shared: an anonymous mapping is visible in /proc/self/maps while alive.
 */
int main(void) {
  char *page = mmap(NULL, 4096, PROT_READ | PROT_WRITE,
                    MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
  if (page == MAP_FAILED)
    return 1;
  strcpy(page, "mapped Linux page");
  printf("%s at %p\n", page, (void *)page);
  return munmap(page, 4096);
}
