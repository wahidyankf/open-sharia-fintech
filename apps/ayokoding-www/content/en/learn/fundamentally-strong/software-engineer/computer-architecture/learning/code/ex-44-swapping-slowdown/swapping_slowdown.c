// learning/code/ex-44-swapping-slowdown/swapping_slowdown.c
/* Example 44: a SAFE, bounded proxy for the memory-hierarchy-cliff-at-scale
   story -- verify a cache-resident working set is measurably faster than a
   DRAM-resident one FAR bigger than any cache level, WITHOUT ever driving
   this shared dev machine into real disk-swap (co-10). */
#include <stdio.h>  // => printf -- the timing/finding report this program prints
#include <stdlib.h> // => malloc/free/rand -- the buffer and its random pointer-chase permutation
#include <time.h>   // => clock_gettime -- the portable wall-clock timer used below

// co-10: DELIBERATE SAFETY BOUND -- this machine has 32 GB RAM; 512 MB is
// comfortably inside it (no risk of exhausting RAM or forcing real disk-swap on
// a SHARED dev machine). This example does NOT claim to measure real swap
// latency -- see the honest discussion below and in prose for why that would be
// irresponsible here.
#define SMALL_KIB 256L // => co-10: 256 KiB -- fits inside this machine's 4 MiB L2 easily
#define LARGE_MB \
    512L               // => co-10: 512 MB -- far bigger than any cache level, still safely
                       // RAM-resident
#define STEPS 4000000L // => co-10: pointer-chase steps timed per working-set size

static double now_seconds(void) {                        // => co-25: shared wall-clock helper, this topic's standard pattern
    struct timespec ts;                                  // supporting statement for this example
    clock_gettime(CLOCK_MONOTONIC, &ts);                 // calls clock_gettime(...)
    return (double)ts.tv_sec + (double)ts.tv_nsec / 1e9; // returns the computed result
}

// co-05: Sattolo's algorithm -- one single cycle over all n indices, so a
// pointer-chase genuinely wanders the ENTIRE working set (same technique ex-31
// uses).
static void sattolo_shuffle(int *arr,
                            int n) { // defines sattolo_shuffle(): helper function used by this example
    for (int i = 0; i < n; i++)
        arr[i] = i;                   // loop header controlling the sweep below
    for (int i = n - 1; i > 0; i--) { // loop header controlling the sweep below
        int j = rand() % i;           // declares j
        int tmp = arr[i];
        arr[i] = arr[j];
        arr[j] = tmp; // declares tmp
    }
}

// co-10: each load DEPENDS on the previous load's result -- out-of-order
// execution cannot hide this latency, so the measured ns/access is close to the
// REAL latency of whichever memory level currently holds the working set
// (co-01).
static double chase_ns_per_access(int *arr,
                                  long steps) { // defines chase_ns_per_access(): helper
                                                // function used by this example
    volatile int idx = 0;                       // declares idx
    double t0 = now_seconds();                  // declares t0
    for (long i = 0; i < steps; i++)
        idx = arr[idx];                     // loop header controlling the sweep below
    double t1 = now_seconds();              // declares t1
    return (t1 - t0) * 1e9 / (double)steps; // returns the computed result
}

int main(void) {                                             // program entry point
    srand(5);                                                // => co-25: fixed seed -- reproducible permutation
    int small_n = (int)((SMALL_KIB * 1024L) / sizeof(int));  // declares small_n
    long large_n = (LARGE_MB * 1024L * 1024L) / sizeof(int); // declares large_n

    int *small_buf = malloc((size_t)small_n * sizeof(int)); // heap-allocates memory for small_buf
    int *large_buf = malloc((size_t)large_n * sizeof(int)); // heap-allocates memory for large_buf
    if (!small_buf || !large_buf) {
        fprintf(stderr, "alloc failed\n");
        return 1;
    } // prints a report line

    sattolo_shuffle(small_buf, small_n); // calls sattolo_shuffle(...)
    sattolo_shuffle((int *)large_buf,
                    (int)large_n); // => large_n fits in int range here (128M elements max)

    double ns_small = chase_ns_per_access(small_buf, STEPS); // => co-10: cache-resident latency
    double ns_large = chase_ns_per_access(large_buf, STEPS); // => co-10: DRAM-resident latency

    printf("small working set: %ld KiB, %.2f ns/access (cache-resident)\n", SMALL_KIB, ns_small);        // prints a report line
    printf("large working set: %ld MB, %.2f ns/access (DRAM-resident)\n", LARGE_MB, ns_large);           // prints a report line
    double ratio = ns_large / ns_small;                                                                  // declares ratio
    printf("DRAM/cache latency ratio: %.2fx -> %s\n", ratio,                                             // prints a report line
           ratio > 2.0 ? "PASS (measured, real gap between cache- and DRAM-resident latency)" : "FAIL"); // continues the printf(...) call above

    printf( // prints a report line
        "\nHONEST SCOPE NOTE (co-10): this example measures the REAL, SAFE "
        "cache-vs-DRAM\n" // continues the printf(...) call above
        "gap above -- it does NOT trigger real disk-swap. Deliberately: this box "
        "has 32 GB\n" // continues the printf(...) call above
        "RAM and forcing a working set past that (to cause real major page "
        "faults hitting\n" // continues the printf(...) call above
        "SSD/disk) would destabilize a SHARED dev machine. Published SSD "
        "random-access\n" // continues the printf(...) call above
        "latency runs roughly 50-150 microseconds and spinning-disk seek latency "
        "roughly\n" // continues the printf(...) call above
        "5-10 milliseconds, vs the DRAM latency measured above in nanoseconds -- "
        "that is a\n" // continues the printf(...) call above
        "further 100x-100,000x gap ON TOP OF the DRAM-vs-cache gap this program "
        "actually\n" // continues the printf(...) call above
        "measured. The mechanism is the SAME structural phenomenon one level "
        "further down\n" // continues the printf(...) call above
        "the memory hierarchy (co-01): once a working set exceeds what a level "
        "can hold, a\n" // continues the printf(...) call above
        "miss there costs a trip to the next slower, bigger level -- swapping is "
        "this same\n"                                                // continues the printf(...) call above
        "story applied to RAM-vs-disk instead of cache-vs-DRAM.\n"); // continues
                                                                     // the
                                                                     // printf(...)
                                                                     // call above

    free(small_buf);            // releases small_buf's heap memory
    free(large_buf);            // releases large_buf's heap memory
    return ratio > 2.0 ? 0 : 1; // returns the computed result
}
