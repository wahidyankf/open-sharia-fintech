// learning/code/ex-67-kahan-summation/kahan.c
/* Example 67: naive float summation vs Kahan compensated summation. */
#include <math.h>  // => fabs: measuring each method's error against a known-exact reference
#include <stdio.h> // stdio.h: standard library header

#define N \
    10000000 // => co-13/co-14: 10M additions -- large enough for float rounding
             // error to compound visibly

int main(void) {                          // program entry point
    float x = 0.1f;                       // => co-13: the SAME float value added every iteration
    double exact = (double)N * (double)x; // => co-13: exact reference -- N*x computed as ONE double
                                          // multiply (no accumulated rounding, unlike a 10M-step loop)

    // ex-67: NAIVE summation -- co-14: as `naive_sum` grows toward N*x ~=
    // 1,000,000, its float ULP (unit in the last place) grows past 0.1 -- so many
    // individual `+= 0.1f` additions round DOWN to a no-op, and the error
    // silently accumulates over all 10M iterations.
    float naive_sum = 0.0f;        // declares naive_sum
    for (long i = 0; i < N; i++) { // loop header controlling the sweep below
        naive_sum += x;            // => co-14: each add can lose the low bits of x once sum is large
    }

    // ex-67: KAHAN compensated summation -- co-13/co-14: `c` tracks the rounding
    // error LOST on the previous addition and feeds it back in on the next one,
    // so error does not silently accumulate.
    float kahan_sum = 0.0f;        // declares kahan_sum
    float c = 0.0f;                // => co-14: running compensation for lost low-order bits
    for (long i = 0; i < N; i++) { // loop header controlling the sweep below
        float y = x - c;           // => co-14: correct this iteration's input by the PRIOR error
        float t = kahan_sum + y;   // => co-14: the addition that may itself lose low bits of y
        c = (t - kahan_sum) - y;   // => co-14: recover exactly what got lost -- (t-kahan_sum) is
                                   // what the FP unit actually added; subtracting y reveals the miss
        kahan_sum = t;             // => co-14: commit the new running sum
    }

    double naive_error = fabs((double)naive_sum - exact); // declares naive_error
    double kahan_error = fabs((double)kahan_sum - exact); // declares kahan_error

    printf("N=%d additions of %.1f (float)\n", N,
           (double)x); // prints a report line
    printf("exact reference (N * x, one double multiply): %.4f\n",
           exact);                                                                                    // prints a report line
    printf("naive float sum:  %.4f  (error=%.4f, %.4f%% of exact)\n", (double)naive_sum, naive_error, // prints a report line
           100.0 * naive_error / exact);                                                              // continues the printf(...) call above
    printf("kahan float sum:  %.4f  (error=%.6f, %.6f%% of exact)\n", (double)kahan_sum, kahan_error, // prints a report line
           100.0 * kahan_error / exact);                                                              // continues the printf(...) call above
    double improvement = naive_error / (kahan_error > 0 ? kahan_error : 1e-12);                       // declares improvement
    printf("kahan is %.1fx more accurate than naive (smaller absolute error)\n",
           improvement);                                           // prints a report line
    int pass = (kahan_error < naive_error) && (naive_error > 1.0); // naive must show REAL, visible drift
    printf("PASS (kahan strictly more accurate than naive, and naive's error is "
           "non-trivial): %s\n",    // prints a report line
           pass ? "PASS" : "FAIL"); // continues the printf(...) call above
    return 0;                       // returns the computed result
}
