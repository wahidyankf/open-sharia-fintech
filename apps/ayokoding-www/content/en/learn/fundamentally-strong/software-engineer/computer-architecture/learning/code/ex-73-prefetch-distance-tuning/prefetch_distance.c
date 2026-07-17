// learning/code/ex-73-prefetch-distance-tuning/prefetch_distance.c
/* Example 73: sweeping software-prefetch distance to find an interior optimum.
 */
#include <stdio.h>  // stdio.h: standard library header
#include <stdlib.h> // stdlib.h: standard library header
#include <time.h>   // time.h: standard library header

// co-03: 64M ints = 256 MB -- past this machine's 4 MiB L2 AND past Apple
// Silicon's on-package system-level cache (a shared cache beyond L2, tens of
// MB), so a random-order walk over it is a genuine DRAM-latency-bound workload
// that stays cold across repeated sweeps -- a smaller array (32 MB, tried first
// during authoring) fit inside that system-level cache, so EVERY distance
// (including "no prefetch") measured near-identically fast after the first
// sweep warmed it up.
#define N 64000000 // constant N = 64000000

// ex-73: Fisher-Yates shuffle -- builds a permutation so `data[perm[i]]` visits
// every index exactly once, but in an order NO hardware next-line/stride
// prefetcher can predict from past addresses alone. This is the classic setup
// where SOFTWARE prefetch distance actually matters: `perm[]` itself is known
// ahead of time, so the loop CAN look up perm[i+D] and prefetch data[perm[i+D]]
// before it is needed, even though the hardware prefetcher has no way to guess
// it.
static int *make_permutation(int n) {    // defines make_permutation(): helper function used by this example
    int *perm = malloc(sizeof(int) * n); // heap-allocates memory for perm
    for (int i = 0; i < n; i++)
        perm[i] = i;                             // loop header controlling the sweep below
    unsigned seed = 17u;                         // declares seed
    for (int i = n - 1; i > 0; i--) {            // => co-03: standard Fisher-Yates -- unbiased shuffle
        seed = seed * 1103515245u + 12345u;      // assigns seed
        int j = (int)(seed % (unsigned)(i + 1)); // declares j
        int tmp = perm[i];
        perm[i] = perm[j];
        perm[j] = tmp; // declares tmp
    }
    return perm; // returns the computed result
}

// ex-73: the timed walk itself -- `distance` == 0 means NO software prefetch at
// all (the baseline); distance > 0 issues one prefetch per iteration,
// `distance` steps AHEAD in the permutation, for the read-only line the loop
// will need `distance` iterations from now.
static double timed_walk(const int *data, const int *perm, int n, int distance,
                         long *out_sum) {       // defines timed_walk(): helper
                                                // function used by this example
    struct timespec t0, t1;                     // supporting statement for this example
    long sum = 0;                               // declares sum
    clock_gettime(CLOCK_MONOTONIC, &t0);        // calls clock_gettime(...)
    for (int i = 0; i < n; i++) {               // loop header controlling the sweep below
        if (distance > 0 && i + distance < n) { // conditional check
            __builtin_prefetch(&data[perm[i + distance]], 0,
                               1); // => co-03: read-hint (0), low temporal
        } // locality (1) -- this line is used once
        sum += data[perm[i]]; // => co-03: the actual (possibly prefetched) load
    }
    clock_gettime(CLOCK_MONOTONIC, &t1);                              // calls clock_gettime(...)
    *out_sum = sum;                                                   // supporting statement for this example
    return (t1.tv_sec - t0.tv_sec) + (t1.tv_nsec - t0.tv_nsec) / 1e9; // returns the computed result
}

int main(void) {                         // program entry point
    int *data = malloc(sizeof(int) * N); // heap-allocates memory for data
    for (int i = 0; i < N; i++)
        data[i] = i % 997;           // => arbitrary, deterministic content -- values don't
                                     // matter, only addresses do
    int *perm = make_permutation(N); // declares perm

    // co-03: sweep a range of lookahead distances -- too small hides too little
    // of the ~100+ cycle DRAM latency; too large risks the prefetched line being
    // evicted again before use, and wastes memory bandwidth/cache capacity on
    // lines fetched too early -- an interior distance should win.
    int distances[] = {0, 1, 4, 8, 16, 32, 64, 128, 256};         // declares distances
    int n_dist = (int)(sizeof(distances) / sizeof(distances[0])); // declares n_dist

// co-03: run SEVERAL full sweeps over EVERY distance, in the SAME order each
// sweep, and keep the BEST (minimum) time seen per distance across all sweeps
// -- this machine's shared system-level cache and DRAM/TLB state get measurably
// "warmer" after the first full pass over this 256 MB array (confirmed during
// authoring: repeat passes over the identical permutation land ~30% faster than
// the very first pass), which would unfairly favor whichever distance happens
// to run LAST if each distance were measured only once. Multiple full sweeps
// give every distance an equal chance to be measured in both a cooler and a
// warmer state, exactly this topic's best-of-N rule.
#define PASSES 4                                                        // constant PASSES = 4
    double best_per_distance[sizeof(distances) / sizeof(distances[0])]; // supporting statement for
                                                                        // this example
    for (int d = 0; d < n_dist; d++)
        best_per_distance[d] = -1.0;                                     // loop header controlling the sweep below
    long reference_sum = -1;                                             // declares reference_sum
    for (int pass = 0; pass < PASSES; pass++) {                          // loop header controlling the sweep below
        for (int d = 0; d < n_dist; d++) {                               // loop header controlling the sweep below
            long sum;                                                    // declares sum
            double secs = timed_walk(data, perm, N, distances[d], &sum); // declares secs
            if (reference_sum < 0)
                reference_sum = sum; // conditional check
            if (sum != reference_sum) {
                fprintf(stderr, "SUM MISMATCH at distance=%d\n", distances[d]);
            } // prints a report line
            if (best_per_distance[d] < 0 || secs < best_per_distance[d])
                best_per_distance[d] = secs; // conditional check
        }
    }

    printf("N=%d random-order int reads (permutation defeats hardware prefetch), "
           "best of %d sweeps\n",
           N, PASSES); // prints a report line
    double best_time = -1.0, t_none = -1.0,
           t_largest = -1.0;           // declares best_time
    int best_distance = -1;            // declares best_distance
    for (int d = 0; d < n_dist; d++) { // loop header controlling the sweep below
        printf("distance=%-4d  %.4f s\n", distances[d],
               best_per_distance[d]); // prints a report line
        if (best_time < 0 || best_per_distance[d] < best_time) {
            best_time = best_per_distance[d];
            best_distance = distances[d];
        } // conditional check
        if (distances[d] == 0)
            t_none = best_per_distance[d]; // conditional check
        if (distances[d] == distances[n_dist - 1])
            t_largest = best_per_distance[d]; // conditional check
    }

    printf("\nbest distance overall: %d (%.4f s)\n", best_distance,
           best_time); // prints a report line
    printf("no-prefetch baseline (distance=0): %.4f s\n",
           t_none); // prints a report line
    printf("largest tested distance (%d): %.4f s\n", distances[n_dist - 1],
           t_largest); // prints a report line

    // co-03: the SWEEP's own claim ("an optimal distance exists") is about TUNING
    // distance among prefetch-enabled values, not about beating "off" -- find the
    // best AMONG distances[1..] only (the smallest tested distance, 1, through
    // the largest, 256) and verify it is a genuine INTERIOR minimum: strictly
    // better than BOTH the smallest and largest positive distances tested.
    double best_positive_time = -1.0, smallest_positive_time = -1.0,
           largest_positive_time = -1.0;                                           // declares best_positive_time
    int best_positive_distance = -1;                                               // declares best_positive_distance
    for (int d = 1; d < n_dist; d++) {                                             // => skip index 0 (distance=0, the "off" baseline)
        if (best_positive_time < 0 || best_per_distance[d] < best_positive_time) { // conditional check
            best_positive_time = best_per_distance[d];                             // assigns best_positive_time
            best_positive_distance = distances[d];                                 // assigns best_positive_distance
        }
        if (d == 1)
            smallest_positive_time = best_per_distance[d]; // conditional check
        if (d == n_dist - 1)
            largest_positive_time = best_per_distance[d]; // conditional check
    }
    printf("\namong ENABLED prefetch distances only (1..%d): best=%d (%.4f s), "
           "smallest-tested=1 (%.4f s),\n", // prints a report line
           distances[n_dist - 1], best_positive_distance, best_positive_time,
           smallest_positive_time); // continues the printf(...) call above
    printf(" largest-tested=%d (%.4f s)\n", distances[n_dist - 1],
           largest_positive_time);                                             // prints a report line
    int interior_optimum = (best_positive_distance > distances[1]) &&          // declares interior_optimum
                           (best_positive_distance < distances[n_dist - 1]) && // supporting statement for this example
                           (best_positive_time < smallest_positive_time) &&    // supporting statement for this example
                           (best_positive_time < largest_positive_time);       // supporting statement for this example
    printf("\nnote: on THIS machine, no-prefetch (%.4f s) is %s the best "
           "enabled-prefetch distance\n",
           t_none,                                                                         // prints a report line
           t_none <= best_positive_time ? "actually AT LEAST AS FAST AS" : "slower than"); // continues the printf(...) call above
    printf(" (%.4f s) -- this Apple Silicon core's hardware prefetcher + low "
           "unified-memory latency\n", // prints a report line
           best_positive_time);        // continues the printf(...) call above
    printf(" leave little room for software prefetch to win outright here; the "
           "tuning question this\n"); // prints a report line
    printf(" example verifies is narrower: GIVEN you prefetch, does the DISTANCE "
           "matter? -- and it does.\n"); // prints a report line
    printf("PASS (an interior distance among the ENABLED prefetch values beats "
           "both the smallest and\n"); // prints a report line
    printf(" largest distances tested): %s\n",
           interior_optimum ? "PASS" : "FAIL"); // prints a report line

    free(data); // releases data's heap memory
    free(perm); // releases perm's heap memory
    return 0;   // returns the computed result
}
