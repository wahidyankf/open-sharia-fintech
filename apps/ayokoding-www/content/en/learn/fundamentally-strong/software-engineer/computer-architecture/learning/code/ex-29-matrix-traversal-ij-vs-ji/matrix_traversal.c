// learning/code/ex-29-matrix-traversal-ij-vs-ji/matrix_traversal.c
// Example 29: sum a large row-major int matrix [i][j] (sequential) vs [j][i]
// (strided) and verify [i][j] is measurably faster (co-03, co-17).
#include <stdio.h>  // => co-25: printf -- the timing/PASS report this program prints
#include <stdlib.h> // => co-17: malloc/free -- the one 64 MiB matrix both traversals share
#include <time.h>   // => co-25: clock_gettime -- the portable wall-clock timer used below

#define N \
    4096          // => co-17: 4096x4096 ints = 64 MiB -- far bigger than this machine's 4
                  // MiB L2
#define REPEATS 3 // => co-25: best-of-3 -- shared-machine noise smoothing (DD-20 step 2)
// => co-25: this program's own PASS/FAIL line is the assertion -- no external
// => test harness is needed to confirm the claim this example makes

static double now_seconds(void) {                        // => co-25: same portable clock_gettime timer used across this tier
    struct timespec ts;                                  // => co-25: POSIX timespec, seconds + nanoseconds fields
    clock_gettime(CLOCK_MONOTONIC, &ts);                 // => co-25: monotonic -- immune to
                                                         // NTP/wall-clock adjustment mid-run
    return (double)ts.tv_sec + (double)ts.tv_nsec / 1e9; // => co-25: combined into one double-seconds
                                                         // value for subtraction
}

static long sum_row_major(int (*m)[N]) { // => co-17: m[i][j] is the pointer-to-array-of-N-ints layout
                                         // C actually uses
    // => co-03: "row-major" means row 0's N ints, then row 1's N ints, etc,
    // => laid out back to back -- C guarantees this for a plain 2-D array
    long total = 0;                   // => co-03: accumulator -- summed in the SAME order memory is laid out
    for (int i = 0; i < N; i++) {     // => co-03: outer loop over rows -- each row is N contiguous ints
        for (int j = 0; j < N; j++) { // => co-03: inner loop walks j sequentially WITHIN one row
            total += m[i][j];         // => co-03: address = base + i*N*4 + j*4 -- j+1 is the
                                      // VERY next int
        }
    }
    return total; // => co-03: identical mathematical sum to sum_col_major below
}

static long sum_col_major(int (*m)[N]) { // => co-17: SAME matrix, SAME memory layout --
                                         // only the loop nesting flips
    // => co-17: this is the classic "algorithm looks identical, performance
    // => doesn't" trap -- big-O is O(N^2) either way, but the constant differs
    // hugely
    long total = 0;                   // => co-17: accumulator -- summed in COLUMN order, against the grain
    for (int j = 0; j < N; j++) {     // => co-17: outer loop over columns now
        for (int i = 0; i < N; i++) { // => co-17: inner loop walks i -- each step jumps N*4 = 16 KiB
            total += m[i][j];         // => co-17: address = base + i*N*4 + j*4 -- i+1 skips a
                                      // whole row
        }
    }
    return total; // => co-17: same total as sum_row_major -- correctness is
                  // unaffected
}

int main(void) {                             // => co-25: single self-contained process -- both traversals
                                             // run in it
    int (*m)[N] = malloc(sizeof(int[N][N])); // => co-17: one 64 MiB row-major allocation,
                                             // shared by BOTH traversals
    if (m == NULL) {
        fprintf(stderr, "alloc failed\n");
        return 1;
    } // => co-25: fail loudly rather than time a null pointer
    for (int i = 0; i < N; i++)          // => co-01: fill once so page faults don't skew either timed pass
        for (int j = 0; j < N; j++)      // => co-01: touches every one of the 16M ints exactly once
            m[i][j] = (i * 31 + j) % 97; // => co-01: arbitrary deterministic values
                                         // -- content doesn't matter here

    double best_row = 1e18,
           best_col = 1e18;        // => co-25: track the FASTEST of REPEATS runs per
                                   // traversal, not the average
    long row_sum = 0, col_sum = 0; // => co-03: captured to prove both traversals
                                   // compute the SAME answer
    // => co-25: both traversals do the EXACT same 16M additions -- only the
    // => memory ACCESS PATTERN differs, isolating the layout effect from work
    // done
    for (int r = 0; r < REPEATS; r++) { // => co-25: re-run to confirm the result
                                        // reproduces, not a lucky sample
        double t0 = now_seconds();      // => co-25: time ONLY the traversal, not the setup above
        row_sum = sum_row_major(m);     // => co-03: the cache-friendly, sequential-access traversal
        double t1 = now_seconds();      // => co-25: stop the clock for the row-major pass
        if (t1 - t0 < best_row)
            best_row = t1 - t0; // => co-25: keep the best (least noisy) row-major timing so far

        double t2 = now_seconds();  // => co-25: start the clock for the column-major pass
        col_sum = sum_col_major(m); // => co-17: the SAME matrix, strided-access traversal
        double t3 = now_seconds();  // => co-25: stop the clock for the column-major pass
        if (t3 - t2 < best_col)
            best_col = t3 - t2; // => co-25: keep the best (least noisy) column-major
                                // timing so far
    }

    printf("row-major [i][j] sum: %ld, best of %d: %.4f s\n", row_sum, REPEATS,
           best_row); // => co-25: methodology stated in the output
    printf("col-major [j][i] sum: %ld, best of %d: %.4f s\n", col_sum, REPEATS,
           best_col);                     // => co-17: methodology stated in the output
    double speedup = best_col / best_row; // => co-03: how many times slower the
                                          // strided traversal really was
    printf("row-major is %.2fx faster -> %s\n",
           speedup,                                // => co-25: prints the ratio the reader should verify against
                                                   // below
           (row_sum == col_sum && speedup > 1.2) ? // => co-03: correctness (equal sums) AND speed both gate the PASS
               "PASS (identical sums, [i][j] measurably faster)"
                                                 :        // => co-25: the program judges its own claim, per DD-20
               "FAIL");                                   // => co-25: an honest FAIL label if either condition fails
    free(m);                                              // => co-17: release the 64 MiB matrix before exiting
    return (row_sum == col_sum && speedup > 1.2) ? 0 : 1; // => co-25: a real process exit code reflecting the PASS/FAIL
}
