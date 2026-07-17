// learning/code/ex-76-atomic-vs-mutex-throughput/atomic_vs_mutex.c
/* Example 76: a CAS-based atomic counter vs a mutex-protected counter under low
 * contention. */
#include <pthread.h>   // pthread.h: standard library header
#include <stdatomic.h> // stdatomic.h: standard library header
#include <stdio.h>     // stdio.h: standard library header
#include <time.h>      // time.h: standard library header

#define THREADS \
    4                                   // => co-24: this machine has 12 logical CPUs -- 4 keeps genuine
                                        // parallelism without saturating every core, the "low contention" case
#define INCREMENTS_PER_THREAD 20000000L // => co-24: 20M increments/thread = 80M total per benchmark

// ex-76: ATOMIC counter -- `_Atomic long` with `atomic_fetch_add_explicit`.
// co-24: on arm64 this compiles to a hardware LSE atomic instruction
// (`ldaddal`) or a tight LL/SC (`ldxr`/`stxr`) retry loop -- either way, the
// increment happens WITHOUT ever leaving user space or invoking the kernel.
static _Atomic long atomic_counter = 0; // supporting statement for this example

static void *worker_atomic(void *arg) { // defines worker_atomic(): helper
                                        // function used by this example
    long n = (long)(intptr_t)arg;       // declares n
    for (long i = 0; i < n; i++) {      // loop header controlling the sweep below
        atomic_fetch_add_explicit(&atomic_counter, 1,
                                  memory_order_relaxed); // => co-24: lock-free increment
    }
    return NULL; // returns the computed result
}

// ex-76: MUTEX-protected counter -- a PLAIN (non-atomic) `long`, but every
// increment is wrapped in `pthread_mutex_lock`/`unlock`. co-24: under LOW
// contention, `pthread_mutex_lock` on most modern libc implementations is often
// a userspace fast-path CAS itself when uncontended -- but it STILL costs more
// than a bare atomic op: extra function-call overhead, a full memory fence
// either way, and a slower path (potentially a real futex/kernel syscall) the
// moment two threads truly collide.
static long mutex_counter = 0;                                    // declares mutex_counter
static pthread_mutex_t counter_mutex = PTHREAD_MUTEX_INITIALIZER; // declares counter_mutex

static void *worker_mutex(void *arg) {        // defines worker_mutex(): helper function used by this example
    long n = (long)(intptr_t)arg;             // declares n
    for (long i = 0; i < n; i++) {            // loop header controlling the sweep below
        pthread_mutex_lock(&counter_mutex);   // => co-24: acquire -- may fast-path,
                                              // may not, under contention
        mutex_counter++;                      // => co-24: the actual (now serialized) increment
        pthread_mutex_unlock(&counter_mutex); // => co-24: release
    }
    return NULL; // returns the computed result
}

static double run_threads(void *(*worker)(void *),
                          long increments_per_thread) { // declares function pointer worker
    pthread_t th[THREADS];                              // declares th
    struct timespec t0, t1;                             // supporting statement for this example
    clock_gettime(CLOCK_MONOTONIC, &t0);                // calls clock_gettime(...)
    for (int i = 0; i < THREADS; i++) {                 // loop header controlling the sweep below
        pthread_create(&th[i], NULL, worker,
                       (void *)(intptr_t)increments_per_thread); // calls pthread_create(...)
    }
    for (int i = 0; i < THREADS; i++)
        pthread_join(th[i], NULL);                                    // loop header controlling the sweep below
    clock_gettime(CLOCK_MONOTONIC, &t1);                              // calls clock_gettime(...)
    return (t1.tv_sec - t0.tv_sec) + (t1.tv_nsec - t0.tv_nsec) / 1e9; // returns the computed result
}

int main(void) {                                           // program entry point
    long expected = (long)THREADS * INCREMENTS_PER_THREAD; // declares expected

    double t_atomic = run_threads(worker_atomic, INCREMENTS_PER_THREAD); // declares t_atomic
    long final_atomic = atomic_load(&atomic_counter);                    // declares final_atomic

    double t_mutex = run_threads(worker_mutex, INCREMENTS_PER_THREAD); // declares t_mutex
    long final_mutex = mutex_counter;                                  // declares final_mutex

    double atomic_ops_per_sec = (double)expected / t_atomic;         // declares atomic_ops_per_sec
    double mutex_ops_per_sec = (double)expected / t_mutex;           // declares mutex_ops_per_sec
    double speedup = mutex_ops_per_sec > 0 ? t_mutex / t_atomic : 0; // declares speedup

    printf("THREADS=%d, %ld increments/thread, %ld total increments per benchmark\n",
           THREADS,                          // prints a report line
           INCREMENTS_PER_THREAD, expected); // continues the printf(...) call above
    printf("atomic counter: %.4f s, %.1fM ops/sec (final=%ld, correct=%s)\n",
           t_atomic, // prints a report line
           atomic_ops_per_sec / 1e6, final_atomic,
           final_atomic == expected ? "yes" : "NO -- BUG"); // continues the printf(...) call above
    printf("mutex  counter: %.4f s, %.1fM ops/sec (final=%ld, correct=%s)\n",
           t_mutex, // prints a report line
           mutex_ops_per_sec / 1e6, final_mutex,
           final_mutex == expected ? "yes" : "NO -- BUG");                                  // continues the printf(...) call above
    printf("atomic speedup over mutex: %.2fx\n", speedup);                                  // prints a report line
    int pass = (final_atomic == expected) && (final_mutex == expected) && (speedup > 1.05); // declares pass
    printf("PASS (both counters correct, atomic strictly faster than mutex under "
           "low contention): %s\n", // prints a report line
           pass ? "PASS" : "FAIL"); // continues the printf(...) call above
    return 0;                       // returns the computed result
}
