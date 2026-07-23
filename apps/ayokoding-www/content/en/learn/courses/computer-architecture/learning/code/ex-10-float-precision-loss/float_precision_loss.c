// learning/code/ex-10-float-precision-loss/float_precision_loss.c
/* Example 10: Float Precision Loss -- a tiny addend silently vanishes into a
 * large float. */

#include <stdio.h> // => co-13: printf -- reports the value before and after the addition

int main(void) {
    // ex-10: float has a 23-bit mantissa -- about 7.2 DECIMAL digits of
    // precision. 100,000,000.0f already consumes all 7-8 of those digits, leaving
    // no room to represent a "+1" that would land in the ones place -- the
    // addition rounds right back to the original value, and the tiny addend is
    // silently discarded.
    float large = 100000000.0f; // => co-13: 1e8 -- at the edge of float's
                                // ~7-digit precision
    float tiny = 1.0f;          // => co-13: would need a units-place digit float can't spare here

    float sum = large + tiny; // => co-14: rounds to nearest REPRESENTABLE float
                              // -- may equal `large`

    printf("large        = %.1f\n", large); // => co-13: the starting large value
    printf("tiny         = %.1f\n",
           tiny); // => co-13: the small addend being tested
    printf("large + tiny = %.1f\n",
           sum); // => co-14: expected to print IDENTICAL to `large`
    printf("sum == large ? %s\n",
           (sum == large) ? "true" : "false"); // => co-14: the assertion this example checks

    // ex-10: the syllabus's claim -- the tiny addend is LOST, i.e. sum equals
    // large, unchanged, as if `+ tiny` had never happened
    int correct = (sum == large); // => co-14: precision loss confirmed if sum didn't move at all
    printf("%s\n",
           correct // => co-14: PASS/FAIL verdict
               ? "PASS: large + tiny == large -- the tiny addend was silently lost "
                 "to rounding"
               : "FAIL: tiny addend was NOT lost -- large + tiny changed the value");

    return correct ? 0 : 1; // => co-14: nonzero exit on assertion failure
}
