// learning/code/ex-59-blocked-transpose/transpose.c
/* Example 59: naive vs cache-blocked matrix transpose. */
#include <stdio.h>  // stdio.h: standard library header
#include <stdlib.h> // stdlib.h: standard library header
#include <time.h>   // time.h: standard library header

#define N \
    2048 // => co-03: 2048x2048 int matrix = 16 MB -- bigger than this machine's 4
         // MiB L2
#define BLOCK \
    32 // => co-03: 32x32 int tile = 4 KB -- comfortably fits alongside other
       // tiles in L1d

// ex-59: naive transpose -- reads `src` row-major (sequential, cache-friendly)
// but WRITES `dst` column-major (stride N*4 bytes between consecutive writes --
// co-03: every write is a fresh cache line, and for N=2048 the write stream
// revisits each line only once every N iterations, so nothing stays resident
// long enough to be reused)
static void transpose_naive(const int *src, int *dst,
                            int n) {         // defines transpose_naive(): helper function used by this example
    for (int i = 0; i < n; i++) {            // => co-03: row-major read of src -- good locality
        for (int j = 0; j < n; j++) {        // loop header controlling the sweep below
            dst[j * n + i] = src[i * n + j]; // => co-03: dst write strides by n*4 bytes -- bad locality
        }
    }
}

// ex-59: cache-blocked transpose -- processes the matrix in BLOCK x BLOCK
// tiles, so both the read tile and the write tile stay resident in L1d for the
// whole inner block instead of streaming through the full 16 MB matrix
// column-by-column
static void transpose_blocked(const int *src, int *dst, int n,
                              int block) {               // defines transpose_blocked(): helper function
                                                         // used by this example
    for (int ii = 0; ii < n; ii += block) {              // => co-03: outer loop over tile rows
        for (int jj = 0; jj < n; jj += block) {          // => co-03: outer loop over tile columns
            int i_max = ii + block < n ? ii + block : n; // => clamp the last tile if n isn't a multiple
            int j_max = jj + block < n ? jj + block : n; // declares j_max
            for (int i = ii; i < i_max; i++) {           // => co-03: inner loops stay INSIDE one tile --
                for (int j = jj; j < j_max; j++) {       // both src and dst touches land in the same
                    dst[j * n + i] = src[i * n + j];     // small hot region for the whole tile's work
                }
            }
        }
    }
}

// ex-59: a shared timing harness so BOTH kernels are measured through the
// identical best-of-N loop -- taking the minimum of several trials, not the
// mean, is what filters out one-off OS scheduling noise without also hiding a
// real, reproducible difference between the two kernels.
static double best_of(void (*fn)(const int *, int *, int, int), const int *src, int *dst, int n, // declares function pointer fn
                      int block, int trials) {                                                   // declares block
    double best = -1.0;                                                                          // declares best
    for (int t = 0; t < trials; t++) {                                                           // loop header controlling the sweep below
        struct timespec t0, t1;                                                                  // supporting statement for this example
        clock_gettime(CLOCK_MONOTONIC, &t0);                                                     // calls clock_gettime(...)
        fn(src, dst, n, block);                                                                  // calls fn(...)
        clock_gettime(CLOCK_MONOTONIC, &t1);                                                     // calls clock_gettime(...)
        double secs = (t1.tv_sec - t0.tv_sec) + (t1.tv_nsec - t0.tv_nsec) / 1e9;                 // declares secs
        if (best < 0 || secs < best)
            best = secs; // conditional check
    }
    return best; // returns the computed result
}

// ex-59: best_of() takes a function pointer matching transpose_blocked's
// 4-argument signature, but transpose_naive only takes 3 -- this thin wrapper
// adapts the naive kernel to that same signature so both kernels can be driven
// through ONE shared timing loop instead of two.
static void naive_wrap(const int *src, int *dst, int n,
                       int block) { // defines naive_wrap(): helper function used by this example
    (void)block;                    // => naive ignores the block-size argument -- unused on purpose
    transpose_naive(src, dst, n);   // calls transpose_naive(...)
}

// ex-59: main() allocates the three N x N buffers once, times each kernel via
// best_of(), then checks TWO independent correctness signals -- a full
// element-by-element diff between the two kernels' outputs, and a sampled
// direct check of the transpose property against the source -- before ever
// looking at which kernel ran faster, so a wrong-but-fast kernel can't sneak a
// PASS.
int main(void) {                                            // program entry point
    int *src = malloc(sizeof(int) * (size_t)N * N);         // heap-allocates memory for src
    int *dst_naive = malloc(sizeof(int) * (size_t)N * N);   // heap-allocates memory for dst_naive
    int *dst_blocked = malloc(sizeof(int) * (size_t)N * N); // heap-allocates memory for dst_blocked
    if (!src || !dst_naive || !dst_blocked) {
        fprintf(stderr, "alloc failed\n");
        return 1;
    } // prints a report line

    for (int i = 0; i < N * N; i++)
        src[i] = i; // => deterministic content: src[i*N+j] == i*N+j

    double naive_secs = best_of(naive_wrap, src, dst_naive, N, BLOCK, 3); // declares naive_secs
    double blocked_secs = best_of(transpose_blocked, src, dst_blocked, N, BLOCK,
                                  3); // declares blocked_secs

    int mismatches = 0;               // => co-03: correctness check -- both outputs must be IDENTICAL
    for (int i = 0; i < N * N; i++) { // loop header controlling the sweep below
        if (dst_naive[i] != dst_blocked[i])
            mismatches++; // conditional check
    }
    // spot-check the transpose property directly: dst[j*N+i] must equal
    // src[i*N+j]
    int property_ok = 1;                   // declares property_ok
    for (int i = 0; i < N; i += 511) {     // sample a handful of rows, not all 2048 (keeps output short)
        for (int j = 0; j < N; j += 511) { // loop header controlling the sweep below
            if (dst_blocked[j * N + i] != src[i * N + j])
                property_ok = 0; // conditional check
        }
    }

    printf("matrix: %dx%d int (%.1f MB), block=%d (%.1f KB per tile)\n", N,
           N, // prints a report line
           (double)(sizeof(int) * (size_t)N * N) / (1024.0 * 1024.0),
           BLOCK,                                           // continues the printf(...) call above
           (double)(sizeof(int) * BLOCK * BLOCK) / 1024.0); // continues the printf(...) call above
    printf("naive transpose:   best of 3 = %.4f s\n",
           naive_secs); // prints a report line
    printf("blocked transpose: best of 3 = %.4f s\n",
           blocked_secs); // prints a report line
    printf("outputs identical: %s (%d mismatches out of %d)\n",
           mismatches == 0 ? "yes" : "NO -- BUG",                            // prints a report line
           mismatches, N * N);                                               // continues the printf(...) call above
    printf("transpose property dst[j][i]==src[i][j] sampled-verified: %s\n", // prints
                                                                             // a
                                                                             // report
                                                                             // line
           property_ok ? "yes" : "NO -- BUG");                               // continues the printf(...) call above
    double speedup = naive_secs / blocked_secs;                              // declares speedup
    printf("speedup: %.2fx (PASS: blocked faster + correct) -> %s\n",
           speedup,                                                               // prints a report line
           (mismatches == 0 && property_ok && speedup > 1.05) ? "PASS" : "FAIL"); // continues the printf(...) call above

    free(src);         // releases src's heap memory
    free(dst_naive);   // releases dst_naive's heap memory
    free(dst_blocked); // releases dst_blocked's heap memory
    return 0;          // returns the computed result
}
