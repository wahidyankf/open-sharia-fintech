// learning/code/ex-51-atomic-increment/atomic_increment.c
/* Example 51: increment a shared _Atomic counter from N threads -- verify
   no updates are lost (co-24). */
#include <pthread.h>   // => co-24: pthread_create/join -- the concurrent writer threads under test
#include <stdatomic.h> // => co-24: _Atomic/atomic_fetch_add -- the hardware-backed atomic RMW operation
#include <stdio.h>     // => printf -- the total/PASS report this program prints

#define NTHREADS 8 // => co-24: 8 threads -- this machine has 12 logical CPUs, real contention
#define ITERS_PER_THREAD \
    2000000L // => co-24: 2M increments/thread -- large enough to make a lost
             //    update virtually certain to appear if atomicity were violated

_Atomic long counter = 0; // => co-24: a single, hardware-atomic shared counter
                          // -- every increment is
                          //    a genuine atomic read-modify-write instruction
                          //    (LDXR/STXR or CAS-loop under the hood on arm64),
                          //    never a plain non-atomic load+add+store

static void *worker(void *arg) {                  // defines worker(): helper function used by this example
    (void)arg;                                    // discards arg to silence an unused-variable warning
    for (long i = 0; i < ITERS_PER_THREAD; i++) { // loop header controlling the sweep below
        atomic_fetch_add(&counter,
                         1); // => co-24: atomic RMW -- indivisible from every
    } //    OTHER thread's view, no matter how they interleave
    return NULL; // returns the computed result
}

int main(void) {                 // program entry point
    pthread_t threads[NTHREADS]; // declares threads
    for (int i = 0; i < NTHREADS; i++)
        pthread_create(&threads[i], NULL, worker, NULL); // => co-24: launch
    for (int i = 0; i < NTHREADS; i++)
        pthread_join(threads[i], NULL); // => co-24: join all

    long expected = (long)NTHREADS * ITERS_PER_THREAD; // => co-24: the mathematically correct total
    long actual = atomic_load(&counter);               // => co-24: read the final value, atomically
    printf("threads=%d, iters/thread=%ld, expected=%ld, actual=%ld\n", NTHREADS,
           ITERS_PER_THREAD,  // prints a report line
           expected, actual); // continues the printf(...) call above
    printf("no updates lost: %s -> %s\n",
           (actual == expected) ? "yes" : "no",                                      // prints a report line
           (actual == expected) ? "PASS (atomic counter exactly correct)" : "FAIL"); // continues the printf(...) call above
    return (actual == expected) ? 0 : 1;                                             // returns the computed result
}
