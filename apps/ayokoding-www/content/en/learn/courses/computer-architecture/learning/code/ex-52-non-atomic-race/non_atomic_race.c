// learning/code/ex-52-non-atomic-race/non_atomic_race.c
/* Example 52: increment a shared PLAIN (non-atomic) counter from N threads
   -- verify the total undercounts, a real, reproducible data race (co-24). */
#include <pthread.h> // => co-24: pthread_create/join -- the concurrent writer threads under test
#include <stdio.h>   // => printf -- the total/FAIL(-by-design) report this program prints

#define NTHREADS 8                // => co-24: SAME thread count as ex-51, for a direct, fair comparison
#define ITERS_PER_THREAD 2000000L // => co-24: SAME iteration count as ex-51

volatile long counter = 0; // => co-24: PLAIN read-modify-write, no atomicity -- volatile only
                           // forces
                           //    each read/write to really happen (defeats the compiler collapsing
                           //    the whole loop into a single `counter += ITERS`); it does NOT make
                           //    the read-modify-write sequence atomic across threads. This is a
                           //    REAL, intentional data race, included to demonstrate the failure
                           //    mode -- see co-24's own note: "false sharing silently kills
                           //    scaling", and here a race silently kills CORRECTNESS.

static void *worker(void *arg) {                  // defines worker(): helper function used by this example
    (void)arg;                                    // discards arg to silence an unused-variable warning
    for (long i = 0; i < ITERS_PER_THREAD; i++) { // loop header controlling the sweep below
        counter = counter + 1;                    // => co-24: READ counter, ADD 1, WRITE counter --
    } //    THREE separate steps another thread's own
    return NULL; //    read/add/write can interleave with, losing updates
}

int main(void) {                 // program entry point
    pthread_t threads[NTHREADS]; // declares threads
    for (int i = 0; i < NTHREADS; i++)
        pthread_create(&threads[i], NULL, worker, NULL); // => co-24: launch
    for (int i = 0; i < NTHREADS; i++)
        pthread_join(threads[i], NULL); // => co-24: join all

    long expected = (long)NTHREADS * ITERS_PER_THREAD; // => co-24: the mathematically correct total
    long actual = counter;                             // => co-24: read the final (likely wrong) value
    printf("threads=%d, iters/thread=%ld, expected=%ld, actual=%ld\n", NTHREADS,
           ITERS_PER_THREAD,       // prints a report line
           expected, actual);      // continues the printf(...) call above
    long lost = expected - actual; // => co-24: how many increments vanished
    printf("lost updates: %ld (%.2f%% of expected)\n", lost,
           100.0 * (double)lost / (double)expected); // prints a report line
    printf("undercounts (a real, reproducible race): %s -> %s\n",
           (actual < expected) ? "yes" : "no", // prints a report line
           (actual < expected) ? "PASS (this example's point IS the undercount -- "
                                 "confirmed)" // continues the printf(...) call above
                               : "FAIL (no undercount observed this run -- see "
                                 "prose: run-to-run " // continues the printf(...)
                                                      // call above
                                 "variance is expected, the race itself is what's "
                                 "reproducible)"); // continues the printf(...) call
                                                   // above
    // co-24: this program's "PASS" means the race WAS observed (actual <
    // expected) -- exit 0 either way, since the point is demonstrating the
    // hazard, not asserting a fixed exact count.
    return 0; // returns the computed result
}
