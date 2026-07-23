// learning/code/ex-48-simd-intrinsics-add/simd_add.c
/* Example 48: hand-write a NEON vector add -- verify it matches the scalar
   result and is faster (co-23). */
#include <arm_neon.h> // => co-23: NEON intrinsics -- this machine is arm64, the real SIMD ISA here
#include <stdio.h>    // => printf -- the timing/PASS report this program prints
#include <stdlib.h>   // => malloc/free/rand -- the three arrays under test
#include <time.h>     // => clock_gettime -- the portable wall-clock timer used below

#define N \
    100000000    // => co-23: 100M floats -- large enough that a per-element speedup
                 // shows in wall time
#define TRIALS 5 // => co-25: best-of-5 -- shared-machine noise smoothing

static double now_seconds(void) {                        // => co-25: shared wall-clock helper, this topic's standard pattern
    struct timespec ts;                                  // supporting statement for this example
    clock_gettime(CLOCK_MONOTONIC, &ts);                 // calls clock_gettime(...)
    return (double)ts.tv_sec + (double)ts.tv_nsec / 1e9; // returns the computed result
}

// co-23: scalar baseline -- one float add per iteration, one element at a time.
// `salt` is added once at the end -- see the comment on scalar_add's caller for
// why (VERIFIED CAVEAT from ex-47: without a per-call distinguishing value,
// -O3's global-value-numbering proves repeated calls with unchanged inputs are
// redundant and silently reuses ONE cached result across a best-of-N trials
// loop).
__attribute__((noinline)) static float scalar_add(const float *a, const float *b, float *c,
                                                  int n,        // calls __attribute__(...)
                                                  float salt) { // supporting statement for this example
                                                                // co-23: vectorize(disable) is REQUIRED here -- elementwise float add has no
                                                                // reduction-associativity hazard, so clang's auto-vectorizer happily turns
                                                                // this "scalar" loop into NEON too at -O2 (verified: without this pragma,
                                                                // both functions measured identically fast, hiding the entire point of this
                                                                // example).
#pragma clang loop vectorize(disable) interleave(disable)       // supporting statement for this example
    for (int i = 0; i < n; i++)
        c[i] = a[i] + b[i]; // => co-23: one scalar `fadd` per element
    return c[0] + salt;     // => a cheap, distinguishing per-call return value
}

// co-23: hand-written NEON -- vld1q_f32 loads 4 floats into one 128-bit
// register, vaddq_f32 adds two such registers (4 adds in ONE instruction),
// vst1q_f32 stores the 4 results back -- this is EXACTLY what ex-47's
// auto-vectorizer does on its own for a reduction; here we do it explicitly for
// an ELEMENTWISE op instead.
__attribute__((noinline)) static float simd_add(const float *a, const float *b, float *c,
                                                int n,        // calls __attribute__(...)
                                                float salt) { // supporting statement for this example
    int i = 0;                                                // declares i
    for (; i + 4 <= n; i += 4) {                              // => co-23: process 4 floats per iteration
        float32x4_t va = vld1q_f32(&a[i]);                    // => load 4 floats from a
        float32x4_t vb = vld1q_f32(&b[i]);                    // => load 4 floats from b
        float32x4_t vc = vaddq_f32(va, vb);                   // => 4 adds in ONE NEON instruction
        vst1q_f32(&c[i], vc);                                 // => store all 4 results at once
    }
    for (; i < n; i++)
        c[i] = a[i] + b[i]; // => co-23: scalar tail for n not a multiple of 4
    return c[0] + salt;     // returns the computed result
}

int main(void) {                                   // program entry point
    float *a = malloc((size_t)N * sizeof(float));  // heap-allocates memory for a
    float *b = malloc((size_t)N * sizeof(float));  // heap-allocates memory for b
    float *c1 = malloc((size_t)N * sizeof(float)); // heap-allocates memory for c1
    float *c2 = malloc((size_t)N * sizeof(float)); // heap-allocates memory for c2
    if (!a || !b || !c1 || !c2) {
        fprintf(stderr, "alloc failed\n");
        return 1;
    } // prints a report line
    srand(21);                                 // calls srand(...)
    for (int i = 0; i < N; i++) {              // loop header controlling the sweep below
        a[i] = (float)(rand() % 1000) * 0.01f; // assigns a[i]
        b[i] = (float)(rand() % 1000) * 0.01f; // assigns b[i]
    }

    double best_scalar = 1e18, best_simd = 1e18; // declares best_scalar
    for (int t = 0; t < TRIALS; t++) {           // => co-25: best-of-N -- keep the fastest clean run
        double t0 = now_seconds();               // declares t0
        scalar_add(a, b, c1, N,
                   (float)t);      // => co-25: salt = t -- distinguishes every call
        double t1 = now_seconds(); // declares t1
        if (t1 - t0 < best_scalar)
            best_scalar = t1 - t0; // conditional check

        double t2 = now_seconds();       // declares t2
        simd_add(a, b, c2, N, (float)t); // calls simd_add(...)
        double t3 = now_seconds();       // declares t3
        if (t3 - t2 < best_simd)
            best_simd = t3 - t2; // conditional check
    }

    int mismatches = 0;           // => co-23: correctness check -- outputs must MATCH
    for (int i = 0; i < N; i++) { // loop header controlling the sweep below
        if (c1[i] != c2[i])
            mismatches++; // => float add is deterministic per-element, no
    } //    reordering risk here (elementwise, not a reduction)

    printf("N=%d floats, best of %d\n", N, TRIALS); // prints a report line
    printf("scalar: %.4f s\n", best_scalar);        // prints a report line
    printf("NEON:   %.4f s\n", best_simd);          // prints a report line
    double speedup = best_scalar / best_simd;       // declares speedup
    printf("mismatches: %d, speedup: %.2fx -> %s\n", mismatches,
           speedup,                                                                                          // prints a report line
           (mismatches == 0 && speedup > 1.1) ? "PASS (identical output, NEON measurably faster)" : "FAIL"); // continues the printf(...) call above
    free(a);                                                                                                 // releases a's heap memory
    free(b);                                                                                                 // releases b's heap memory
    free(c1);                                                                                                // releases c1's heap memory
    free(c2);                                                                                                // releases c2's heap memory
    return (mismatches == 0 && speedup > 1.1) ? 0 : 1;                                                       // returns the computed result
}
