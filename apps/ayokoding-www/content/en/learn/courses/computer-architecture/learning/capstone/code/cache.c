// learning/capstone/code/cache.c
/* Capstone step 2: the cache-HOSTILE baseline -- average the `reading` field
 * across a large array of SensorRecord structs (array-of-structs). Each record
 * carries plenty of cold metadata the averaging kernel never touches, so every
 * cache-line fetch wastes most of its bytes on fields this loop ignores.
 * Compiled and timed the same way as every other example in this topic
 * (clock_gettime, best-of-N wall clock) -- the exact same dataset and kernel
 * is restructured in cache_soa.c, and the two are compared for correctness
 * and speed in explanation.md.
 */
#include <assert.h>
#include <stdint.h> // => int32_t/int64_t -- fixed-width fields so SensorRecord's byte layout is exact
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define N \
    2000000 // => co-17: 2M sensor readings -- large enough that layout, not loop
            // overhead, dominates
#define TRIALS \
    5 // => co-25: best-of-N wall-clock timing, this topic's established
      // measurement methodology

// ex-cache: a deliberately realistic "sensor record" -- one HOT field (reading)
// the averaging kernel needs, wrapped in COLD fields (id, location label,
// timestamp) nobody touches in this kernel -- co-17: exactly the AoS shape a
// real telemetry/IoT record takes
typedef struct {
    int32_t sensor_id;  // => COLD -- never read by the averaging kernel
    float reading;      // => HOT -- the ONE field this kernel actually reads
    char location[112]; // => COLD -- sized so sizeof == 128 B == one full cache
                        // line on this machine
    int64_t timestamp;  // => COLD -- never read by the averaging kernel
} SensorRecord;         // => sizeof == 128 bytes: exactly one 128 B cache line per
                        // record (4 + 4 + 112 + 8 = 128, no trailing padding needed for
                        // int64_t's
                        //  8-byte alignment -- verified below, not just asserted)

static double average_reading_aos(const SensorRecord *records,
                                  int n) { // => co-17: cache-hostile pass
    double sum = 0.0;                      // => double accumulator: avoids float accumulation error at
                                           // N=2M terms
    for (int i = 0; i < n; i++) {          // => co-17: one full 128 B cache-line record
                                           // loaded per iteration...
        sum += records[i].reading;         // => ...to read 4 of those 128 bytes -- the rest
                                           // is wasted memory traffic
    }
    return sum / n;
}

static double best_of_seconds(double *out_result, const SensorRecord *data, int n) {
    double best = -1.0;
    double result = 0.0;
    for (int t = 0; t < TRIALS; t++) { // => co-25: report the fastest of TRIALS
                                       // runs, not one noisy sample
        struct timespec t0, t1;
        clock_gettime(CLOCK_MONOTONIC, &t0);
        result = average_reading_aos(data, n);
        clock_gettime(CLOCK_MONOTONIC, &t1);
        double secs = (t1.tv_sec - t0.tv_sec) + (t1.tv_nsec - t0.tv_nsec) / 1e9;
        if (best < 0 || secs < best)
            best = secs;
    }
    *out_result = result;
    return best;
}

int main(void) {
    static_assert(sizeof(SensorRecord) == 128, "SensorRecord must be exactly one 128 B cache line");
    // => co-02: a COMPILE-TIME check, not just a comment claim -- this build
    // fails loudly if the struct's true size ever drifts from the 128 B this
    // whole capstone step's story depends on

    SensorRecord *records = malloc(sizeof(SensorRecord) * (size_t)N);
    if (!records) {
        fprintf(stderr, "alloc failed\n");
        return 1;
    }

    unsigned seed = 7u; // => deterministic PRNG seed -- reproducible dataset every run
    for (int i = 0; i < N; i++) {
        seed = seed * 1103515245u + 12345u;
        records[i].sensor_id = (int32_t)(i % 4096);
        records[i].reading = (float)(seed % 10000u) * 0.01f; // => reading in [0.00, 99.99)
        memset(records[i].location, 0, sizeof(records[i].location));
        records[i].timestamp = 1700000000LL + i;
    }

    printf("dataset: N=%d records, sizeof(SensorRecord)=%zu bytes (%.1f MB total "
           "AoS)\n",
           N, sizeof(SensorRecord), (double)(sizeof(SensorRecord) * (size_t)N) / 1e6);

    double result;
    double secs = best_of_seconds(&result, records, N);
    printf("AoS (cache-hostile) average_reading: best of %d = %.4f s, result=%.6f\n", TRIALS, secs, result);

    free(records);
    return 0;
}
