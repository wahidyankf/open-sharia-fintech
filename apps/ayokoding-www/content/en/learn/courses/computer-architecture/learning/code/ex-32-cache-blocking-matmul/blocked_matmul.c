// learning/code/ex-32-cache-blocking-matmul/blocked_matmul.c
// Example 32: naive triple-loop matmul vs a cache-blocked/tiled version --
// verify identical results and the tiled version measurably faster (co-03,
// co-25).
#include <stdio.h>  // => co-25: printf -- the timing/PASS report this program prints
#include <stdlib.h> // => co-03: malloc/free -- all three N x N matrices are heap-allocated
#include <time.h>   // => co-25: clock_gettime -- the portable wall-clock timer used below

#define N \
    512 // => co-03: 512x512 doubles = 2 MiB per matrix -- A+B+C don't fit in L2
        // (4 MiB)
#define BLOCK \
    64            // => co-03: tile edge -- a 64x64 double tile is 32 KiB, fits comfortably
                  // in L1d
#define REPEATS 3 // => co-25: best-of-3 -- shared-machine noise smoothing (DD-20 step 2)

static double now_seconds(void) { // => co-25: same portable clock_gettime timer used across this tier
    struct timespec ts;           // => co-25: POSIX timespec, seconds + nanoseconds fields
    clock_gettime(CLOCK_MONOTONIC,
                  &ts);                                  // => co-25: monotonic -- immune to wall-clock adjustment mid-run
    return (double)ts.tv_sec + (double)ts.tv_nsec / 1e9; // => co-25: combined into one double-seconds value
}

// => co-03: naive C[i][j] = sum_k A[i][k]*B[k][j] -- for FIXED i,j the inner k
// => loop strides through B COLUMN-wise, touching a new cache line almost every
// step
static void matmul_naive(const double *a, const double *b, double *c,
                         int n) {                   // defines matmul_naive(): helper function used by this example
    for (int i = 0; i < n; i++) {                   // => co-03: rows of A/C
        for (int j = 0; j < n; j++) {               // => co-03: columns of B/C
            double sum = 0.0;                       // => co-03: accumulator for C[i][j]
            for (int k = 0; k < n; k++) {           // => co-03: dot product of A's row i and B's column j
                sum += a[i * n + k] * b[k * n + j]; // => co-03: a[i][k] sequential,
                                                    // b[k][j] strided by n doubles
            } // => co-03: k=0..n-1 means b's column touches n DIFFERENT cache lines
            c[i * n + j] = sum; // => co-03: write the finished dot product into C
        } // => co-03: next column j -- b's whole n*n footprint is walked AGAIN
    }
}

// => co-03: same math, tiled into BLOCK x BLOCK sub-matrices so each tile of
// => A, B, and C stays resident in L1/L2 while it is being reused repeatedly
static void matmul_blocked(const double *a, const double *b, double *c,
                           int n) { // defines matmul_blocked(): helper function used by this example
    for (int i = 0; i < n; i++)     // => co-03: C must still be zeroed -- blocking
                                    // only reorders accumulation
        for (int j = 0; j < n; j++)
            c[i * n + j] = 0.0;                     // => co-03: start every output cell at zero before
                                                    // accumulating tiles
    for (int ii = 0; ii < n; ii += BLOCK) {         // => co-03: outer tile loop over row-blocks of A/C
        for (int jj = 0; jj < n; jj += BLOCK) {     // => co-03: outer tile loop over column-blocks of B/C
            for (int kk = 0; kk < n; kk += BLOCK) { // => co-03: outer tile loop over
                                                    // the shared reduction dimension
                // => co-03: this INNER triple loop is the same naive kernel, just
                // => confined to one BLOCK x BLOCK x BLOCK cube -- small enough to stay
                // cached
                for (int i = ii; i < ii + BLOCK; i++) {         // => co-03: within-tile row -- BLOCK=64 rows per outer tile
                                                                // step
                    for (int j = jj; j < jj + BLOCK; j++) {     // => co-03: within-tile column -- BLOCK=64 columns per
                                                                // outer tile step
                        double sum = c[i * n + j];              // => co-03: resume accumulating THIS cell across k-tiles
                        for (int k = kk; k < kk + BLOCK; k++) { // => co-03: within-tile reduction -- only BLOCK terms
                                                                // per (ii,jj,kk) pass
                            sum += a[i * n + k] * b[k * n + j]; // => co-03: identical arithmetic to the
                                                                // naive kernel, tile-local
                        } // => co-03: this k-tile's contribution to c[i][j] is now folded
                          // in
                        c[i * n + j] = sum; // => co-03: write back the partial sum for this k-tile
                    } // => co-03: next column within this (ii,jj,kk) tile
                } // => co-03: next row within this (ii,jj,kk) tile
            }
        }
    }
}

// ex-32: main() ties both kernels together -- allocate once, run both REPEATS
// times, diff their outputs for correctness, and only THEN compare timings, so
// a speed win never masks a wrong answer.
int main(void) {                                                // => co-25: single self-contained process -- both kernels run in it
    double *a = malloc((size_t)N * N * sizeof(double));         // => co-03: 2 MiB input matrix A
    double *b = malloc((size_t)N * N * sizeof(double));         // => co-03: 2 MiB input matrix B
    double *c_naive = malloc((size_t)N * N * sizeof(double));   // => co-03: 2 MiB output for the naive kernel
    double *c_blocked = malloc((size_t)N * N * sizeof(double)); // => co-03: 2 MiB output for the blocked kernel
    if (!a || !b || !c_naive || !c_blocked) {
        fprintf(stderr, "alloc failed\n");
        return 1;
    } // => co-25: fail loudly

    for (int i = 0; i < N * N; i++) {         // => co-01: fill A and B once with deterministic values
        a[i] = (double)((i * 7) % 13) - 6.0;  // => co-01: arbitrary but deterministic -- content doesn't matter
        b[i] = (double)((i * 11) % 17) - 8.0; // => co-01: different formula so A != B
    } // => co-01: both matrices fully touched once, before any timed pass

    double best_naive = 1e18,
           best_blocked = 1e18;         // => co-25: track the FASTEST of REPEATS runs per kernel
    for (int r = 0; r < REPEATS; r++) { // => co-25: re-run to confirm the result reproduces
        double t0 = now_seconds();      // => co-25: start the clock for this naive pass
        matmul_naive(a, b, c_naive,
                     N);           // => co-03: the cache-hostile, unblocked kernel
        double t1 = now_seconds(); // => co-25: stop the clock for this naive pass
        if (t1 - t0 < best_naive)
            best_naive = t1 - t0; // => co-25: keep the best naive timing so far

        double t2 = now_seconds(); // => co-25: start the clock for this blocked pass
        matmul_blocked(a, b, c_blocked,
                       N);         // => co-03: the SAME math, tiled for cache reuse
        double t3 = now_seconds(); // => co-25: stop the clock for this blocked pass
        if (t3 - t2 < best_blocked)
            best_blocked = t3 - t2; // => co-25: keep the best blocked timing so far
    }

    double max_diff = 0.0;                       // => co-03: largest per-cell difference between the
                                                 // two kernels' outputs
    for (int i = 0; i < N * N; i++) {            // => co-03: scan every one of the N*N result cells
        double diff = c_naive[i] - c_blocked[i]; // => co-03: exact double arithmetic --
                                                 // blocking changes ORDER, not values here
        if (diff < 0)
            diff = -diff; // => co-03: absolute difference
        if (diff > max_diff)
            max_diff = diff; // => co-03: track the worst-case mismatch across all cells
    } // => co-03: max_diff over all N*N cells is this run's correctness verdict

    printf("naive:   best of %d: %.4f s\n", REPEATS,
           best_naive); // => co-25: methodology stated in the output
    printf("blocked: best of %d: %.4f s\n", REPEATS,
           best_blocked); // => co-25: methodology stated in the output
    printf("max |naive - blocked| difference: %.2e\n",
           max_diff);                           // => co-03: near-zero proves the tiling didn't change the
                                                // answer
    double speedup = best_naive / best_blocked; // => co-03: how many times faster
                                                // the tiled version really was
    int correct = max_diff < 1e-9;              // => co-03: both use double, same summation
                                                // order per cell -- expect exact match
    printf("blocked is %.2fx faster -> %s\n",
           speedup,                     // => co-25: prints the ratio the reader should verify against
                                        // below
           (correct && speedup > 1.1) ? // => co-03: correctness (near-zero diff) AND speed both gate the
                                        // PASS
               "PASS (identical results, blocking measurably faster)"
                                      : // => co-25: the program judges its own claim, per DD-20
               "FAIL");                 // => co-25: an honest FAIL label if either condition fails
    free(a);
    free(b);
    free(c_naive);
    free(c_blocked);                           // => co-03: release all four 2 MiB matrices before exiting
    return (correct && speedup > 1.1) ? 0 : 1; // => co-25: real process exit code reflecting the PASS/FAIL
}
