/* Example 76: full-systems-slice. Exercises co-07, co-22, co-30.
 * Annotation: this small, safe counterpart keeps the invariant runnable; never
 * deliberately invoke undefined behavior just to obtain a sanitizer report. */
#include <limits.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

int main(void) {
  /* Every example checks a concrete result and returns nonzero on failure. */
  int *owned = malloc(sizeof *owned);
  if (owned == NULL) {
    return 1;
  }
  *owned = 76;
  int pass = (*owned == 76);
  free(owned); /* sole owner releases exactly once */
  printf("PASS ex-76: full-systems-slice\n");
  return pass ? 0 : 1;
}
