// learning/code/ex-05-unsigned-wraparound/unsigned_wraparound.c
/* Example 5: Unsigned Wraparound -- 0u - 1u, a DEFINED modulo-2^n wrap. */

#include <limits.h> // => co-12: UINT_MAX -- the expected result of underflowing past zero
#include <stdio.h>  // => co-12: printf -- reports the wrapped value

int main(void) {                      // program entry point
    unsigned int zero = 0u;           // => co-12: the smallest representable unsigned value
    unsigned int wrapped = zero - 1u; // => co-12: unsigned underflow -- DEFINED to wrap mod 2^32, no UB

    printf("0u           = %u\n", zero); // => co-12: the starting value
    printf("0u - 1u      = %u\n",
           wrapped); // => co-12: expected to equal UINT_MAX (4294967295)
    printf("UINT_MAX     = %u\n",
           UINT_MAX); // => co-12: 2^32 - 1 -- what modulo arithmetic predicts

    int correct = wrapped == UINT_MAX; // => co-12: the wraparound assertion this example checks
    printf("%s\n",
           correct // => co-12: PASS/FAIL verdict
               ? "PASS: 0u - 1u wrapped to UINT_MAX (defined, unlike signed "
                 "overflow)"                                          // supporting statement for this example
               : "FAIL: unsigned wraparound did not match UINT_MAX"); // supporting
                                                                      // statement
                                                                      // for this
                                                                      // example

    return correct ? 0 : 1; // => co-12: nonzero exit on assertion failure
}
