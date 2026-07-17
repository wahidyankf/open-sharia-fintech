// learning/code/ex-08-float-not-equal/float_not_equal.c
/* Example 8: Float Not Equal -- 0.1 + 0.2 != 0.3 in double precision, bit-level
 * cause shown. */

#include <stdio.h>  // => co-13: printf -- reports both the value-level and bit-level mismatch
#include <string.h> // => co-13: memcpy -- reinterprets a double's 8 bytes as a uint64_t, UB-free

int main(void) {         // program entry point
    double a = 0.1;      // => co-13: 0.1 has NO exact finite binary representation
    double b = 0.2;      // => co-13: same problem -- both are ROUNDED to nearest double
    double sum = a + b;  // => co-14: the rounded 0.1 plus the rounded 0.2, then rounded again
    double target = 0.3; // => co-13: 0.3 is ALSO rounded, but to a DIFFERENT nearby double

    unsigned long long sum_bits, // => co-13: two unsigned 64-bit slots for the raw bit patterns
        target_bits;             // => co-13: raw 64-bit patterns for a byte-level comparison
    memcpy(&sum_bits, &sum,      // => co-13: copies sum's 8 bytes into sum_bits, no aliasing UB
           sizeof sum_bits);     // => co-13: memcpy avoids strict-aliasing UB
    memcpy(&target_bits, &target,
           sizeof target_bits); // => co-13: same technique applied to target

    printf("a + b        = %.20f\n",
           sum); // => co-14: 20 digits reveals the rounding error visually
    printf("0.3          = %.20f\n",
           target);                             // => co-14: a DIFFERENT tail of digits than a + b
    printf("a + b == 0.3 ? %s\n",               // => co-14: the strict equality this example
                                                // proves unreliable
           (sum == target) ? "true" : "false"); // supporting statement for this example
    printf("sum bits     = 0x%016llx\n",
           sum_bits); // => co-13: raw bit pattern of a + b
    printf("target bits  = 0x%016llx\n",
           target_bits);                                  // => co-13: raw bit pattern of 0.3 -- differs by 1 ULP here
    printf("bit diff     = %lld\n",                       // => co-13: signed integer difference between
                                                          // the two patterns
           (long long)sum_bits - (long long)target_bits); // supporting statement for this example

    // ex-08: the syllabus's own claim -- strict == must be false, and the two bit
    // patterns must differ (proving this ISN'T a display-only rounding artifact)
    int correct = (sum != target) && (sum_bits != target_bits); // => co-14: both the value AND the bits genuinely differ
    printf("%s\n",
           correct // => co-14: PASS/FAIL verdict
               ? "PASS: 0.1 + 0.2 != 0.3 -- strict == is false, bit patterns "
                 "genuinely differ"                           // supporting statement for this example
               : "FAIL: 0.1 + 0.2 unexpectedly equaled 0.3"); // supporting statement
                                                              // for this example

    return correct ? 0 : 1; // => co-14: nonzero exit on assertion failure
}
