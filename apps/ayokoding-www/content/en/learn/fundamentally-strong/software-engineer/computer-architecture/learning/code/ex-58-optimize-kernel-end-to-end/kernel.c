// learning/code/ex-58-optimize-kernel-end-to-end/kernel.c
/* Example 58: profile a slow kernel, fix its layout, re-measure. */
#include <stdio.h>  // => printf: report the profile-fix-reprofile transcript
#include <stdlib.h> // => malloc/free/rand: build and free the synthetic dataset
#include <string.h> // => memset: fill the "cold" bytes so the record is realistic, not zeroed noise
#include <time.h>   // => clock_gettime: the wall-clock stopwatch this whole example is built on

#define N \
    4000000 // => co-25: 4M records -- large enough that layout dominates over
            // instruction count
#define TRIALS \
    5 // => co-25: best-of-N wall-clock timing, per this topic's measurement
      // methodology

// ex-58: a deliberately realistic "record" -- one HOT field (grade) the kernel
// actually needs, wrapped in COLD fields (a padded name buffer and metadata)
// nobody touches in this kernel -- exactly the shape a real "student record" or
// "log event" struct takes co-17: this struct's shape, not the loop's
// instruction count, is what ex-58 optimizes
typedef struct {       // struct layout definition
    int grade;         // => co-17: the ONE field the average-grade kernel actually reads
    char name[124];    // => co-17: COLD -- padded to make the record one full 128 B
                       // cache line
    int enrolled_year; // => co-17: COLD -- never read by this kernel, still paid
                       // for every cache line
} StudentRecord;       // => sizeof == 132 bytes: crosses more than one 128 B cache
                       // line per record

// ex-58: the ORIGINAL kernel -- walks the array-of-structs, reading `grade` out
// of every full 132-byte record even though 128 of those bytes are dead weight
// for this computation
static double average_grade_aos(const StudentRecord *records,
                                int n) { // => co-17: cache-hostile pass
    long sum = 0;                        // => accumulate as long: N * max_grade never overflows int
    for (int i = 0; i < n; i++) {        // => co-17: one full 132 B record loaded per iteration...
        sum += records[i].grade;         // => ...to read 4 of those 132 bytes -- the rest
                                         // is wasted traffic
    }
    return (double)sum / n; // => co-25: the "profile" step's number-to-explain
}

// ex-58: the FIXED kernel -- given a pre-extracted compact `int grade[]` array
// (SoA for just the field this computation needs), the exact same arithmetic
// runs over dense, fully cache-line-packed data: co-02 -- every 128 B line now
// holds 32 real `grade` values
static double average_grade_soa(const int *grade,
                                int n) { // => co-17: cache-friendly pass
    long sum = 0;                        // => same accumulator type, same arithmetic -- ONLY layout changed
    for (int i = 0; i < n; i++) {        // => co-03: sequential dense reads, 32 useful ints per line
        sum += grade[i];                 // updates sum
    }
    return (double)sum / n; // => must equal average_grade_aos's result bit-for-bit (both are
} // integer sums divided once -- no floating-point reordering risk)

static double best_of_seconds(double (*fn)(const void *, int), const void *data,
                              int n) {       // declares function pointer fn
    double best = -1.0;                      // => co-25: best-of-N methodology -- report the fastest clean run,
    for (int t = 0; t < TRIALS; t++) {       // not a single noisy sample, per this topic's measurement rule
        struct timespec t0, t1;              // supporting statement for this example
        clock_gettime(CLOCK_MONOTONIC, &t0); // calls clock_gettime(...)
        volatile double result = fn(data,
                                    n);                                          // => volatile: stop the optimizer from deleting the "unused" call
        clock_gettime(CLOCK_MONOTONIC, &t1);                                     // calls clock_gettime(...)
        (void)result;                                                            // => silence "unused variable" -- the volatile read is the
                                                                                 // real guard
        double secs = (t1.tv_sec - t0.tv_sec) + (t1.tv_nsec - t0.tv_nsec) / 1e9; // declares secs
        if (best < 0 || secs < best)
            best = secs; // => keep the fastest of TRIALS runs
    }
    return best; // returns the computed result
}

// ex-58: thin typed wrappers so best_of_seconds can call either kernel through
// one function-pointer signature -- co-25: this is scaffolding for the
// STOPWATCH, not the kernel itself
static double wrap_aos(const void *p,
                       int n) {                        // defines wrap_aos(): helper function used by this example
    const StudentRecord *r = (const StudentRecord *)p; // declares r
    return average_grade_aos(r, n);                    // returns the computed result
}
static double wrap_soa(const void *p,
                       int n) {     // defines wrap_soa(): helper function used by this example
    const int *g = (const int *)p;  // declares g
    return average_grade_soa(g, n); // returns the computed result
}

int main(void) { // program entry point
    // Step 1 ("profile a slow kernel"): build the realistic AoS dataset a real
    // system would hand you.
    StudentRecord *records = malloc(sizeof(StudentRecord) * N); // => co-17: 132 B * 4M ~= 528 MB AoS
    if (!records) {
        fprintf(stderr, "alloc failed\n");
        return 1;
    } // prints a report line
    unsigned seed = 12345u;                    // => co-25: fixed seed -- reproducible dataset every run
    for (int i = 0; i < N; i++) {              // loop header controlling the sweep below
        seed = seed * 1103515245u + 12345u;    // => a tiny deterministic LCG, no <stdlib.h> rand() state
        records[i].grade = (int)(seed % 101u); // grades 0..100
        memset(records[i].name, 'x',
               sizeof(records[i].name));                    // => cold bytes: realistic non-zero payload
        records[i].enrolled_year = 2020 + (int)(seed % 6u); // cold field, never read by the kernel
    }

    double aos_secs = best_of_seconds(wrap_aos, records, N); // => co-25: profile step -- measure the slow path
    double aos_avg = average_grade_aos(records, N);          // => capture the actual numeric result too

    // Step 2 ("fix its layout"): extract just the hot field into a dense SoA
    // buffer.
    int *grade = malloc(sizeof(int) * N); // => co-17: 4 B * 4M = 16 MB -- 33x smaller footprint than AoS
    if (!grade) {
        fprintf(stderr, "alloc failed\n");
        return 1;
    } // prints a report line
    for (int i = 0; i < N; i++)
        grade[i] = records[i].grade; // => the one-time extraction cost (not timed)

    // Step 3 ("re-measure"): profile the fixed kernel with the identical
    // stopwatch.
    double soa_secs = best_of_seconds(wrap_soa, grade, N); // => co-25: re-profile step -- measure the fix
    double soa_avg = average_grade_soa(grade, N);          // declares soa_avg

    printf("dataset: N=%d records, sizeof(StudentRecord)=%zu bytes (%.1f MB "
           "total AoS)\n", // prints a report line
           N, sizeof(StudentRecord),
           (double)(sizeof(StudentRecord) * N) / (1024.0 * 1024.0));                                    // continues the printf(...) call above
    printf("step 1 (profile)  AoS average_grade: best of %d = %.4f s, result=%.6f\n", TRIALS, aos_secs, // prints a report line
           aos_avg);                                                                                    // continues the printf(...) call above
    printf("step 3 (reprofile) SoA average_grade: best of %d = %.4f s, "
           "result=%.6f\n",
           TRIALS, soa_secs, // prints a report line
           soa_avg);         // continues the printf(...) call above
    printf("results identical: %s (both %.10f)\n", (aos_avg == soa_avg) ? "yes" : "NO -- BUG",
           aos_avg);                      // prints a report line
    double speedup = aos_secs / soa_secs; // declares speedup
    printf("speedup: %.2fx  (PASS: SoA faster with identical result) -> %s\n",
           speedup,                                                   // prints a report line
           (aos_avg == soa_avg && speedup > 1.05) ? "PASS" : "FAIL"); // continues the printf(...) call above

    free(records); // releases records's heap memory
    free(grade);   // releases grade's heap memory
    return 0;      // returns the computed result
}
