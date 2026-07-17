// learning/code/ex-40-ilp-multiple-accumulators/ilp_accumulators.c
/* Example 40: sum a large array with 1 accumulator vs 4 accumulators --
   verify the 4-accumulator version is faster because it breaks the
   dependency chain (co-22). */
#include <stdio.h>  // => printf -- the timing/PASS report this program prints
#include <stdlib.h> // => malloc/free -- the array being reduced
#include <time.h>   // => clock_gettime -- the portable wall-clock timer used below

#define N \
    200000000    // => co-22: 200M elements, a multiple of 4 -- no remainder handling
                 // needed
#define TRIALS 3 // => co-25: best-of-3 -- shared-machine noise smoothing

static double now_seconds(void) {                        // => co-25: shared wall-clock helper, this topic's standard pattern
    struct timespec ts;                                  // supporting statement for this example
    clock_gettime(CLOCK_MONOTONIC, &ts);                 // calls clock_gettime(...)
    return (double)ts.tv_sec + (double)ts.tv_nsec / 1e9; // returns the computed result
}

// co-22: ONE accumulator over a REAL array -- every `sum += arr[i]` must wait
// for the previous one to finish (co-20's dependency chain), so the add's
// latency (not its throughput) is the bottleneck, no matter how many execution
// ports this superscalar core has. `vectorize/unroll(disable)` isolates the ILP
// effect this example is about from clang's own auto-optimizations
// (ex-39/ex-47's job).
static long sum_1acc(const int *arr,
                     int n) {                         // defines sum_1acc(): helper function used by this example
    long sum = 0;                                     // declares sum
#pragma clang loop vectorize(disable) unroll(disable) // supporting statement for this example
    for (int i = 0; i < n; i++) {                     // loop header controlling the sweep below
        sum += arr[i];                                // => co-20: strictly serial -- add i+1 waits on add i
    }
    return sum; // returns the computed result
}

// co-22: FOUR accumulators over the SAME array -- sum0..sum3 have no dependency
// on each other, so a superscalar out-of-order core can execute several of
// these adds per cycle instead of waiting on one serial chain; only combined
// into one total at the very end, after the loop.
static long sum_4acc(const int *arr,
                     int n) { // defines sum_4acc(): helper function used by this example
    long sum0 = 0, sum1 = 0, sum2 = 0,
         sum3 = 0;                                    // => co-22: four independent partial sums
#pragma clang loop vectorize(disable) unroll(disable) // supporting statement for this example
    for (int i = 0; i < n; i += 4) {                  // => co-22: n/4 iterations, 4 elements consumed each
        sum0 += arr[i];                               // => co-22: these four adds are mutually independent --
        sum1 += arr[i + 1];                           //    the CPU can execute them concurrently
        sum2 += arr[i + 2];                           // updates sum2
        sum3 += arr[i + 3];                           // updates sum3
    }
    return sum0 + sum1 + sum2 + sum3; // => co-22: combined ONCE, after all chains finish
}

int main(void) {                                // program entry point
    int *arr = malloc((size_t)N * sizeof(int)); // heap-allocates memory for arr
    if (!arr) {
        fprintf(stderr, "alloc failed\n");
        return 1;
    } // prints a report line
    for (int i = 0; i < N; i++)
        arr[i] = (i % 5) - 2; // => small deterministic values, no overflow risk

    double best_1acc = 1e18, best_4acc = 1e18; // declares best_1acc
    long sum_1 = 0, sum_4 = 0;                 // declares sum_1
    for (int t = 0; t < TRIALS; t++) {         // => co-25: best-of-N -- keep the fastest clean run
        double t0 = now_seconds();             // declares t0
        sum_1 = sum_1acc(arr, N);              // assigns sum_1
        double t1 = now_seconds();             // declares t1
        if (t1 - t0 < best_1acc)
            best_1acc = t1 - t0; // conditional check

        double t2 = now_seconds(); // declares t2
        sum_4 = sum_4acc(arr, N);  // assigns sum_4
        double t3 = now_seconds(); // declares t3
        if (t3 - t2 < best_4acc)
            best_4acc = t3 - t2; // conditional check
    }

    printf("1 accumulator sum=%ld, best of %d: %.4f s\n", sum_1, TRIALS,
           best_1acc); // prints a report line
    printf("4 accumulator sum=%ld, best of %d: %.4f s\n", sum_4, TRIALS,
           best_4acc);                                                     // prints a report line
    double speedup = best_1acc / best_4acc;                                // => co-22: how much breaking the dependency bought
    printf("4-accumulator is %.2fx faster -> %s\n", speedup,               // prints a report line
           (sum_1 == sum_4 && speedup > 1.2)                               // continues the printf(...) call above
               ? "PASS (identical sums, 4 accumulators measurably faster)" // continues
                                                                           // the
                                                                           // printf(...)
                                                                           // call
                                                                           // above
               : "FAIL");                                                  // continues the printf(...) call above
    free(arr);                                                             // releases arr's heap memory
    return (sum_1 == sum_4 && speedup > 1.2) ? 0 : 1;                      // returns the computed result
}
