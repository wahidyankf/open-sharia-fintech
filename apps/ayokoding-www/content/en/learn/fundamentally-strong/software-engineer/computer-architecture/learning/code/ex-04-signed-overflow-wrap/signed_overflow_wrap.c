// learning/code/ex-04-signed-overflow-wrap/signed_overflow_wrap.c
/* Example 4: Signed Overflow Wrap -- INT_MAX + 1 under -fwrapv (defined
 * wraparound). */

#include <limits.h> // => co-12: INT_MAX/INT_MIN -- the two's-complement boundary values under test
#include <stdio.h>  // => co-12: printf -- reports the wrapped value

int main(void) {
    // ex-04: THIS PROGRAM MUST BE COMPILED WITH -fwrapv (see the Compile line
    // below). Without -fwrapv, signed overflow is UNDEFINED BEHAVIOR in C -- the
    // compiler is free to assume it never happens and may optimize this
    // comparison away entirely. -fwrapv is a real, documented Clang/GCC flag that
    // turns UB into a GUARANTEED two's-complement wraparound, which is what this
    // example measures on purpose.
    int max = INT_MAX;     // => co-12: 2147483647 -- the largest representable int
    int wrapped = max + 1; // => co-12: WOULD be UB without -fwrapv; wraps here by contract

    printf("INT_MAX      = %d\n", max); // => co-12: the starting value
    printf("INT_MAX + 1  = %d\n",
           wrapped); // => co-12: the wrapped result, expected to equal INT_MIN
    printf("INT_MIN      = %d\n",
           INT_MIN); // => co-12: -2147483648 -- what two's complement predicts

    int correct = wrapped == INT_MIN; // => co-12: the wraparound assertion this example checks
    printf("%s\n", correct            // => co-12: PASS/FAIL verdict
                       ? "PASS: INT_MAX + 1 wrapped to INT_MIN under -fwrapv"
                       : "FAIL: wraparound did not match INT_MIN");
    printf("note: without -fwrapv this add is UNDEFINED BEHAVIOR, not a "
           "guaranteed wrap\n"); // => co-12: honesty note

    return correct ? 0 : 1; // => co-12: nonzero exit on assertion failure
}
