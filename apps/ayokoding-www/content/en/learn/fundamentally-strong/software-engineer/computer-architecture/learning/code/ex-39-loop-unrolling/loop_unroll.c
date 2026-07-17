// learning/code/ex-39-loop-unrolling/loop_unroll.c
/* Example 39: unroll a single-accumulator reduction loop 8x -- verify higher
   throughput than the rolled loop (co-20, co-22). */
#include <stdio.h>  // => printf -- the timing/PASS report this program prints
#include <stdlib.h> // => malloc/free -- the array being reduced
#include <time.h>   // => clock_gettime -- the portable wall-clock timer used below

#define N \
    200000000    // => co-20: 200M elements -- N is a multiple of 8, no remainder
                 // handling needed
#define TRIALS 3 // => co-25: best-of-3 -- shared-machine noise smoothing

static double now_seconds(void) {                        // => co-25: shared wall-clock helper, this topic's standard pattern
    struct timespec ts;                                  // supporting statement for this example
    clock_gettime(CLOCK_MONOTONIC, &ts);                 // calls clock_gettime(...)
    return (double)ts.tv_sec + (double)ts.tv_nsec / 1e9; // returns the computed result
}

// co-20: the ROLLED loop -- one `cmp`, one conditional branch, one index
// increment, and one add PER element. `vectorize/unroll(disable)` stops clang's
// own optimizer from doing this example's job for it, so the measured gap below
// is really about OUR manual unrolling, not the auto-vectorizer (that
// comparison belongs to ex-47).
static long sum_rolled(const int *arr,
                       int n) {                       // defines sum_rolled(): helper function used by this example
    long sum = 0;                                     // declares sum
#pragma clang loop vectorize(disable) unroll(disable) // supporting statement for this example
    for (int i = 0; i < n; i++) {                     // loop header controlling the sweep below
        sum += arr[i];                                // => co-20: 1 add's worth of USEFUL work per iteration,
    } //    but paired with a full cmp+branch+increment
    return sum; // returns the computed result
}

// co-20: manually UNROLLED 8x, still ONE accumulator (the dependency chain is
// NOT broken -- each `sum +=` still depends on the previous one) -- the only
// thing that changes is the loop-control overhead: one cmp+branch+increment now
// covers EIGHT adds instead of one, so co-22's superscalar front-end has less
// bookkeeping to issue per unit of useful work, even though the adds themselves
// stay serialized.
static long sum_unrolled8(const int *arr,
                          int n) {                    // defines sum_unrolled8(): helper function used by this example
    long sum = 0;                                     // declares sum
#pragma clang loop vectorize(disable) unroll(disable) // supporting statement for this example
    for (int i = 0; i < n; i += 8) {                  // => co-20: ONE cmp+branch+increment per 8 elements
        sum += arr[i];                                // => co-20: still a single serial chain of 8 adds --
        sum += arr[i + 1];                            //    ONLY the loop-control cost shrank, not the
        sum += arr[i + 2];                            //    per-add latency (that's ex-40's job, not this one)
        sum += arr[i + 3];                            // updates sum
        sum += arr[i + 4];                            // updates sum
        sum += arr[i + 5];                            // updates sum
        sum += arr[i + 6];                            // updates sum
        sum += arr[i + 7];                            // updates sum
    }
    return sum; // returns the computed result
}

int main(void) {                                // program entry point
    int *arr = malloc((size_t)N * sizeof(int)); // heap-allocates memory for arr
    if (!arr) {
        fprintf(stderr, "alloc failed\n");
        return 1;
    } // prints a report line
    for (int i = 0; i < N; i++)
        arr[i] = (i % 7) - 3; // => small deterministic values, no overflow risk

    double best_rolled = 1e18, best_unrolled = 1e18; // declares best_rolled
    long sum_r = 0, sum_u = 0;                       // declares sum_r
    for (int t = 0; t < TRIALS; t++) {               // => co-25: best-of-N -- keep the fastest clean run
        double t0 = now_seconds();                   // declares t0
        sum_r = sum_rolled(arr, N);                  // assigns sum_r
        double t1 = now_seconds();                   // declares t1
        if (t1 - t0 < best_rolled)
            best_rolled = t1 - t0; // conditional check

        double t2 = now_seconds();     // declares t2
        sum_u = sum_unrolled8(arr, N); // assigns sum_u
        double t3 = now_seconds();     // declares t3
        if (t3 - t2 < best_unrolled)
            best_unrolled = t3 - t2; // conditional check
    }

    printf("rolled   sum=%ld, best of %d: %.4f s\n", sum_r, TRIALS,
           best_rolled); // prints a report line
    printf("unrolled sum=%ld, best of %d: %.4f s\n", sum_u, TRIALS,
           best_unrolled);                                                      // prints a report line
    double speedup = best_rolled / best_unrolled;                               // => co-20: how much the reduced loop overhead bought
    printf("unrolled is %.2fx faster -> %s\n", speedup,                         // prints a report line
           (sum_r == sum_u && speedup > 1.05)                                   // continues the printf(...) call above
               ? "PASS (identical sums, unrolled measurably higher throughput)" // continues
                                                                                // the
                                                                                // printf(...)
                                                                                // call
                                                                                // above
               : "FAIL");                                                       // continues the printf(...) call above
    free(arr);                                                                  // releases arr's heap memory
    return (sum_r == sum_u && speedup > 1.05) ? 0 : 1;                          // returns the computed result
}
