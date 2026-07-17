// learning/capstone/code/cache_soa.c
/* Capstone step 3: the cache-FRIENDLY restructuring of cache.c's exact kernel
 * and dataset. Only the LAYOUT changes -- struct-of-arrays instead of
 * array-of-structs
 * -- so the averaging loop touches only a dense `float reading[]` array: every
 * 128 B cache line now holds 32 real, useful readings instead of one. Same
 * seed, same values, same arithmetic, same best-of-N timing methodology as
 * cache.c, so the two are directly comparable in explanation.md.
 */
#include <stdint.h> // => int32_t/int64_t -- same fixed-width fields cache.c uses, for a fair byte-for-byte comparison
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define N \
    2000000 // => co-17: identical record count to cache.c -- only the layout
            // differs, not the data volume
#define TRIALS \
    5 // => co-25: same best-of-N wall-clock methodology as every other example in
      // this topic

// ex-cache-soa: the SAME four fields as cache.c's SensorRecord, but held as
// four separate dense arrays -- co-17: the averaging kernel below now touches
// ONLY the `reading` array; sensor_id/location/timestamp are never even
// allocated densely alongside it, so no cache line is ever wasted on cold bytes
typedef struct {
    int32_t *sensor_id;    // => COLD -- still allocated (for a fair total-byte-count
                           // comparison) but never read below
    float *reading;        // => HOT -- the only array this kernel's hot loop actually reads
    char (*location)[112]; // => COLD -- same 112 B width as cache.c's AoS field,
                           // for an apples-to-apples byte count
    int64_t *timestamp;    // => COLD -- allocated but never touched by
                           // average_reading_soa
} SensorSoA;               // => co-17: four separate arrays instead of one array-of-structs
                           // -- this is the ONLY change

static double average_reading_soa(const float *reading,
                                  int n) { // => co-17: cache-friendly pass
    double sum = 0.0;                      // => same accumulator type, same arithmetic -- ONLY layout changed
    for (int i = 0; i < n; i++) {          // => co-03: sequential dense reads, 32 useful
                                           // floats per 128 B line
        sum += reading[i];                 // => co-17: every fetched byte in this line is a real
                                           // reading -- nothing wasted
    }
    return sum / n; // => identical formula to cache.c's average_reading_aos
}

static double best_of_seconds(double *out_result, const float *reading, int n) {
    double best = -1.0; // => co-25: track the FASTEST of TRIALS runs, not the average
    double result = 0.0;
    for (int t = 0; t < TRIALS; t++) { // => co-25: re-run to smooth shared-machine noise
        struct timespec t0, t1;        // => co-25: POSIX timespec -- seconds + nanoseconds
        clock_gettime(CLOCK_MONOTONIC,
                      &t0);                       // => co-25: monotonic clock -- immune to wall-clock adjustment
        result = average_reading_soa(reading, n); // => the ONLY line whose timing this function measures
        clock_gettime(CLOCK_MONOTONIC, &t1);
        double secs = (t1.tv_sec - t0.tv_sec) + (t1.tv_nsec - t0.tv_nsec) / 1e9; // => combine into one double-seconds value
        if (best < 0 || secs < best)
            best = secs; // => co-25: keep the best (least noisy) timing so far
    }
    *out_result = result; // => captured to prove cache.c and this file compute the SAME sum
    return best;
}

int main(void) {
    SensorSoA soa;                                                           // => co-17: four independent heap allocations, not one struct array
    soa.sensor_id = malloc(sizeof(int32_t) * (size_t)N);                     // => cold array 1 -- id, never read by the hot loop
    soa.reading = malloc(sizeof(float) * (size_t)N);                         // => HOT array -- the only one average_reading_soa touches
    soa.location = malloc(sizeof(*soa.location) * (size_t)N);                // => cold array 2 -- 112 B label per record, never read
    soa.timestamp = malloc(sizeof(int64_t) * (size_t)N);                     // => cold array 3 -- never read by the hot loop
    if (!soa.sensor_id || !soa.reading || !soa.location || !soa.timestamp) { // => co-25: fail loudly, never time a null pointer
        fprintf(stderr, "alloc failed\n");
        return 1;
    }

    // => IDENTICAL generation sequence to cache.c's AoS dataset, so the two
    // averages must match bit-for-bit -- proves the layout change alone drove any
    // speedup
    unsigned seed = 7u; // => same PRNG seed as cache.c -- reproducible, matching dataset
    for (int i = 0; i < N; i++) {
        seed = seed * 1103515245u + 12345u;              // => same LCG step as cache.c, applied in the same loop order
        soa.sensor_id[i] = (int32_t)(i % 4096);          // => same formula as cache.c's records[i].sensor_id
        soa.reading[i] = (float)(seed % 10000u) * 0.01f; // => same formula as cache.c's records[i].reading
                                                         // -- must match bit-for-bit
        for (int k = 0; k < 112; k++)
            soa.location[i][k] = 0;          // => same zero-fill as cache.c's memset on the AoS field
        soa.timestamp[i] = 1700000000LL + i; // => same formula as cache.c's records[i].timestamp
    }

    size_t total_bytes = (sizeof(int32_t) + sizeof(float) + 112 + sizeof(int64_t)) * (size_t)N; // => co-17: same total byte count as cache.c's AoS -- only the
                                                                                                // arrangement differs
    printf("dataset: N=%d records, SoA total = %.1f MB (same 4 fields as "
           "cache.c, held as 4 dense arrays)\n",
           N, (double)total_bytes / 1e6);

    double result;
    double secs = best_of_seconds(&result, soa.reading,
                                  N); // => only soa.reading is passed -- the hot
                                      // loop never sees the cold arrays
    printf("SoA (cache-friendly) average_reading: best of %d = %.4f s, "
           "result=%.6f\n",
           TRIALS, secs, result);

    free(soa.sensor_id); // => release all four arrays -- symmetric with the four
                         // mallocs above
    free(soa.reading);
    free(soa.location);
    free(soa.timestamp);
    return 0;
}
