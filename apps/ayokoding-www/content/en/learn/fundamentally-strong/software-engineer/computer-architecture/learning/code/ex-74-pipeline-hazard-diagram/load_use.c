// learning/code/ex-74-pipeline-hazard-diagram/load_use.c
/* Example 74: measuring a real load-use pipeline stall (chained vs independent
 * loads). */
#include <stdio.h>  // stdio.h: standard library header
#include <stdlib.h> // stdlib.h: standard library header
#include <time.h>   // time.h: standard library header

// co-20: 2048 ints = 8 KB -- comfortably inside this machine's 64 KiB L1d, so
// BOTH benchmarks below stay entirely L1-resident. That is deliberate: the goal
// is to isolate the LOAD-USE pipeline hazard's forwarding delay itself, not to
// re-measure a cache-miss cost (that is ex-28's job).
#define ARR_N 2048 // constant ARR_N = 2048
#define ITERS \
    200000000L // => co-20: repeat the (small) chain/stream this many times for a
               // stable measurement

// ex-74: DEPENDENT chain -- `idx = perm[idx]` makes each load's ADDRESS depend
// on the PREVIOUS load's VALUE. co-20: the CPU cannot even begin computing the
// next load's address until this load's result has been produced and forwarded
// -- this is the textbook load-use hazard: the consuming instruction (the next
// load) needs a value that is not ready until the MEM pipeline stage of the
// instruction before it, forcing a stall no amount of out-of-order issue can
// hide.
__attribute__((noinline)) static long chase_pointer_chain(const int *perm, long iters) { // calls __attribute__(...)
    long idx = 0;                                                                        // declares idx
    for (long i = 0; i < iters; i++) {                                                   // loop header controlling the sweep below
        idx = perm[idx];                                                                 // => co-20: THIS load's address needs the PREVIOUS load's
                                                                                         // result -- serialized
    }
    return idx; // returns the computed result
}

// ex-74: INDEPENDENT loads -- `data[i % ARR_N]` needs only the LOOP COUNTER,
// never a previous load's VALUE. co-20/co-22: the CPU's out-of-order window can
// have several of these loads in flight simultaneously (no load-use dependency
// between them), so their latency OVERLAPS instead of serializing -- exactly
// what the dependent chain above cannot do.
__attribute__((noinline)) static long sum_independent(const int *data, long iters) { // calls __attribute__(...)
    long sum = 0;                                                                    // declares sum
    for (long i = 0; i < iters; i++) {                                               // loop header controlling the sweep below
        sum += data[i % ARR_N];                                                      // => co-22: address depends only on `i`, computable
                                                                                     // arbitrarily far ahead
    }
    return sum; // returns the computed result
}

// ex-74: `fn` is reloaded through a `volatile` function-pointer VARIABLE on
// every trial instead of being called directly through the parameter. This is
// load-bearing, and TWO weaker fixes were tried and rejected first: (1) a plain
// `volatile long result = fn(...)` still let clang fold all 5 trials' calls
// into ONE real computation (chase_pointer_chain/sum_independent are read-only,
// same- argument calls, so clang's call-CSE reused trial 1's result for trials
// 2-5, hoisting the actual work above the trial loop -- verified in the emitted
// assembly: only ONE `bl _chase_pointer_chain` appeared for all 5 timed
// trials); (2) an `asm volatile("" ::: "memory")` compiler barrier around the
// call also did not stop it (the callee's readonly-ness was determined not to
// depend on anything that barrier invalidates). BOTH left every trial after the
// first measuring an empty pair of back-to-back `clock_gettime` calls -- 0.0000
// ns/iter, a benchmarking artifact, not a real number. Routing the call through
// a `volatile` function-pointer VARIABLE works because clang must treat every
// read of a `volatile` variable as a fresh, unpredictable value -- it can no
// longer prove trial 2's call target is "the same known callee" as trial 1's,
// so CSE cannot fire at all.
static double time_ns_per_iter(long (*fn)(const int *, long), const int *arr, long iters,
                               long *out) {               // declares function pointer fn
    struct timespec t0, t1;                               // supporting statement for this example
    double best = -1.0;                                   // declares best
    long result = 0;                                      // declares result
    long (*volatile fn_indirect)(const int *, long) = fn; // => co-20: volatile function-pointer VARIABLE
    for (int trial = 0; trial < 5; trial++) {             // loop header controlling the sweep below
        clock_gettime(CLOCK_MONOTONIC, &t0);              // calls clock_gettime(...)
        result = fn_indirect(arr,
                             iters);                                             // => co-20: a genuinely fresh, non-CSE-able call every trial
        clock_gettime(CLOCK_MONOTONIC, &t1);                                     // calls clock_gettime(...)
        double secs = (t1.tv_sec - t0.tv_sec) + (t1.tv_nsec - t0.tv_nsec) / 1e9; // declares secs
        if (best < 0 || secs < best)
            best = secs; // conditional check
    }
    *out = result;                       // supporting statement for this example
    return (best / (double)iters) * 1e9; // => ns per iteration
}

int main(void) { // program entry point
    // ex-74: a random permutation of 0..ARR_N-1 -- guarantees the dependent chain
    // visits every slot (no short 2-cycle sub-loop an optimizer or predictor
    // could exploit) while staying L1-resident.
    int *perm = malloc(sizeof(int) * ARR_N); // heap-allocates memory for perm
    for (int i = 0; i < ARR_N; i++)
        perm[i] = i;                             // loop header controlling the sweep below
    unsigned seed = 9u;                          // declares seed
    for (int i = ARR_N - 1; i > 0; i--) {        // loop header controlling the sweep below
        seed = seed * 1103515245u + 12345u;      // assigns seed
        int j = (int)(seed % (unsigned)(i + 1)); // declares j
        int tmp = perm[i];
        perm[i] = perm[j];
        perm[j] = tmp; // declares tmp
    }
    int *data = malloc(sizeof(int) * ARR_N); // heap-allocates memory for data
    for (int i = 0; i < ARR_N; i++)
        data[i] = i; // loop header controlling the sweep below

    long chase_result, sum_result; // declares chase_result
    double ns_chase = time_ns_per_iter(chase_pointer_chain, perm, ITERS,
                                       &chase_result); // declares ns_chase
    double ns_indep = time_ns_per_iter(sum_independent, data, ITERS,
                                       &sum_result); // declares ns_indep
    double stall_ns = ns_chase - ns_indep;           // declares stall_ns

    printf("ARR_N=%d ints (L1-resident), ITERS=%ld\n", ARR_N,
           ITERS); // prints a report line
    printf("dependent load-use chain:  %.4f ns/iter (final idx=%ld)\n", ns_chase,
           chase_result); // prints a report line
    printf("independent loads:         %.4f ns/iter (sum=%ld)\n", ns_indep,
           sum_result); // prints a report line
    printf("extra ns/iter attributable to the load-use hazard: %.4f ns\n",
           stall_ns); // prints a report line
    printf("(no cycle counter on macOS -- reported in ns, per this topic's "
           "stated measurement rule;\n"); // prints a report line
    printf(" the Mermaid diagram in this example's markdown labels its stall "
           "bubble with this exact\n");                         // prints a report line
    printf(" measured number, not an invented cycle count)\n"); // prints a report
                                                                // line
    int pass = stall_ns > 0.2;                                  // dependent chain must be measurably, not just noisily, slower
    printf("PASS (dependent load-use chain measurably slower per iteration than "
           "independent loads): %s\n", // prints a report line
           pass ? "PASS" : "FAIL");    // continues the printf(...) call above

    free(perm); // releases perm's heap memory
    free(data); // releases data's heap memory
    return 0;   // returns the computed result
}
