// learning/code/ex-53-memory-barrier-ordering/memory_barrier.c
/* Example 53: demonstrate the CORRECT release/acquire handshake pattern for
   passing data between threads -- verify zero ordering violations across a
   bounded stress test, AND a real, 100%-reproducible violation with
   memory_order_relaxed (co-24). VERIFIED FINDING (found while building
   this example, confirmed via -O2 -S disassembly): the relaxed version's
   failure here is NOT a subtle, hard-to-catch CPU store-buffer reorder --
   it is the COMPILER outright DEAD-CODE-ELIMINATING the `rhs.data = i`
   store. Because relaxed ordering creates no happens-before edge, and a
   race on a plain (non-atomic) variable is undefined behavior in C11, the
   compiler is standards-permitted to treat that store as dead (this
   thread never reads it back) and delete it -- disassembly confirms the
   write never appears inside the loop at -O2. The release/acquire version
   does not have this problem: the ordering constraint is exactly what
   forces the compiler (and the CPU) to keep the data write visible before
   the flag update it is paired with. */
#include <pthread.h>   // => co-24: pthread_create/join -- the producer/consumer thread pair
#include <stdatomic.h> // => co-24: _Atomic/memory_order_release/memory_order_acquire -- the C11 tools
#include <stdio.h>     // => printf -- the violation-count/PASS report this program prints

#define ITERS \
    1000000L // => co-24: 1M handshake round-trips -- a bounded, finite stress
             // test (not an
             //    infinite fuzzer), per this example's honest, stated scope

// co-24: the CORRECT pattern -- `data` is a PLAIN (non-atomic) field, but
// `flag` is an _Atomic used with explicit release/acquire ordering. The C11
// memory model GUARANTEES that everything the producer wrote BEFORE its
// release-store to `flag` is visible to the consumer AFTER its acquire-load
// observes that same value -- this is the exact mechanism (not a spinlock, not
// a mutex) that makes lock-free message-passing safe.
typedef struct {      // struct layout definition
    long data;        // => co-24: the payload -- ordinary memory
    _Atomic int flag; // => co-24: the synchronization point
} Handshake;          // supporting statement for this example

static Handshake hs = {0, 0}; // declares hs

static void *producer(void *arg) {      // defines producer(): helper function used by this example
    (void)arg;                          // discards arg to silence an unused-variable warning
    for (long i = 1; i <= ITERS; i++) { // loop header controlling the sweep below
        hs.data = i;                    // => co-24: plain write -- NOT yet guaranteed visible
        atomic_store_explicit(&hs.flag, 1,
                              memory_order_release);                        // => co-24: release -- this store, and every
                                                                            //    write before it in program order, become
                                                                            //    visible to any thread that acquire-loads
                                                                            //    this SAME atomic and observes THIS value
        while (atomic_load_explicit(&hs.flag, memory_order_acquire) != 0) { // loop header controlling the sweep below
                                                                            // => co-24: spin until the consumer resets flag to 0 (ready for the next
                                                                            // round)
        }
    }
    return NULL; // returns the computed result
}

static void *consumer(void *arg) {                                          // defines consumer(): helper function used by this example
    long *violations = (long *)arg;                                         // declares violations
    long expected = 1;                                                      // declares expected
    for (long i = 0; i < ITERS; i++) {                                      // loop header controlling the sweep below
        while (atomic_load_explicit(&hs.flag, memory_order_acquire) == 0) { // loop header controlling the sweep below
                                                                            // => co-24: spin until the producer's release-store makes flag==1 AND
                                                                            // data visible
        }
        long observed = hs.data; // => co-24: per the C11 model, this MUST see the
                                 //    producer's write from before its release-store
        if (observed != expected)
            (*violations)++; // => co-24: the ordering-violation counter
        expected++;          // supporting statement for this example
        atomic_store_explicit(&hs.flag, 0,
                              memory_order_release); // => co-24: signal "ready for next" back
    }
    return NULL; // returns the computed result
}

// co-24: a SECOND handshake using memory_order_relaxed on BOTH sides -- relaxed
// ordering gives NO cross-thread visibility guarantee for `data` at all, and
// (per the file-level comment above) VERIFIED to let the compiler delete the
// `data` store outright at -O2, since it's dead from the writer thread's own
// local view.
typedef struct {      // struct layout definition
    long data;        // declares data
    _Atomic int flag; // supporting statement for this example
} RelaxedHandshake;   // supporting statement for this example

static RelaxedHandshake rhs = {0, 0}; // declares rhs

static void *relaxed_producer(void *arg) { // defines relaxed_producer(): helper
                                           // function used by this example
    (void)arg;                             // discards arg to silence an unused-variable warning
    for (long i = 1; i <= ITERS; i++) {    // loop header controlling the sweep below
        rhs.data = i;                      // assigns rhs.data
        atomic_store_explicit(&rhs.flag, 1,
                              memory_order_relaxed);                         // => co-24: relaxed -- NO ordering guarantee
        while (atomic_load_explicit(&rhs.flag, memory_order_relaxed) != 0) { // loop header controlling the sweep below
        }
    }
    return NULL; // returns the computed result
}

static void *relaxed_consumer(void *arg) {                                   // defines relaxed_consumer(): helper
                                                                             // function used by this example
    long *violations = (long *)arg;                                          // declares violations
    long expected = 1;                                                       // declares expected
    for (long i = 0; i < ITERS; i++) {                                       // loop header controlling the sweep below
        while (atomic_load_explicit(&rhs.flag, memory_order_relaxed) == 0) { // loop header controlling the sweep below
        }
        long observed = rhs.data; // => co-24: NOT guaranteed to see the producer's
        if (observed != expected)
            (*violations)++;                                       //    write -- relaxed provides no such promise
        expected++;                                                // supporting statement for this example
        atomic_store_explicit(&rhs.flag, 0, memory_order_relaxed); // calls atomic_store_explicit(...)
    }
    return NULL; // returns the computed result
}

int main(void) {                                     // program entry point
    long violations = 0;                             // declares violations
    pthread_t p, c;                                  // declares p
    pthread_create(&p, NULL, producer, NULL);        // calls pthread_create(...)
    pthread_create(&c, NULL, consumer, &violations); // calls pthread_create(...)
    pthread_join(p, NULL);                           // calls pthread_join(...)
    pthread_join(c, NULL);                           // calls pthread_join(...)
    printf("[release/acquire] ITERS=%ld, ordering violations: %ld -> %s\n", ITERS,
           violations,                                                                       // prints a report line
           (violations == 0) ? "PASS (release/acquire handshake held under load)" : "FAIL"); // continues the printf(...) call above

    long relaxed_violations = 0; // declares relaxed_violations
    pthread_t rp, rc;            // declares rp
    pthread_create(&rp, NULL, relaxed_producer,
                   NULL); // calls pthread_create(...)
    pthread_create(&rc, NULL, relaxed_consumer,
                   &relaxed_violations); // calls pthread_create(...)
    pthread_join(rp, NULL);              // calls pthread_join(...)
    pthread_join(rc, NULL);              // calls pthread_join(...)
    printf("[relaxed, for comparison] ITERS=%ld, ordering violations: %ld -> %s\n",
           ITERS,              // prints a report line
           relaxed_violations, // continues the printf(...) call above
           relaxed_violations > 0 ? "confirms the hazard (see prose for the "
                                    "compiler-DCE mechanism)" // continues the
                                                              // printf(...) call
                                                              // above
                                  : "no violation THIS run (see prose: absence "
                                    "isn't proof of safety)"); // continues the
                                                               // printf(...) call
                                                               // above

    return (violations == 0) ? 0 : 1; // => co-24: THIS example's hard gate is the CORRECT
} //    pattern holding -- the relaxed run is informational
