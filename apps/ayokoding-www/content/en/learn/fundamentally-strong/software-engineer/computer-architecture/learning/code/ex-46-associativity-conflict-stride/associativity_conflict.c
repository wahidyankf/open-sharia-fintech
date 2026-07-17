// learning/code/ex-46-associativity-conflict-stride/associativity_conflict.c
/* Example 46: column-sum a matrix whose row width is a large power of two
   vs the SAME matrix with a small padding offset -- verify the power-of-two
   stride's conflict misses cost measurably more (co-06). */
#include <stdio.h>  // => printf -- the timing/PASS report this program prints
#include <stdlib.h> // => malloc/free -- the two matrices under test
#include <time.h>   // => clock_gettime -- the portable wall-clock timer used below

#define ROWS 8000 // => co-06: enough rows for a stable timing signal
#define COLS_POW2 \
    1024 // => co-06: 1024 ints = 4096 B row stride -- a large
         //    POWER-OF-TWO stride, the classic conflict-miss trigger
         //    (every row's column-0 element lands on the SAME set
         //    modulo the cache's indexing, because the stride is an
         //    exact multiple of common power-of-two cache/set sizes;
         //    VERIFIED empirically: 4096 B produced the strongest,
         //    most reproducible conflict-miss signal on this machine
         //    among several power-of-two strides tried)
#define COLS_PADDED \
    (COLS_POW2 + 16) // => co-06: +16 ints (64 B) breaks the power-of-two
                     //    periodicity -- the standard, well-known fix
#define REPEATS \
    500 // => co-06: revisit column 0 this many times -- amplifies
        //    the conflict-miss signal (single pass alone is too fast)

static double now_seconds(void) {                        // => co-25: shared wall-clock helper, this topic's standard pattern
    struct timespec ts;                                  // supporting statement for this example
    clock_gettime(CLOCK_MONOTONIC, &ts);                 // calls clock_gettime(...)
    return (double)ts.tv_sec + (double)ts.tv_nsec / 1e9; // returns the computed result
}

// co-06: sums column 0 down ROWS rows, REPEATS times -- every element accessed
// is `row * cols` ints apart, so a power-of-two `cols` makes every access alias
// onto the same small set of cache lines/sets, regardless of the cache's total
// CAPACITY -- this is associativity pressure, not a capacity miss
// (co-01/co-05).
static long sum_column0(const int *mat, int rows, int cols,
                        int repeats) {      // defines sum_column0(): helper function
                                            // used by this example
    long total = 0;                         // declares total
    for (int r = 0; r < repeats; r++) {     // loop header controlling the sweep below
        for (int i = 0; i < rows; i++) {    // loop header controlling the sweep below
            total += mat[(size_t)i * cols]; // => co-06: stride = cols ints between accesses
        }
    }
    return total; // returns the computed result
}

int main(void) {                                                        // program entry point
    int *mat_pow2 = malloc((size_t)ROWS * COLS_POW2 * sizeof(int));     // heap-allocates memory for mat_pow2
    int *mat_padded = malloc((size_t)ROWS * COLS_PADDED * sizeof(int)); // heap-allocates memory for mat_padded
    if (!mat_pow2 || !mat_padded) {
        fprintf(stderr, "alloc failed\n");
        return 1;
    } // prints a report line

    for (long i = 0; i < (long)ROWS * COLS_POW2; i++)
        mat_pow2[i] = (int)(i % 251); // loop header controlling the sweep below
    for (long i = 0; i < (long)ROWS * COLS_PADDED; i++)
        mat_padded[i] = (int)(i % 251); // loop header controlling the sweep below

    double t0 = now_seconds();                                       // declares t0
    long sum_pow2 = sum_column0(mat_pow2, ROWS, COLS_POW2, REPEATS); // declares sum_pow2
    double t1 = now_seconds();                                       // declares t1
    long sum_padded = sum_column0(mat_padded, ROWS, COLS_PADDED,
                                  REPEATS); // declares sum_padded
    double t2 = now_seconds();              // declares t2

    double secs_pow2 = t1 - t0;   // declares secs_pow2
    double secs_padded = t2 - t1; // declares secs_padded
    printf("rows=%d, pow2 stride=%d ints (%zu B), padded stride=%d ints (%zu B), "
           "repeats=%d\n",
           ROWS, // prints a report line
           COLS_POW2, (size_t)COLS_POW2 * sizeof(int), COLS_PADDED,
           (size_t)COLS_PADDED * sizeof(int), // continues the printf(...) call above
           REPEATS);                          // continues the printf(...) call above
    printf("power-of-two stride: sum=%ld, %.4f s\n", sum_pow2,
           secs_pow2); // prints a report line
    printf("padded stride:       sum=%ld, %.4f s\n", sum_padded,
           secs_padded);                    // prints a report line
    double ratio = secs_pow2 / secs_padded; // => co-06: how much the power-of-two conflict costs
    printf("power-of-two/padded ratio: %.2fx -> %s\n",
           ratio, // prints a report line
           ratio > 1.15 ? "PASS (conflict-miss spike measurably costs more at "
                          "the critical stride)"
                        : "FAIL"); // continues the printf(...) call above
    free(mat_pow2);                // releases mat_pow2's heap memory
    free(mat_padded);              // releases mat_padded's heap memory
    return ratio > 1.15 ? 0 : 1;   // returns the computed result
}
