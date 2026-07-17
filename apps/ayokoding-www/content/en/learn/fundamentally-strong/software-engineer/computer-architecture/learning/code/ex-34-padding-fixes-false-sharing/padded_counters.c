// learning/code/ex-34-padding-fixes-false-sharing/padded_counters.c
/* Example 34: pad two counters onto separate 128 B cache lines -- verify
   ex-33's false-sharing slowdown disappears once each counter owns its own
   line (co-02, co-24). */
#include <pthread.h> // => co-24: pthread_create/join -- the two concurrent writer threads under test
#include <stdio.h>   // => printf -- the sizeof/timing/PASS report this program prints
#include <stdlib.h>  // => calloc/free -- both counter layouts under test are heap-allocated
#include <time.h>    // => clock_gettime -- the portable wall-clock timer used below

#define ITERS \
    100000000L // => co-24: same iteration count as ex-33 -- an apples-to-apples
               // rerun
#define LINE \
    128 // => co-02: THIS machine's real cache line size (128 B on Apple Silicon)
        // --
        //    hardcoding the common 64 B x86 number here would silently under-pad

// co-02: reproduces ex-33's failing case in THIS file too, so ex-34 stays
// self-contained -- two counters with no padding between them, guaranteed to
// share one 128 B line.
typedef struct {              // struct layout definition
    volatile long unpadded_a; // => co-24: volatile -- same collapse-prevention
                              // reasoning as ex-33
    volatile long unpadded_b; // => co-02: 8 bytes after unpadded_a -- same cache
                              // line, by construction
} Unpadded;                   // supporting statement for this example

// co-02: the FIX -- one real counter plus enough padding bytes to fill out a
// whole 128 B line, so that in an ARRAY of these structs, element [1] starts on
// the NEXT cache line instead of a few bytes into element [0]'s line.
typedef struct {                   // struct layout definition
    volatile long value;           // => co-24: the one real counter this struct holds
    char pad[LINE - sizeof(long)]; // => co-16: deliberate, performance-motivated
                                   // struct padding --
} PaddedCounter;                   //    120 filler bytes so sizeof(PaddedCounter) == 128 exactly

static void *inc_long(void *arg) {           // => co-24: one shared thread body for BOTH experiments
    volatile long *p = (volatile long *)arg; // => co-24: works on any single volatile long address
    for (long i = 0; i < ITERS; i++)
        (*p)++;  // => co-24: real load+add+store every iteration
    return NULL; // returns the computed result
}

static double now_seconds(void) {                        // => co-25: shared wall-clock helper, this topic's standard pattern
    struct timespec ts;                                  // supporting statement for this example
    clock_gettime(CLOCK_MONOTONIC, &ts);                 // calls clock_gettime(...)
    return (double)ts.tv_sec + (double)ts.tv_nsec / 1e9; // returns the computed result
}

static double run_two(volatile long *a,
                      volatile long *b) { // => co-24: times two threads
                                          // hammering a/b concurrently
    pthread_t t1, t2;                     // declares t1
    double t0 = now_seconds();            // declares t0
    pthread_create(&t1, NULL, inc_long,
                   (void *)a); // => co-24: thread 1 increments *a
    pthread_create(&t2, NULL, inc_long,
                   (void *)b); // => co-24: thread 2 increments *b, concurrently
    pthread_join(t1, NULL);    // calls pthread_join(...)
    pthread_join(t2, NULL);    // calls pthread_join(...)
    return now_seconds() - t0; // => co-25: total wall-clock for both threads combined
}

int main(void) {                                                                  // program entry point
    printf("sizeof(PaddedCounter) = %zu bytes (padded to one %d B cache line)\n", // prints a report line
           sizeof(PaddedCounter),
           LINE); // => co-16: prove the padding actually landed at 128

    Unpadded *u = calloc(1, sizeof(Unpadded)); // => co-02: false-sharing baseline, reproduced here
    if (!u) {
        fprintf(stderr, "alloc failed\n");
        return 1;
    } // prints a report line
    double t_unpadded = run_two(&u->unpadded_a, &u->unpadded_b); // => co-24: ex-33's slow case, rerun

    PaddedCounter *p = calloc(2,
                              sizeof(PaddedCounter)); // => co-02: array of 2 -- p[1] starts a WHOLE line
    if (!p) {
        fprintf(stderr, "alloc failed\n");
        return 1;
    } //    after p[0], by the padding above
    double t_padded = run_two(&p[0].value,
                              &p[1].value); // => co-24: the FIXED case -- no shared line at all

    printf("unpadded (false-sharing) pair: %.4f s\n",
           t_unpadded); // => co-24: reproduces ex-33's slow number
    printf("padded (own cache line each):  %.4f s\n",
           t_padded);                                                           // => co-24: the fixed, fast number
    double speedup = t_unpadded / t_padded;                                     // => co-24: how much the padding fix recovered
    printf("padding speedup: %.2fx -> %s\n", speedup,                           // prints a report line
           speedup > 1.3 ? "PASS (padding fix removes the slowdown)" : "FAIL"); // => co-25: self-judged PASS/FAIL
    free(u);                                                                    // => release the false-sharing baseline struct
    free(p);                                                                    // => release the padded-counter array
    return speedup > 1.3 ? 0 : 1;                                               // => real process exit code reflecting the PASS/FAIL
}
