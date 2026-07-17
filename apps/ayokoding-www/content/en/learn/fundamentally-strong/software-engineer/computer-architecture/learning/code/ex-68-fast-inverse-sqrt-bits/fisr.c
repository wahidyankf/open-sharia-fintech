// learning/code/ex-68-fast-inverse-sqrt-bits/fisr.c
/* Example 68: the Quake III fast inverse square root -- bit-hacking a float's
 * IEEE-754 layout. */
#include <math.h>   // => sqrtf: the reference this bit-hack approximates
#include <stdint.h> // => uint32_t: the exact-width integer the float's 32 raw bits get copied into
#include <stdio.h>  // stdio.h: standard library header
#include <string.h> // => memcpy: the standards-legal way to reinterpret a float's bits (no UB, unlike
                    // a `union`-based type pun in strict C, and no aliasing violation like a cast)

// ex-68: the famous magic constant from Quake III Arena's `q_rsqrt` -- co-13:
// this is only meaningful because IEEE-754's bit layout (1 sign + 8 exponent +
// 23 mantissa) makes a float's raw integer bit pattern an approximately LINEAR
// function of log2(value). Halving that integer approximately halves
// log2(value), which approximately computes log2(1/sqrt(value)) =
// -0.5*log2(value).
#define MAGIC 0x5f3759dfu // constant MAGIC = 0x5f3759dfu

// ex-68: reinterpret the float's 32 bits as a uint32_t, shift, subtract from
// the magic constant, reinterpret back as float -- one Newton-Raphson
// refinement step polishes the crude bit-hack guess.
static float fast_inv_sqrt(float x) {  // defines fast_inv_sqrt(): helper function used by this example
    float x_half = 0.5f * x;           // => co-13: needed by the Newton-Raphson step below
    uint32_t bits;                     // declares bits
    memcpy(&bits, &x, sizeof(bits));   // => co-13: float bit pattern, as an integer
                                       // -- legal reinterpretation
    bits = MAGIC - (bits >> 1);        // => co-13: the bit-hack -- an approximate log-domain halving
    float y;                           // declares y
    memcpy(&y, &bits, sizeof(y));      // => co-13: reinterpret the hacked bits back as
                                       // a float -- crude guess
    y = y * (1.5f - (x_half * y * y)); // => one Newton-Raphson iteration: y_new = y*(1.5 - x/2*y^2),
                                       // refines the crude guess to within ~0.2% of the true value
    return y;                          // returns the computed result
}

int main(void) { // program entry point
    // ex-68: a spread of magnitudes -- co-13: the hack must work across the
    // exponent range, not just near 1.0, because it operates on the FULL
    // floating-point bit pattern including the exponent bits.
    float tests[] = {1.0f, 2.0f, 4.0f, 10.0f, 100.0f, 0.25f, 0.01f, 1000.0f}; // declares tests
    int n = (int)(sizeof(tests) / sizeof(tests[0]));                          // declares n

    double max_rel_error = 0.0;                                                  // declares max_rel_error
    printf("value      fast_inv_sqrt   1/sqrtf(value)   rel_error\n");           // prints a
                                                                                 // report line
    for (int i = 0; i < n; i++) {                                                // loop header controlling the sweep below
        float x = tests[i];                                                      // declares x
        float approx = fast_inv_sqrt(x);                                         // => co-13: the bit-hack's answer
        float exact = 1.0f / sqrtf(x);                                           // => the library's correctly-rounded answer
        double rel_error = fabs((double)approx - (double)exact) / (double)exact; // declares rel_error
        if (rel_error > max_rel_error)
            max_rel_error = rel_error;                                                                           // conditional check
        printf("%-10.4f %-15.6f %-16.6f %.6f%%\n", (double)x, (double)approx, (double)exact, rel_error * 100.0); // prints a report line
    }

    printf("\nmax relative error across all test values: %.4f%%\n",
           max_rel_error * 100.0); // prints a report line
    // ex-68: the well-known published tolerance for THIS exact magic-constant +
    // one-Newton-step combination is well under 1% relative error -- verify that
    // tolerance actually holds here.
    int pass = max_rel_error < 0.01; // < 1% relative error
    printf("PASS (max relative error under 1%% across the tested range): %s\n",
           pass ? "PASS" : "FAIL"); // prints a report line
    return 0;                       // returns the computed result
}
