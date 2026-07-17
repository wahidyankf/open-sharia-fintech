// learning/code/ex-33-false-sharing-demo/false_sharing.c
/* Example 33: two threads increment adjacent longs sharing one 128 B cache
   line vs longs placed on separate cache lines -- verify a real, measured
   slowdown from false sharing (co-02, co-24). */
#include <pthread.h> // => co-24: pthread_create/join -- the two concurrent writer threads under test
#include <stdio.h>   // => printf -- the timing/PASS report this program prints
#include <stdlib.h>  // => calloc/free -- the shared buffer both counter pairs live inside
#include <time.h>    // => clock_gettime -- the portable wall-clock timer used below

#define ITERS \
    100000000L          // => co-24: 100M increments/thread -- large enough for a stable
                        // timing signal
#define STRIDE_LONGS 32 // => co-02: 32 * 8 B = 256 B -- guarantees two DIFFERENT 128 B cache lines

// co-24: a pair of pointers, not two named fields -- lets run_pair() reuse ONE
// thread body for both the "same line" and "different line" experiments below,
// varying only which addresses inside one shared buffer the two threads are
// told to hammer.
typedef struct {
    volatile long *a; // => co-24: volatile is load-bearing here -- without it
                      // clang can prove no other
    volatile long *b; //    thread observes intermediate values and collapse the
                      //    loop to `*a += ITERS`
} Pair;               //    once, which would silently delete the false-sharing traffic this
                      //    measures

static void *inc_a(void *arg) { // => co-24: thread body -- increments *only* a
    Pair *p = (Pair *)arg;      // => co-24: recover the shared pointer pair
    for (long i = 0; i < ITERS; i++)
        (*p->a)++; // => co-24: real load+add+store every iteration --
    return NULL;   //    contended by thread B's writes if a/b share a line
}
static void *inc_b(void *arg) { // => co-24: thread body -- increments *only* b
    Pair *p = (Pair *)arg;      // => co-24: same struct, opposite field
    for (long i = 0; i < ITERS; i++)
        (*p->b)++; // => co-24: identical work to inc_a, mirrored
    return NULL;
}

static double now_seconds(void) { // => co-25: shared wall-clock helper, this topic's standard pattern
    struct timespec ts;           // => POSIX timespec: seconds + nanoseconds
    clock_gettime(CLOCK_MONOTONIC,
                  &ts);                                  // => monotonic -- immune to wall-clock adjustment mid-run
    return (double)ts.tv_sec + (double)ts.tv_nsec / 1e9; // => combined into one double-seconds value
}

// co-24: spins up both writer threads on the SAME pair of addresses, times
// wall-clock from before creation to after both joins -- the two-core
// contention IS the measurement.
static double run_pair(volatile long *a, volatile long *b) {
    Pair p = {a, b}; // => co-24: bundle both target addresses once
    pthread_t t1,
        t2;                               // => co-24: two OS threads -- real concurrency, not simulated
    double t0 = now_seconds();            // => co-25: start the clock before either thread exists
    pthread_create(&t1, NULL, inc_a, &p); // => co-24: thread 1 hammers *a
    pthread_create(&t2, NULL, inc_b,
                   &p); // => co-24: thread 2 hammers *b, concurrently
    pthread_join(t1,
                 NULL); // => co-24: block until thread 1's 100M increments finish
    pthread_join(t2,
                 NULL);        // => co-24: block until thread 2's 100M increments finish
    return now_seconds() - t0; // => co-25: total wall-clock for both threads combined
}

int main(void) {
    // co-02: one big buffer -- WE control offsets directly instead of trusting
    // malloc's internal placement, so the "same line" vs "different line" claim
    // is exact, not assumed.
    long *buf = calloc(1024, sizeof(long)); // => 8 KB buffer, zero-initialized counters
    if (!buf) {
        fprintf(stderr, "alloc failed\n");
        return 1;
    } // => fail loudly, never time a null pointer

    // co-02: offsets 0 and 1 are 8 bytes apart -- both land inside the SAME 128 B
    // line
    double t_adjacent = run_pair((volatile long *)&buf[0], (volatile long *)&buf[1]);
    // co-02: offsets 0 and STRIDE_LONGS are 256 bytes apart -- two DIFFERENT 128
    // B lines
    double t_separate = run_pair((volatile long *)&buf[0], (volatile long *)&buf[STRIDE_LONGS]);

    printf("adjacent (false-sharing) pair:     %.4f s\n",
           t_adjacent); // => co-24: same-line timing
    printf("separate (independent-line) pair:  %.4f s\n",
           t_separate);                        // => co-24: different-line timing
    double slowdown = t_adjacent / t_separate; // => co-24: how many times slower sharing a line was
    printf("false-sharing slowdown: %.2fx -> %s\n", slowdown,
           slowdown > 1.3 ? "PASS (adjacent measurably slower)" : "FAIL"); // => co-25: program judges its own claim
    free(buf);                                                             // => release the 8 KB shared buffer
    return slowdown > 1.3 ? 0 : 1;                                         // => real process exit code reflecting the PASS/FAIL
}
