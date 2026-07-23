// learning/code/ex-71-loop-interchange/interchange.c
/* Example 71: loop interchange -- swapping matmul's j/k loop order for
 * locality. */
#include <stdio.h>  // stdio.h: standard library header
#include <stdlib.h> // stdlib.h: standard library header
#include <time.h>   // time.h: standard library header

#define N \
    768 // => co-03: 768x768 float matrix = 2.25 MB -- bigger than L1d, fits
        // alongside L2 traffic

// ex-71: naive `ijk` loop order for C = A*B (row-major storage, C[i][j] +=
// A[i][k]*B[k][j]). co-17: in the INNERMOST loop (over k), A[i][k] advances by
// 1 float (sequential -- good), but B[k][j] advances by N floats between
// iterations (co-03: a full-row stride -- a NEW cache line almost every step,
// and that line is not reused again until the WHOLE next row of C is computed).
static void matmul_ijk(const float *a, const float *b, float *c,
                       int n) {                     // defines matmul_ijk(): helper function used by this example
    for (int i = 0; i < n; i++) {                   // loop header controlling the sweep below
        for (int j = 0; j < n; j++) {               // loop header controlling the sweep below
            float sum = 0.0f;                       // declares sum
            for (int k = 0; k < n; k++) {           // => co-03: innermost loop strides B by N floats -- BAD
                sum += a[i * n + k] * b[k * n + j]; // updates sum
            }
            c[i * n + j] = sum; // supporting statement for this example
        }
    }
}

// ex-71: INTERCHANGED `ikj` loop order -- same three loops, same total
// multiply-adds, ONLY the nesting order of j and k is swapped. co-03: now the
// innermost loop (over j) walks B[k][j] AND c[i][j] both sequentially (unit
// stride), while a[i*n+k] is loop-invariant across the whole j loop (the
// compiler hoists it into a register) -- co-17: this is the textbook
// loop-interchange win.
static void matmul_ikj(const float *a, const float *b, float *c,
                       int n) {   // defines matmul_ikj(): helper function used by this example
    for (int i = 0; i < n; i++) { // loop header controlling the sweep below
        for (int j = 0; j < n; j++)
            c[i * n + j] = 0.0f;                     // => must zero-init: this order accumulates INTO c across k
        for (int k = 0; k < n; k++) {                // loop header controlling the sweep below
            float a_ik = a[i * n + k];               // => co-03: loop-invariant across the j loop
                                                     // below -- loaded ONCE per k
            for (int j = 0; j < n; j++) {            // => co-03: innermost loop strides B AND C by 1 float -- GOOD
                c[i * n + j] += a_ik * b[k * n + j]; // supporting statement for this example
            }
        }
    }
}

// ex-71: a single-trial timer shared by both loop orders -- both matmul_ijk and
// matmul_ikj match this exact function-pointer signature, so one small driver
// measures either kernel without duplicating the clock_gettime bookkeeping for
// each order separately.
static double time_matmul(void (*fn)(const float *, const float *, float *, int),
                          const float *a,                             // declares function pointer fn
                          const float *b, float *c, int n) {          // declares b
    struct timespec t0, t1;                                           // supporting statement for this example
    clock_gettime(CLOCK_MONOTONIC, &t0);                              // calls clock_gettime(...)
    fn(a, b, c, n);                                                   // calls fn(...)
    clock_gettime(CLOCK_MONOTONIC, &t1);                              // calls clock_gettime(...)
    return (t1.tv_sec - t0.tv_sec) + (t1.tv_nsec - t0.tv_nsec) / 1e9; // returns the computed result
}

// ex-71: main() runs identical A/B inputs through both loop orders into
// SEPARATE output buffers, times each order once, then diffs the two outputs
// before trusting the timing -- loop interchange only reorders arithmetic, so a
// real bug would show up as a nonzero diff.
int main(void) {                                          // program entry point
    float *a = malloc(sizeof(float) * (size_t)N * N);     // heap-allocates memory for a
    float *b = malloc(sizeof(float) * (size_t)N * N);     // heap-allocates memory for b
    float *c_ijk = malloc(sizeof(float) * (size_t)N * N); // heap-allocates memory for c_ijk
    float *c_ikj = malloc(sizeof(float) * (size_t)N * N); // heap-allocates memory for c_ikj
    if (!a || !b || !c_ijk || !c_ikj) {
        fprintf(stderr, "alloc failed\n");
        return 1;
    } // prints a report line

    unsigned seed = 3u;                     // declares seed
    for (int i = 0; i < N * N; i++) {       // loop header controlling the sweep below
        seed = seed * 1103515245u + 12345u; // assigns seed
        a[i] = (float)(seed % 10u) * 0.1f;  // assigns a[i]
        seed = seed * 1103515245u + 12345u; // assigns seed
        b[i] = (float)(seed % 10u) * 0.1f;  // assigns b[i]
    }

    double t_ijk = time_matmul(matmul_ijk, a, b, c_ijk, N); // declares t_ijk
    double t_ikj = time_matmul(matmul_ikj, a, b, c_ikj, N); // declares t_ikj

    double max_diff = 0.0;                              // => co-17: both orders compute the SAME mathematical result
    for (int i = 0; i < N * N; i++) {                   // loop header controlling the sweep below
        double d = (double)c_ijk[i] - (double)c_ikj[i]; // declares d
        if (d < 0)
            d = -d; // conditional check
        if (d > max_diff)
            max_diff = d; // conditional check
    }

    printf("matmul: %dx%d float matrices (%.2f MB each)\n", N, N,
           (double)(sizeof(float) * N * N) / (1024.0 * 1024.0)); // prints a report line
    printf("ijk order (B strides by N in innermost loop): %.4f s\n",
           t_ijk); // prints a report line
    printf("ikj order (B, C sequential in innermost loop): %.4f s\n",
           t_ikj); // prints a report line
    printf("max |c_ijk - c_ikj| difference: %.6f\n",
           max_diff);               // prints a report line
    double speedup = t_ijk / t_ikj; // declares speedup
    printf("speedup: %.2fx (PASS: ikj faster + numerically equal) -> %s\n",
           speedup,                                                // prints a report line
           (max_diff < 0.01 && speedup > 1.05) ? "PASS" : "FAIL"); // continues the printf(...) call above

    free(a);
    free(b);
    free(c_ijk);
    free(c_ikj); // releases a's heap memory
    return 0;    // returns the computed result
}
