// learning/code/ex-09-float-epsilon-compare/float_epsilon_compare.c
/* Example 9: Float Epsilon Compare -- fabs(a-b) < 1e-9 succeeds where ==
 * failed. */

#include <math.h>  // => co-14: fabs -- the standard epsilon-comparison building block
#include <stdio.h> // => co-14: printf -- reports both comparison outcomes side by side

int main(void) {         // program entry point
    double a = 0.1;      // => co-14: SAME inputs as ex-08 -- this example is its
                         // direct sequel
    double b = 0.2;      // declares b
    double sum = a + b;  // => co-14: the rounded sum, identical to ex-08
    double target = 0.3; // => co-14: identical target value

    double diff = fabs(sum - target); // => co-14: the ABSOLUTE difference between the two doubles
    double epsilon = 1e-9;            // => co-14: a tolerance many orders of magnitude above 1 ULP here

    int strict_equal = (sum == target);   // => co-14: repeats ex-08's failing strict comparison
    int epsilon_equal = (diff < epsilon); // => co-14: the FIX -- "close enough"
                                          // instead of "bit-identical"

    printf("a + b            = %.20f\n",
           sum); // => co-14: same rounded value as ex-08
    printf("0.3              = %.20f\n",
           target); // => co-14: same target as ex-08
    printf("|diff|           = %.20f\n",
           diff); // => co-14: tiny -- on the order of 1e-17, not 1e-9
    printf("epsilon          = %.1e\n",
           epsilon); // => co-14: the chosen tolerance
    printf("strict (==)      : %s\n",
           strict_equal ? "true" : "false"); // => co-14: expected false -- repeats ex-08
    printf("epsilon (<1e-9)  : %s\n",
           epsilon_equal ? "true" : "false"); // => co-14: expected true -- the fix works

    // ex-09: the exact claim -- the epsilon test PASSES precisely where the
    // strict test FAILED for the identical 0.1 + 0.2 vs 0.3 case from ex-08
    int correct = (!strict_equal) && epsilon_equal; // => co-14: both halves of the contrast must hold
    printf("%s\n", correct                          // => co-14: PASS/FAIL verdict
                       ? "PASS: epsilon compare succeeds exactly where strict == "
                         "failed"                                             // supporting statement for this example
                       : "FAIL: epsilon compare did not behave as expected"); // supporting
                                                                              // statement
                                                                              // for
                                                                              // this
                                                                              // example

    return correct ? 0 : 1; // => co-14: nonzero exit on assertion failure
}
