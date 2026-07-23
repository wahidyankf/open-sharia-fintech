// learning/code/ex-30-aos-vs-soa-hot-loop/aos_vs_soa.c
// Example 30: sum ONE hot field across a large array-of-structs (AoS) vs the
// same data as a struct-of-arrays (SoA) -- verify SoA wins the hot-only sum
// (co-17).
#include <stdio.h>  // => co-17: printf -- the timing/PASS report this program prints
#include <stdlib.h> // => co-17: malloc/free -- both layouts under test are heap-allocated
#include <time.h>   // => co-17: clock_gettime -- the portable wall-clock timer used below

#define N \
    8000000       // => co-17: 8M elements -- each AoS struct is 64 B, so AoS = 512 MiB
                  // total
#define REPEATS 3 // => co-25: best-of-3 -- shared-machine noise smoothing (DD-20 step 2)
// => co-17: cold[15] simulates the OTHER 15 fields a real record carries
// => (name, timestamps, flags, ...) that a hot loop never touches per iteration

typedef struct {  // => co-17: array-of-structs -- ONE struct per element, fields
                  // interleaved
    int hot;      // => co-17: the ONLY field the hot loop below actually reads
    int cold[15]; // => co-17: 15 unused ints -- simulates a "real" record's other
                  // fields
} AosRecord;      // => co-16: sizeof(AosRecord) == 64 B (16 ints * 4 B), no padding
                  // needed here

static double now_seconds(void) { // => co-25: same portable clock_gettime timer used across this tier
    struct timespec ts;           // => co-25: POSIX timespec, seconds + nanoseconds fields
    clock_gettime(CLOCK_MONOTONIC,
                  &ts);                                  // => co-25: monotonic -- immune to wall-clock adjustment mid-run
    return (double)ts.tv_sec + (double)ts.tv_nsec / 1e9; // => co-25: combined into one double-seconds value
}

static long sum_hot_aos(const AosRecord *records,
                        int n) {  // => co-17: reads records[i].hot, skipping
                                  // records[i].cold every time
    long total = 0;               // => co-17: accumulator over the hot field only
    for (int i = 0; i < n; i++) { // => co-17: one iteration per record -- N total
        total += records[i].hot;  // => co-17: pulls in the WHOLE 64 B struct's cache
                                  // line for 4 B of data
    }
    return total; // => co-17: same mathematical sum as sum_hot_soa below
}

static long sum_hot_soa(const int *hot,
                        int n) {  // => co-17: reads hot[i] directly -- cold
                                  // fields live in a SEPARATE array
    long total = 0;               // => co-17: accumulator over the SAME hot values, different layout
    for (int i = 0; i < n; i++) { // => co-17: one iteration per element -- N total, identical work
        total += hot[i];          // => co-17: every fetched cache line is 100% hot data, 0%
                                  // wasted
    }
    return total; // => co-17: same mathematical sum as sum_hot_aos above
}

int main(void) { // => co-25: single self-contained process -- both layouts run in it
    // => co-17: two layouts of the SAME logical data -- one struct per record
    // (AoS)
    // => vs one flat array of just the hot field (SoA) -- correctness must match
    AosRecord *aos = malloc((size_t)N * sizeof(AosRecord)); // => co-17: 512 MiB -- N structs,
                                                            // hot+cold interleaved per record
    int *soa_hot = malloc((size_t)N * sizeof(int));         // => co-17: 32 MiB -- N ints, ONLY the
                                                            // hot field, tightly packed
    if (aos == NULL || soa_hot == NULL) {
        fprintf(stderr, "alloc failed\n");
        return 1;
    } // => co-25: fail loudly, never time a null pointer

    for (int i = 0; i < N; i++) {      // => co-01: fill both layouts with the SAME hot values once
        int value = (i * 7919) % 1009; // => co-01: arbitrary deterministic value --
                                       // content doesn't matter
        aos[i].hot = value;            // => co-17: same value written into the AoS record's hot field
        soa_hot[i] = value;            // => co-17: same value written into the SoA hot-only array
    }

    double best_aos = 1e18,
           best_soa = 1e18;        // => co-25: track the FASTEST of REPEATS runs per layout
    long aos_sum = 0, soa_sum = 0; // => co-17: captured to prove both layouts
                                   // compute the SAME answer
    // => co-17: both loops read exactly N ints of real data -- only the STRIDE
    // => between successive hot values (64 B in AoS, 4 B in SoA) differs
    for (int r = 0; r < REPEATS; r++) { // => co-25: re-run to confirm the result reproduces
        double t0 = now_seconds();      // => co-25: start the clock for this AoS pass
        aos_sum = sum_hot_aos(aos,
                              N);  // => co-17: the cache-hostile layout -- 15/16 of each line wasted
        double t1 = now_seconds(); // => co-25: stop the clock for this AoS pass
        if (t1 - t0 < best_aos)
            best_aos = t1 - t0; // => co-25: keep the best AoS timing so far

        double t2 = now_seconds(); // => co-25: start the clock for this SoA pass
        soa_sum = sum_hot_soa(soa_hot,
                              N);  // => co-17: the cache-friendly layout -- every fetched byte used
        double t3 = now_seconds(); // => co-25: stop the clock for this SoA pass
        if (t3 - t2 < best_soa)
            best_soa = t3 - t2; // => co-25: keep the best SoA timing so far
    }

    printf("AoS hot-field sum: %ld, best of %d: %.4f s\n", aos_sum, REPEATS,
           best_aos); // => co-17: methodology stated in output
    printf("SoA hot-field sum: %ld, best of %d: %.4f s\n", soa_sum, REPEATS,
           best_soa);                     // => co-17: methodology stated in output
    double speedup = best_aos / best_soa; // => co-17: how many times slower the
                                          // interleaved layout really was
    printf("SoA is %.2fx faster -> %s\n",
           speedup,                                // => co-25: prints the ratio the reader should verify against
                                                   // below
           (aos_sum == soa_sum && speedup > 1.2) ? // => co-17: correctness (equal sums) AND speed both gate the PASS
               "PASS (identical sums, SoA measurably faster for hot-only sum)"
                                                 :        // => co-25: the program judges its own claim
               "FAIL");                                   // => co-25: an honest FAIL label if either condition fails
    free(aos);                                            // => co-17: release the 512 MiB AoS buffer
    free(soa_hot);                                        // => co-17: release the 32 MiB SoA buffer
    return (aos_sum == soa_sum && speedup > 1.2) ? 0 : 1; // => co-25: real process exit code reflecting the PASS/FAIL
}
