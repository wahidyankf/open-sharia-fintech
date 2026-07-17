// learning/code/ex-61-parallel-histogram-scaling/histogram.c
/* Example 61: parallel histogram -- shared atomic bins vs per-thread bins. */
#include <pthread.h>   // pthread.h: standard library header
#include <stdatomic.h> // stdatomic.h: standard library header
#include <stdio.h>     // stdio.h: standard library header
#include <stdlib.h>    // stdlib.h: standard library header
#include <time.h>      // time.h: standard library header

#define TOTAL 40000000 // => co-24: 40M keys total, split evenly across threads
#define BINS 256       // => one bucket per byte value
#define THREADS \
    8 // => co-24: this machine has 12 logical CPUs -- 8 leaves headroom for the
      // OS

static unsigned char *keys; // => co-24: shared read-only input, identical for
                            // every variant tested

// ex-61: SHARED bins -- every thread atomically increments the SAME 256-int
// array. co-02: 256 ints = 1024 bytes = 8 cache lines on this 128 B-line
// machine, so with 8 threads hammering essentially the whole array, most
// increments collide with another thread's recent write to the SAME line (false
// sharing) even when they hit different bins.
static _Atomic int shared_hist[BINS]; // supporting statement for this example

typedef struct {
    int id;
    long start;
    long count;
} Range; // performs several bookkeeping updates in one line

static void *worker_shared(void *arg) {                     // defines worker_shared(): helper
                                                            // function used by this example
    Range *r = (Range *)arg;                                // declares r
    for (long i = r->start; i < r->start + r->count; i++) { // loop header controlling the sweep below
        atomic_fetch_add_explicit(&shared_hist[keys[i]], 1,
                                  memory_order_relaxed); // => co-24: contends
    }
    return NULL; // returns the computed result
}

// ex-61: PER-THREAD bins -- each thread owns a private 256-int row in a
// [THREADS][BINS] array and touches ONLY its own row -- co-24: zero
// cross-thread cache-line traffic during the counting phase; the only shared
// step is the cheap single-threaded merge at the end.
static int per_thread_hist[THREADS][BINS]; // supporting statement for this example

static void *worker_local(void *arg) {                      // defines worker_local(): helper function used by this example
    Range *r = (Range *)arg;                                // declares r
    int tid = r->id;                                        // declares tid
    for (long i = r->start; i < r->start + r->count; i++) { // loop header controlling the sweep below
        per_thread_hist[tid][keys[i]]++;                    // => co-24: private memory -- no atomic,
                                                            // no contention at all
    }
    return NULL; // returns the computed result
}

// ex-61: a shared thread-spawning-and-timing harness -- taking a worker
// function pointer lets the SAME launch/join/timing code drive either the
// shared-bins worker or the per-thread-bins worker, so the two variants are
// compared under identical scheduling and timing conditions.
static double run_threads(void *(*worker)(void *),
                          int nthreads) {                                          // declares function pointer worker
    pthread_t th[THREADS];                                                         // declares th
    Range ranges[THREADS];                                                         // declares ranges
    long chunk = TOTAL / nthreads;                                                 // declares chunk
    struct timespec t0, t1;                                                        // supporting statement for this example
    clock_gettime(CLOCK_MONOTONIC, &t0);                                           // calls clock_gettime(...)
    for (int i = 0; i < nthreads; i++) {                                           // loop header controlling the sweep below
        ranges[i].id = i;                                                          // assigns ranges[i].id
        ranges[i].start = (long)i * chunk;                                         // assigns ranges[i].start
        ranges[i].count = (i == nthreads - 1) ? (TOTAL - ranges[i].start) : chunk; // last thread takes remainder
        pthread_create(&th[i], NULL, worker,
                       &ranges[i]); // calls pthread_create(...)
    }
    for (int i = 0; i < nthreads; i++)
        pthread_join(th[i], NULL);                                    // loop header controlling the sweep below
    clock_gettime(CLOCK_MONOTONIC, &t1);                              // calls clock_gettime(...)
    return (t1.tv_sec - t0.tv_sec) + (t1.tv_nsec - t0.tv_nsec) / 1e9; // returns the computed result
}

static long total_count(void) { // defines total_count(): helper function used by this example
    long total = 0;             // declares total
    for (int b = 0; b < BINS; b++)
        total += atomic_load(&shared_hist[b]); // loop header controlling the sweep below
    return total;                              // returns the computed result
}
static long total_count_local(void) { // defines total_count_local(): helper function used by this example
    long total = 0;                   // declares total
    for (int t = 0; t < THREADS; t++) // loop header controlling the sweep below
        for (int b = 0; b < BINS; b++)
            total += per_thread_hist[t][b]; // loop header controlling the sweep below
    return total;                           // returns the computed result
}

// ex-61: main() runs THREE timed passes -- a 1-thread baseline, THREADS-way
// shared-bin, and THREADS-way per-thread-bin -- and computes each scaling
// variant's speedup relative to the SAME baseline, so "per-thread scales
// better" is a direct, apples-to-apples ratio comparison.
int main(void) {                               // program entry point
    keys = malloc(TOTAL);                      // heap-allocates memory for keys
    unsigned seed = 7u;                        // declares seed
    for (long i = 0; i < TOTAL; i++) {         // loop header controlling the sweep below
        seed = seed * 1103515245u + 12345u;    // assigns seed
        keys[i] = (unsigned char)(seed >> 16); // => uniform-ish byte values across all 256 bins
    }

    // Baseline: 1 thread, shared-style bins (no contention possible with 1 thread
    // -- the true single-core cost of doing this work at all).
    double t1_baseline = run_threads(worker_shared, 1); // declares t1_baseline
    long count1 = total_count();                        // declares count1

    for (int b = 0; b < BINS; b++)
        atomic_store(&shared_hist[b], 0); // reset for the 8-thread run

    double t_shared8 = run_threads(worker_shared, THREADS); // declares t_shared8
    long count_shared8 = total_count();                     // declares count_shared8

    double t_local8 = run_threads(worker_local, THREADS); // declares t_local8
    long count_local8 = total_count_local();              // declares count_local8

    double speedup_shared = t1_baseline / t_shared8; // declares speedup_shared
    double speedup_local = t1_baseline / t_local8;   // declares speedup_local

    printf("TOTAL=%d keys, BINS=%d, THREADS=%d\n", TOTAL, BINS,
           THREADS); // prints a report line
    printf("1-thread baseline:            %.4f s (count=%ld)\n", t1_baseline,
           count1);                                                                                    // prints a report line
    printf("%d-thread SHARED atomic bins:  %.4f s (count=%ld) -> %.2fx speedup\n", THREADS, t_shared8, // prints a report line
           count_shared8, speedup_shared);                                                             // continues the printf(...) call above
    printf("%d-thread PER-THREAD bins:     %.4f s (count=%ld) -> %.2fx speedup\n", THREADS, t_local8,  // prints a report line
           count_local8, speedup_local);                                                               // continues the printf(...) call above
    int counts_ok = (count1 == TOTAL) && (count_shared8 == TOTAL) && (count_local8 == TOTAL);          // declares counts_ok
    int pass = counts_ok && (speedup_local > speedup_shared);                                          // declares pass
    printf("PASS (all counts correct, per-thread scales better than shared): %s\n",
           pass ? "PASS" : "FAIL"); // prints a report line
    return 0;                       // returns the computed result
}
