// learning/code/ex-24-temporal-locality-working-set/temporal_locality_working_set.c
/* Example 24: Temporal Locality Working Set -- small (L1-resident) vs large
 * (LLC-busting) sets, same total touches. */

#include <stdio.h>  // => co-04: printf -- reports both timings and the per-touch comparison
#include <stdlib.h> // => co-04: malloc/free -- both working-set buffers
#include <time.h>   // => co-25: clock_gettime -- wall-clock timing, per the shared brief

#define SMALL_INTS \
    (8u * 1024u / sizeof(int))                         // => co-04: 8 KiB working set -- comfortably
                                                       // resident in L1d (65536 B here)
#define LARGE_INTS (32u * 1024u * 1024u / sizeof(int)) // => co-04: 32 MiB working set -- far bigger than L2/LLC
#define TOTAL_TOUCHES \
    (100u * 1000u * 1000u) // => co-04: SAME total touch count for both cases -- a
                           // fair comparison
#define REPEATS 3          // => co-25: best-of-N, per DD-20

static double now_seconds(void) {                        // defines now_seconds(): helper function used by this example
    struct timespec ts;                                  // supporting statement for this example
    clock_gettime(CLOCK_MONOTONIC, &ts);                 // calls clock_gettime(...)
    return (double)ts.tv_sec + (double)ts.tv_nsec / 1e9; // returns the computed result
}

// ex-24: builds a random permutation of 0..count-1 -- RANDOM order matters here
// because SEQUENTIAL re-scans are so prefetcher/vectorizer-friendly that they
// hide temporal-locality effects entirely (verified empirically while building
// this example); random order is what actually exposes "does this fit in a
// cache level?"
static void make_permutation(size_t *perm, size_t count,
                             unsigned seed) { // defines make_permutation(): helper function
                                              // used by this example
    for (size_t i = 0; i < count; i++)
        perm[i] = i;                         // => co-04: start as the identity permutation
    srand(seed);                             // => co-04: FIXED seed -- makes this run reproducible
    for (size_t i = count - 1; i > 0; i--) { // => co-04: Fisher-Yates shuffle
        size_t j = (size_t)rand() % (i + 1); // => co-04: pick a random earlier-or-equal index
        size_t tmp = perm[i];
        perm[i] = perm[j];
        perm[j] = tmp; // => co-04: swap -- standard shuffle step
    }
}

// ex-24: repeatedly re-scans `buf` IN THE SAME RANDOM ORDER (`perm`) until
// TOTAL_TOUCHES individual reads have happened -- the small buffer's random
// order still gets FULLY cache-resident after the first pass (temporal
// locality: it fits), the large buffer's random order keeps evicting itself
// between passes (it does not)
static double time_repeated_random_scans(const int *buf, const size_t *perm,
                                         size_t count) {                     // defines time_repeated_random_scans(): helper function
                                                                             // used by this example
    volatile long sink = 0;                                                  // => co-04: volatile -- defeats dead-code elimination
    size_t touches_done = 0;                                                 // => co-04: counts individual element reads across all rescans
    double t0 = now_seconds();                                               // => co-25: start timer for this whole run
    while (touches_done < TOTAL_TOUCHES) {                                   // => co-04: keep rescanning until the
                                                                             // fixed touch budget is spent
        for (size_t i = 0; i < count && touches_done < TOTAL_TOUCHES; i++) { // => co-04: one full (or partial, at the end) rescan
            sink += buf[perm[i]];                                            // => co-04: THE probed read -- SAME random order
                                                                             // every rescan
            touches_done++;                                                  // => co-04: one more touch counted toward the fixed
                                                                             // budget
        }
    }
    (void)sink;                // => co-04: silences "unused" -- volatile already forced the reads
    return now_seconds() - t0; // => co-25: total elapsed time for exactly TOTAL_TOUCHES reads
}

int main(void) {                                              // program entry point
    int *small = malloc(SMALL_INTS * sizeof(int));            // => co-04: the L1-sized working set
    int *large = malloc(LARGE_INTS * sizeof(int));            // => co-04: the L2/LLC-busting working set
    size_t *small_perm = malloc(SMALL_INTS * sizeof(size_t)); // => co-04: random visiting order for the small set
    size_t *large_perm = malloc(LARGE_INTS * sizeof(size_t)); // => co-04: random visiting order for the large set
    if (!small || !large || !small_perm || !large_perm) {
        fprintf(stderr, "malloc failed\n");
        return 1;
    } // => co-04: defensive check
    for (size_t i = 0; i < SMALL_INTS; i++)
        small[i] = (int)i; // => co-04: fill the small buffer
    for (size_t i = 0; i < LARGE_INTS; i++)
        large[i] = (int)i; // => co-04: fill the large buffer
    make_permutation(small_perm, SMALL_INTS,
                     7); // => co-04: fixed seed 7 -- small set's random order
    make_permutation(large_perm, LARGE_INTS,
                     7); // => co-04: same seed -- large set's random order

    double small_best = 1e300, large_best = 1e300; // => co-25: best-of-N trackers
    for (int r = 0; r < REPEATS; r++) {            // => co-25: REPEATS runs, keep the fastest of each
        double t_small = time_repeated_random_scans(small, small_perm,
                                                    SMALL_INTS); // => co-04: TOTAL_TOUCHES reads, SMALL random order
        if (t_small < small_best)
            small_best = t_small; // => co-25: keep the fastest small-set run
        double t_large = time_repeated_random_scans(large, large_perm,
                                                    LARGE_INTS); // => co-04: TOTAL_TOUCHES reads, LARGE random order
        if (t_large < large_best)
            large_best = t_large; // => co-25: keep the fastest large-set run
    }

    double small_ns_per_touch = (small_best / TOTAL_TOUCHES) * 1e9; // => co-04: normalized to a per-touch cost
    double large_ns_per_touch = (large_best / TOTAL_TOUCHES) * 1e9; // => co-04: same normalization for the large set

    printf("small set (%zu ints, %zu B) best-of-%d = %.4f s, %.3f ns/touch\n",                                             // prints
                                                                                                                           // a
                                                                                                                           // report
                                                                                                                           // line
           (size_t)SMALL_INTS, (size_t)(SMALL_INTS * sizeof(int)), REPEATS, small_best, small_ns_per_touch);               // => co-04: small-set summary
    printf("large set (%zu ints, %zu MiB) best-of-%d = %.4f s, %.3f ns/touch\n",                                           // prints a report line
           (size_t)LARGE_INTS, (size_t)(LARGE_INTS * sizeof(int) / 1024 / 1024), REPEATS, large_best, large_ns_per_touch); // => co-04: large-set summary
    printf("large / small per-touch ratio = %.2fx\n",
           large_ns_per_touch / small_ns_per_touch); // => co-04: how much slower the large set is,
                                                     // per touch

    // ex-24: the claim -- for the SAME total number of touches, the small (L1-
    // resident) working set is measurably CHEAPER per touch than the large (LLC-
    // busting) working set, because re-scanning the small set keeps reusing data
    // that is still resident from the previous pass (temporal locality, co-04)
    int correct = (large_ns_per_touch > small_ns_per_touch * 1.2); // => co-04: a modest, honest threshold
    printf("%s\n", correct                                         // => co-04: PASS/FAIL verdict
                       ? "PASS: small (L1-resident) working set is measurably "
                         "faster per touch than the large one" // supporting
                                                               // statement for
                                                               // this example
                       : "FAIL: small working set was not measurably faster per "
                         "touch"); // supporting statement for this example

    free(small);
    free(large);
    free(small_perm);
    free(large_perm);       // => co-04: releases all four allocations
    return correct ? 0 : 1; // => co-04: nonzero exit on assertion failure
}
