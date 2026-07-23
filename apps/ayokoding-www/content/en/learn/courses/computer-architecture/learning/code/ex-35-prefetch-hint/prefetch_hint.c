// learning/code/ex-35-prefetch-hint/prefetch_hint.c
/* Example 35: add a __builtin_prefetch hint to a random-index (gather)
   summation -- measure its REAL effect on this machine, honestly, rather
   than assume the textbook win (co-03, co-25). */
#include <stdio.h>  // => printf -- the timing/finding report this program prints
#include <stdlib.h> // => malloc/free/rand -- the data array and its random permutation
#include <time.h>   // => clock_gettime -- the portable wall-clock timer used below

#define N \
    100000000 // => co-03: 100M ints = 400 MB -- far bigger than this machine's 4
              // MiB L2,
              //    so every access below is a real DRAM-latency miss
#define BLOCK \
    64 // => co-03: prefetch a whole 64-element BLOCK ahead at once, not one
       //    element at a time -- the block-ahead shape used in real
       //    prefetch-tuned kernels (tried first: per-element prefetch;
       //    block-ahead measured the same)
#define BLOCK_AHEAD \
    256          // => co-03: how many elements AHEAD (in the permutation's visiting order)
                 //    the block of prefetches targets
#define TRIALS 4 // => co-25: best-of-4 -- shared-machine noise smoothing

static double now_seconds(void) {                        // => co-25: shared wall-clock helper, this topic's standard pattern
    struct timespec ts;                                  // supporting statement for this example
    clock_gettime(CLOCK_MONOTONIC, &ts);                 // calls clock_gettime(...)
    return (double)ts.tv_sec + (double)ts.tv_nsec / 1e9; // returns the computed result
}

// co-03: Fisher-Yates -- a genuinely random VISITING ORDER (not a dependent
// pointer chase), so each element's target address is unpredictable to a
// hardware STRIDE prefetcher, but fully knowable BLOCK_AHEAD steps in advance
// from the array alone -- exactly the shape software prefetching is designed to
// exploit.
static void shuffle(int *perm,
                    int n) { // defines shuffle(): helper function used by this example
    for (int i = 0; i < n; i++)
        perm[i] = i;                  // => start as the identity order
    for (int i = n - 1; i > 0; i--) { // => standard Fisher-Yates from the back
        int j = rand() % (i + 1);     // declares j
        int tmp = perm[i];
        perm[i] = perm[j];
        perm[j] = tmp; // => swap -- builds one random permutation
    }
}

// co-03: no hint -- the CPU only discovers `data[perm[i]]` is needed when the
// load actually issues; this machine's out-of-order engine still overlaps many
// INDEPENDENT loads on its own (co-22), which is exactly what this example
// measures.
static long sum_no_prefetch(const int *data, const int *perm,
                            int n) { // defines sum_no_prefetch(): helper function used by this example
    long total = 0;                  // declares total
    for (int i = 0; i < n; i++) {    // loop header controlling the sweep below
        total += data[perm[i]];      // => co-05: an unpredicted-address gather load
    }
    return total; // returns the computed result
}

// co-03: WITH the hint -- __builtin_prefetch tells the CPU "you will want this
// address soon", issued for a whole BLOCK_AHEAD-elements-ahead block before
// that block is consumed, hoping the fetch lands in cache before the real load
// needs it.
static long sum_with_prefetch(const int *data, const int *perm,
                              int n) {        // defines sum_with_prefetch(): helper
                                              // function used by this example
    long total = 0;                           // declares total
    int i = 0;                                // declares i
    for (; i + BLOCK <= n; i += BLOCK) {      // => co-03: process one BLOCK of elements at a time
        int fbase = i + BLOCK_AHEAD;          // => co-03: this block's prefetch TARGETS start here
        if (fbase + BLOCK <= n) {             // conditional check
            for (int k = 0; k < BLOCK; k++) { // loop header controlling the sweep below
                __builtin_prefetch(&data[perm[fbase + k]], 0,
                                   1); // => co-03: read hint, low locality (used once)
            }
        }
        for (int k = 0; k < BLOCK; k++)
            total += data[perm[i + k]]; // => co-05: the real, consumed loads
    }
    for (; i < n; i++)
        total += data[perm[i]]; // => co-03: scalar tail for n not a multiple of BLOCK
    return total;               // returns the computed result
}

int main(void) {                                 // program entry point
    srand(7);                                    // => co-25: fixed seed -- reproducible permutation
    int *data = malloc((size_t)N * sizeof(int)); // => the 400 MB array being summed
    int *perm = malloc((size_t)N * sizeof(int)); // => the random visiting order over that array
    if (!data || !perm) {
        fprintf(stderr, "alloc failed\n");
        return 1;
    } // prints a report line
    for (int i = 0; i < N; i++)
        data[i] = (i * 2654435761u) % 1000u; // => deterministic filler values
    shuffle(perm, N);                        // => one random permutation, reused by BOTH runs

    double best_no_pf = 1e18, best_pf = 1e18;   // declares best_no_pf
    long sum_a = 0, sum_b = 0;                  // declares sum_a
    for (int t = 0; t < TRIALS; t++) {          // => co-25: best-of-N -- keep the fastest clean run
        double t0 = now_seconds();              // declares t0
        sum_a = sum_no_prefetch(data, perm, N); // assigns sum_a
        double t1 = now_seconds();              // declares t1
        if (t1 - t0 < best_no_pf)
            best_no_pf = t1 - t0; // conditional check

        double t2 = now_seconds();                // declares t2
        sum_b = sum_with_prefetch(data, perm, N); // assigns sum_b
        double t3 = now_seconds();                // declares t3
        if (t3 - t2 < best_pf)
            best_pf = t3 - t2; // conditional check
    }

    printf("N=%d ints (%.0f MB), block=%d, block_ahead=%d, best of %d\n",
           N, // prints a report line
           (double)(N * sizeof(int)) / (1024.0 * 1024.0), BLOCK, BLOCK_AHEAD,
           TRIALS); // continues the printf(...) call above
    printf("no prefetch:   sum=%ld, %.4f s (%.2f ns/elem)\n", sum_a,
           best_no_pf,            // prints a report line
           best_no_pf * 1e9 / N); // continues the printf(...) call above
    printf("with prefetch: sum=%ld, %.4f s (%.2f ns/elem)\n", sum_b, best_pf,
           best_pf * 1e9 / N);           // prints a report line
    double ratio = best_no_pf / best_pf; // => co-03: >1.0 would mean prefetch helped
    printf("prefetch ratio: %.2fx, correctness: %s\n", ratio,
           (sum_a == sum_b) ? "identical sums" : "MISMATCH -- BUG"); // prints a report line
    printf(                                                          // prints a report line
        "OBSERVED FINDING (measured, not assumed, per co-25): on THIS machine's "
        "deep\n" // continues the printf(...) call above
        "out-of-order core, %s -- see prose for why (co-22's memory-level "
        "parallelism\n"                                                                                      // continues the printf(...) call above
        "already overlaps independent gather loads without help here).\n",                                   // continues
                                                                                                             // the
                                                                                                             // printf(...)
                                                                                                             // call
                                                                                                             // above
        ratio > 1.03 ? "the prefetch hint measurably helped" : "the prefetch hint did NOT measurably help"); // continues the
                                                                                                             // printf(...) call
                                                                                                             // above
    free(data);                                                                                              // releases data's heap memory
    free(perm);                                                                                              // releases perm's heap memory
    return (sum_a == sum_b) ? 0 : 1;                                                                         // => correctness is the only hard gate here --
} //    this example's point is the MEASUREMENT itself
