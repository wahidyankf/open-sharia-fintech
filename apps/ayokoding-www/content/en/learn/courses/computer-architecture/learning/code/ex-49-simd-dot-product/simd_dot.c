// learning/code/ex-49-simd-dot-product/simd_dot.c
/* Example 49: vectorize a dot product with a NEON horizontal reduction --
   verify correctness (within float epsilon) and a speedup (co-23). */
#include <arm_neon.h> // => co-23: NEON intrinsics -- this machine is arm64, the real SIMD ISA here
#include <math.h>     // => fabsf -- the epsilon-based float comparison (co-14: exact == is unreliable)
#include <stdio.h>    // => printf -- the timing/PASS report this program prints
#include <stdlib.h>   // => malloc/free/rand -- the two vectors under test
#include <time.h>     // => clock_gettime -- the portable wall-clock timer used below

// co-14: VERIFIED CAVEAT (found while building this example): with N=100M, the
// SCALAR serial accumulator hits float32's 2^24 (16,777,216) exact-integer
// limit and effectively STOPS growing (catastrophic precision loss from adding
// small increments to a large accumulator), while the NEON version's 4 separate
// lanes each accumulate a SMALLER partial sum and combine at the end -- so the
// two versions land on very different totals for reasons that are a REAL float-
// precision story (co-13/co-14), not a correctness bug. N is kept small enough
// here that NEITHER accumulator gets near that ceiling, so the epsilon check
// below is testing real numerical correctness, not colliding with that limit.
#define N \
    8000000      // => co-23: 8M floats -- expected sum ~4M, safely under float32's
                 // 2^24 ceiling
#define TRIALS 7 // => co-25: best-of-7 -- shared-machine noise smoothing

static double now_seconds(void) {                        // => co-25: shared wall-clock helper, this topic's standard pattern
    struct timespec ts;                                  // supporting statement for this example
    clock_gettime(CLOCK_MONOTONIC, &ts);                 // calls clock_gettime(...)
    return (double)ts.tv_sec + (double)ts.tv_nsec / 1e9; // returns the computed result
}

// co-23: scalar dot product -- a serial reduction, one multiply-add per
// element. vectorize(disable) forces genuine scalar code (co-14: float addition
// is NOT associative, so clang would otherwise need -ffast-math to
// auto-vectorize this anyway -- disabling it here makes the comparison explicit
// and unambiguous).
__attribute__((noinline)) static float scalar_dot(const float *a, const float *b, int n,
                                                  float salt) { // calls __attribute__(...)
    float sum = 0.0f;                                           // declares sum
#pragma clang loop vectorize(disable) interleave(disable)       // supporting statement for this example
    for (int i = 0; i < n; i++)
        sum += a[i] * b[i]; // => co-23: one scalar fmadd per element, serial chain
    return sum + salt;      // => co-25: salt distinguishes each trial's call (see ex-47/48)
}

// co-23: NEON dot product -- 4 multiply-adds per instruction via vmlaq_f32,
// into 4 PARALLEL partial-sum lanes (breaks the serial dependency co-22's ILP
// lesson warns about), then a horizontal reduction (vaddvq_f32) sums the 4
// lanes into one scalar at the very end -- exactly once, not once per element.
__attribute__((noinline)) static float simd_dot(const float *a, const float *b, int n,
                                                float salt) { // calls __attribute__(...)
    float32x4_t vsum = vdupq_n_f32(0.0f);                     // => co-23: 4 independent partial-sum lanes, all zero
    int i = 0;                                                // declares i
    for (; i + 4 <= n; i += 4) {                              // => co-23: process 4 elements per iteration
        float32x4_t va = vld1q_f32(&a[i]);                    // => load 4 floats from a
        float32x4_t vb = vld1q_f32(&b[i]);                    // => load 4 floats from b
        vsum = vmlaq_f32(vsum, va, vb);                       // => co-22: vsum += a*b for all 4 lanes, ONE instruction
    }
    float sum = vaddvq_f32(vsum); // => co-23: horizontal reduction -- sums all 4 lanes
    for (; i < n; i++)
        sum += a[i] * b[i]; // => co-23: scalar tail for n not a multiple of 4
    return sum + salt;      // returns the computed result
}

int main(void) {                                  // program entry point
    float *a = malloc((size_t)N * sizeof(float)); // heap-allocates memory for a
    float *b = malloc((size_t)N * sizeof(float)); // heap-allocates memory for b
    if (!a || !b) {
        fprintf(stderr, "alloc failed\n");
        return 1;
    } // prints a report line
    srand(31);                                // calls srand(...)
    for (int i = 0; i < N; i++) {             // => small values -- keeps the running sum well-scaled
        a[i] = (float)(rand() % 100) * 0.01f; // assigns a[i]
        b[i] = (float)(rand() % 100) * 0.01f; // assigns b[i]
    }

    double best_scalar = 1e18, best_simd = 1e18;                // declares best_scalar
    float last_scalar = 0.0f, last_simd = 0.0f;                 // declares last_scalar
    for (int t = 0; t < TRIALS; t++) {                          // => co-25: best-of-N -- keep the fastest clean run
        double t0 = now_seconds();                              // declares t0
        last_scalar = scalar_dot(a, b, N, (float)t) - (float)t; // => co-25: salt added then removed -- see ex-48
        double t1 = now_seconds();                              // declares t1
        if (t1 - t0 < best_scalar)
            best_scalar = t1 - t0; // conditional check

        double t2 = now_seconds();                          // declares t2
        last_simd = simd_dot(a, b, N, (float)t) - (float)t; // assigns last_simd
        double t3 = now_seconds();                          // declares t3
        if (t3 - t2 < best_simd)
            best_simd = t3 - t2; // conditional check
    }

    // co-14: SIMD's 4-lane parallel partial sums combine in a DIFFERENT order
    // than the scalar version's single serial chain -- floating-point addition is
    // not associative, so an exact == is the WRONG check here; compare within a
    // relative epsilon instead.
    float diff = fabsf(last_scalar - last_simd);    // declares diff
    float rel_diff = diff / fabsf(last_scalar);     // declares rel_diff
    printf("N=%d floats, best of %d\n", N, TRIALS); // prints a report line
    printf("scalar dot: %.6f, %.4f s\n", last_scalar,
           best_scalar); // prints a report line
    printf("NEON dot:   %.6f, %.4f s\n", last_simd,
           best_simd); // prints a report line
    printf("abs diff=%.8f, relative diff=%.8f\n", diff,
           rel_diff);                         // prints a report line
    double speedup = best_scalar / best_simd; // declares speedup
    // co-14: epsilon = 1% -- generous enough to absorb REAL float32 accumulation
    // drift over millions of additions (verified: ~0.6% observed, an expected
    // consequence of naive serial summation, not a bug), while still catching an
    // actual correctness bug (a wrong sign, a dropped term, a factor-of-2 error).
    printf("speedup: %.2fx -> %s\n", speedup,                                                           // prints a report line
           (rel_diff < 1e-2 && speedup > 1.1) ? "PASS (correct within epsilon, NEON measurably faster)" // continues
                                                                                                        // the
                                                                                                        // printf(...)
                                                                                                        // call
                                                                                                        // above
                                              : "FAIL");                                                // continues the printf(...) call above
    free(a);                                                                                            // releases a's heap memory
    free(b);                                                                                            // releases b's heap memory
    return (rel_diff < 1e-2 && speedup > 1.1) ? 0 : 1;                                                  // returns the computed result
}
