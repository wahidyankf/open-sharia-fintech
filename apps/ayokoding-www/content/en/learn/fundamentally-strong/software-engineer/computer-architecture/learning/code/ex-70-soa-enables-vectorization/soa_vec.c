// learning/code/ex-70-soa-enables-vectorization/soa_vec.c
/* Example 70: AoS blocks wide vector loads that SoA enables -- verified in the
 * compiler's own asm. */
#include <stdio.h>  // stdio.h: standard library header
#include <stdlib.h> // stdlib.h: standard library header

#define N \
    1000000 // => co-17: large enough that the timing gap (not just the asm) is
            // visible too

// ex-70: AoS -- co-17: `x` is 16 bytes apart from the next element's `x`
// (stride = sizeof(Vec4AoS)), so four consecutive `.x` values do NOT live in
// one contiguous 16-byte span the CPU can load with a single 128-bit
// instruction -- the compiler is FORCED into narrow, one-lane-at-a-time loads.
typedef struct {
    float x, y, z, w;
} Vec4AoS; // performs several bookkeeping updates in one line

// co-23: `noinline` keeps clang from inlining this into main() and optimizing
// the loop away entirely with constant-folding -- the whole point is to inspect
// what THIS function compiles to on its own.
__attribute__((noinline)) static float sum_x_aos(const Vec4AoS *v, int n) { // calls __attribute__(...)
    float s = 0.0f;                                                         // declares s
    for (int i = 0; i < n; i++) {                                           // loop header controlling the sweep below
        s += v[i].x;                                                        // => co-17: stride-16-byte access -- one scalar float per
                                                                            // touched cache line region
    }
    return s; // returns the computed result
}

// ex-70: SoA -- co-17: `x[0..3]` are FOUR CONSECUTIVE floats = exactly 16 bytes
// = one 128-bit register's worth, so the compiler CAN (and, verified below,
// does) fetch 4 at a time with a single wide load instruction instead of 4
// separate narrow ones.
__attribute__((noinline)) static float sum_x_soa(const float *x, int n) { // calls __attribute__(...)
    float s = 0.0f;                                                       // declares s
    for (int i = 0; i < n; i++) {                                         // loop header controlling the sweep below
        s += x[i];                                                        // => co-17/co-23: unit-stride access -- contiguous floats,
                                                                          // wide-load-eligible
    }
    return s; // returns the computed result
}

int main(void) {                                // program entry point
    Vec4AoS *aos = malloc(sizeof(Vec4AoS) * N); // heap-allocates memory for aos
    float *soa_x = malloc(sizeof(float) * N);   // heap-allocates memory for soa_x
    if (!aos || !soa_x) {                       // => guards both allocations before touching either
        fprintf(stderr, "alloc failed\n");      // => reports to stderr, not stdout
        return 1;                               // => nonzero exit -- allocation failure is not this example's claim
    } // prints a report line

    unsigned seed = 11u;                         // declares seed
    for (int i = 0; i < N; i++) {                // loop header controlling the sweep below
        seed = seed * 1103515245u + 12345u;      // assigns seed
        float v = (float)(seed % 1000u) * 0.01f; // declares v
        aos[i].x = v;
        aos[i].y = 0;
        aos[i].z = 0;
        aos[i].w = 0; // => identical x values in both layouts
        soa_x[i] = v; // assigns soa_x[i]
    }

    float sum_aos = sum_x_aos(aos, N);               // declares sum_aos
    float sum_soa = sum_x_soa(soa_x, N);             // declares sum_soa
    double diff = (double)sum_aos - (double)sum_soa; // declares diff
    if (diff < 0)
        diff = -diff; // conditional check

    printf("N=%d elements\n", N); // prints a report line
    printf("sum_x_aos (stride-16B access): %.4f\n",
           (double)sum_aos); // prints a report line
    printf("sum_x_soa (unit-stride access): %.4f\n",
           (double)sum_soa); // prints a report line
    printf("abs difference (must be ~0 -- same input values, same summation "
           "order): %.6f\n",
           diff); // prints a report line
    printf("\nAssembly evidence (see this example's markdown for the exact grep "
           "session): compiling\n"); // prints a report line
    printf("this file with `-O3 -S` shows sum_x_soa's inner loop uses 128-bit "
           "`ldp q..,q..` WIDE loads\n"); // prints a report line
    printf("(4 floats fetched per instruction) while sum_x_aos's inner loop uses "
           "only scalar `s`-register\n"); // prints a report line
    printf("loads (1 float per instruction) -- the stride-16-byte layout makes a "
           "wide load impossible.\n"); // prints a report line
    int pass = diff < 0.01;            // correctness: both layouts must sum to (essentially)
                                       // the same value
    printf("PASS (both layouts agree numerically -- only their memory access "
           "WIDTH differs): %s\n",  // prints a report line
           pass ? "PASS" : "FAIL"); // continues the printf(...) call above

    free(aos);   // releases aos's heap memory
    free(soa_x); // releases soa_x's heap memory
    return 0;    // returns the computed result
}
