// learning/code/ex-31-working-set-cache-cliffs/working_set_cliffs.c
// Example 31: pointer-chase through working sets crossing L1 (64 KiB) and L2
// (4 MiB) on this machine -- report the REAL observed cliffs, honestly (co-01,
// co-05).
#include <stdio.h>  // => co-01: printf -- the per-size latency table this program prints
#include <stdlib.h> // => co-01: malloc/free/rand -- buffer allocation and permutation shuffling
#include <time.h>   // => co-25: clock_gettime -- the portable wall-clock timer used below

#define N_SIZES 12     // => co-01: number of working-set sizes swept, 16 KiB .. 32 MiB
#define STEPS 4000000L // => co-05: pointer-chase steps timed per working-set size
// => co-25: this example REPORTS whatever cliffs actually appear on THIS
// => machine/run rather than asserting the textbook L1=64 KiB/L2=4 MiB numbers

static double now_seconds(void) { // => co-25: same portable clock_gettime timer used across this tier
    struct timespec ts;           // => co-25: POSIX timespec, seconds + nanoseconds fields
    clock_gettime(CLOCK_MONOTONIC,
                  &ts);                                  // => co-25: monotonic -- immune to wall-clock adjustment mid-run
    return (double)ts.tv_sec + (double)ts.tv_nsec / 1e9; // => co-25: combined into one double-seconds value
}

// => co-05: Sattolo's algorithm -- builds ONE single cycle over all n indices
// => (no short sub-cycles), so pointer-chasing it truly wanders the ENTIRE
// => working set instead of bouncing inside a small, easily cached loop
static void sattolo_shuffle(int *arr,
                            int n) { // => co-05: builds the pointer-chase path
                                     // -- read this BEFORE chase_ns_per_access
    for (int i = 0; i < n; i++)
        arr[i] = i;                   // => co-05: start as the identity permutation
    for (int i = n - 1; i > 0; i--) { // => co-05: Sattolo's variant of
                                      // Fisher-Yates -- guarantees one big cycle
        int j = rand() % i;           // => co-05: j strictly < i (never swaps an element with itself)
        int tmp = arr[i];
        arr[i] = arr[j];
        arr[j] = tmp; // => co-05: swap -- builds the single-cycle permutation in place
    } // => co-05: after this loop, arr is one n-length cycle:
      // 0->arr[0]->arr[arr[0]]->...
}

// => co-05: chases arr[idx] STEPS times -- each load depends on the PREVIOUS
// => load's result, so out-of-order execution cannot hide the memory latency;
// => this measures real latency, not throughput
static double chase_ns_per_access(int *arr, int n, long steps) {
    volatile int idx = 0;              // => co-25: volatile -- forces every dependent load to really happen
    double t0 = now_seconds();         // => co-25: start the clock right before the timed
                                       // dependent-load loop
    for (long i = 0; i < steps; i++) { // => co-05: STEPS sequential, data-dependent loads
        idx = arr[idx];                // => co-05: the next index to visit -- unknown until THIS
                                       // load returns
    }
    double t1 = now_seconds();              // => co-25: stop the clock right after the loop
    (void)n;                                // => co-25: n only used by the caller for the printed table, not here
    return (t1 - t0) * 1e9 / (double)steps; // => co-25: normalized to nanoseconds
                                            // per pointer-chase step
}

int main(void) {
    srand(42);                                                                                     // => co-05: fixed seed -- the SAME permutation shape every run
    size_t sizes_kib[N_SIZES] = {16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768}; // => co-01: KiB working sets
    int max_elems = (int)((sizes_kib[N_SIZES - 1] * 1024UL) / sizeof(int));                        // => co-01: largest size drives the one shared buffer
    int *buf = malloc((size_t)max_elems * sizeof(int));                                            // => co-01: one 32 MiB buffer, reused
                                                                                                   // (re-shuffled) at each smaller size
    if (buf == NULL) {
        fprintf(stderr, "alloc failed\n");
        return 1;
    } // => co-25: fail loudly, never time a null pointer

    printf("L1d=64 KiB, L2=4 MiB on this machine (sysctl "
           "hw.l1dcachesize/hw.l2cachesize)\n"); // => co-01: known boundaries,
                                                 // stated up front
    printf("%10s %14s\n", "size(KiB)",
           "ns/access");                                      // => co-01: table header for the sweep below
    double prev_ns = 0.0;                                     // => co-05: previous size's latency, for computing the jump ratio
    int printed_first = 0;                                    // => co-05: skip the ratio print on the very first (smallest) size
    for (int s = 0; s < N_SIZES; s++) {                       // => co-01: one timed pointer-chase per working-set size
        int n = (int)((sizes_kib[s] * 1024UL) / sizeof(int)); // => co-01: element count for THIS size, within
                                                              // the shared buffer
        sattolo_shuffle(buf, n);                              // => co-05: a fresh single-cycle permutation
                                                              // confined to the first n ints
        double ns = chase_ns_per_access(buf, n,
                                        STEPS); // => co-05: the real measured latency for this working-set size
        printf("%10zu %14.2f", sizes_kib[s],
               ns);                      // => co-05: prints the REAL measured ns/access, never a guessed
                                         // number
        if (printed_first) {             // => co-05: report the jump ratio vs the PREVIOUS
                                         // (smaller) size
            double ratio = ns / prev_ns; // => co-05: how much slower THIS size is
                                         // than the one before it
            printf("   (%.2fx vs prior size)",
                   ratio); // => co-05: prints the real ratio, not an assumed textbook
                           // number
            if (ratio > 1.4)
                printf("  <-- CLIFF"); // => co-05: flag a real, measured jump -- not
                                       // asserted, OBSERVED
        }
        printf("\n");      // => co-05: end this size's table row
        prev_ns = ns;      // => co-05: remember this size's latency for the NEXT ratio
        printed_first = 1; // => co-05: every size after the first prints a ratio
    }
    free(buf); // => co-01: release the 32 MiB shared buffer
    printf("\nObserved cliffs are reported above as measured, not assumed -- see "
           "the\n"
           "prose discussion for which sizes crossed L1/L2 on THIS run.\n"); // =>
                                                                             // co-25:
                                                                             // honesty
                                                                             // statement
                                                                             // per
                                                                             // DD-20
    return 0;                                                                // => co-25: this example reports observations -- no PASS/FAIL
                                                                             // threshold
}
