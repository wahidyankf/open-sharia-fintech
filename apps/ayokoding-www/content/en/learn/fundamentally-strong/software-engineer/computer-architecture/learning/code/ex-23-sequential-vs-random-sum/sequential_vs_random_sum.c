// learning/code/ex-23-sequential-vs-random-sum/sequential_vs_random_sum.c
/* Example 23: Sequential vs Random Sum -- spatial locality measured, not
 * asserted. */

#include <stdio.h>  // => co-03: printf -- reports both timings and the relative speedup
#include <stdlib.h> // => co-03: malloc/free/rand -- the array and its shuffled index permutation
#include <time.h>   // => co-25: clock_gettime -- wall-clock timing, per the shared brief

#define N \
    (32u * 1024u * 1024u) // => co-05: 32M ints = 128 MiB -- far bigger than any
                          // cache level, so misses are real
#define REPEATS 3         // => co-25: best-of-N, per DD-20

static double now_seconds(void) {                        // defines now_seconds(): helper function used by this example
    struct timespec ts;                                  // supporting statement for this example
    clock_gettime(CLOCK_MONOTONIC, &ts);                 // calls clock_gettime(...)
    return (double)ts.tv_sec + (double)ts.tv_nsec / 1e9; // returns the computed result
}

int main(void) {                               // program entry point
    int *data = malloc(N * sizeof(int));       // => co-03: the array both access patterns sum over
    size_t *perm = malloc(N * sizeof(size_t)); // => co-03: a RANDOM permutation of indices 0..N-1
    if (!data || !perm) {                      // => co-03: guard both allocations before touching either
        fprintf(stderr, "malloc failed\n");    // => co-03: reports the failure to stderr, not stdout
        return 1;                              // => co-03: nonzero exit -- allocation failure is not this example's claim
    } // => co-03: defensive check for a 160+ MiB allocation

    for (size_t i = 0; i < N; i++) { // => co-03: fills BOTH arrays in one pass over the same index
        data[i] = (int)(i % 997);    // => co-03: a small repeating pattern, cheap to compute
        perm[i] = i;                 // => co-03: perm starts as the IDENTITY permutation (0,1,2,...)
    } // => co-03: fill data, perm starts identity

    srand(42);                               // => co-03: FIXED seed -- makes this run reproducible
    for (size_t i = N - 1; i > 0; i--) {     // => co-03: Fisher-Yates shuffle -- genuinely randomizes perm
        size_t j = (size_t)rand() % (i + 1); // => co-03: pick a random earlier-or-equal index
        size_t tmp = perm[i];                // => co-03: standard 3-step swap, first half
        perm[i] = perm[j];                   // => co-03: standard 3-step swap, second half
        perm[j] = tmp;                       // => co-03: swap -- standard shuffle step
    }

    double seq_best = 1e300, rand_best = 1e300; // => co-25: best-of-N trackers
    volatile long sink = 0;                     // => co-03: volatile -- prevents the compiler from discarding the sums

    for (int r = 0; r < REPEATS; r++) {          // => co-25: REPEATS runs of each pattern, keep the fastest
        double t0 = now_seconds();               // => co-25: start sequential timer
        long seq_sum = 0;                        // => co-03: local accumulator for THIS repeat
        for (size_t i = 0; i < N; i++)           // => co-03: walks the array in ascending order
            seq_sum += data[i];                  // => co-03: SEQUENTIAL access -- next line often
                                                 // shares a cache line
        double seq_elapsed = now_seconds() - t0; // => co-25: elapsed time for this sequential pass
        if (seq_elapsed < seq_best)
            seq_best = seq_elapsed; // => co-25: keep the fastest sequential run
        sink += seq_sum;            // => co-03: accumulate into sink so the sum is never dead code

        double t1 = now_seconds(); // => co-25: start random timer
        long rand_sum = 0;         // => co-03: local accumulator for THIS repeat
        for (size_t i = 0; i < N; i++)
            rand_sum += data[perm[i]];            // => co-03: RANDOM access -- almost always a
                                                  // cache miss
        double rand_elapsed = now_seconds() - t1; // => co-25: elapsed time for this random pass
        if (rand_elapsed < rand_best)
            rand_best = rand_elapsed; // => co-25: keep the fastest random run
        sink += rand_sum;             // => co-03: same anti-optimization technique
    }

    double speedup = rand_best / seq_best; // => co-05: relative comparison -- portable across machines
    printf("sequential best of %d = %.4f s\n", REPEATS,
           seq_best); // => co-25: fastest sequential-order pass
    printf("random best of %d     = %.4f s\n", REPEATS,
           rand_best); // => co-25: fastest random-order pass
    printf("random / sequential   = %.2fx\n",
           speedup); // => co-05: how much slower random access is
    printf("sink (ignore)         = %ld\n",
           sink); // => co-03: proves the loops were not optimized away

    // ex-23: the claim -- SEQUENTIAL access is measurably faster than RANDOM
    // access over the same data, because sequential access exploits spatial
    // locality (co-03) while random access defeats it, paying a fresh miss almost
    // every touch (co-05)
    int correct = (speedup > 1.2); // => co-05: a modest, honest threshold -- not an inflated claim
    printf("%s\n", correct         // => co-05: PASS/FAIL verdict
                       ? "PASS: sequential access measurably faster than random "
                         "access (spatial locality)" // supporting statement for
                                                     // this example
                       : "FAIL: sequential access was not measurably faster than "
                         "random"); // supporting statement for this example

    free(data);             // => co-03: releases the data array
    free(perm);             // => co-03: releases both large allocations
    return correct ? 0 : 1; // => co-05: nonzero exit on assertion failure
}
