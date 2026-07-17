// learning/code/ex-38-pipeline-dependency-chain/dependency_chain.c
/* Example 38: time a serial dependent add chain vs 4 independent add chains --
   verify the independent version is faster (co-20, co-22). */
#include <stdio.h> // => printf -- the timing/PASS report this program prints
#include <time.h>  // => clock_gettime -- the portable wall-clock timer used below

#define OPS \
    400000000L // => co-20: 400M total increments in EITHER version -- equal total
               // work

static double now_seconds(void) {                        // => co-25: shared wall-clock helper, this topic's standard pattern
    struct timespec ts;                                  // supporting statement for this example
    clock_gettime(CLOCK_MONOTONIC, &ts);                 // calls clock_gettime(...)
    return (double)ts.tv_sec + (double)ts.tv_nsec / 1e9; // returns the computed result
}

// co-20: a pure SERIAL dependency chain -- iteration i+1's `x = x + 1` cannot
// even START until iteration i's result is committed, because it reads the
// value iteration i just wrote. `volatile` forces a real store+load every step
// (not a register-only loop the compiler could fold to `x=OPS`), so this
// exposes the CPU's add latency chained OPS times with NO opportunity for the
// pipeline to overlap independent work.
static long dependent_chain(long ops) { // defines dependent_chain(): helper
                                        // function used by this example
    volatile long x = 0;                // => co-20: volatile -- forces a real memory round-trip
    for (long i = 0; i < ops; i++) {    // loop header controlling the sweep below
        x = x + 1;                      // => co-20: this step depends on the PREVIOUS step's x
    }
    return x; // returns the computed result
}

// co-22: FOUR independent chains, interleaved in ONE loop -- x0..x3 have no
// data dependency on each other, so a superscalar out-of-order core can
// dispatch and execute all four adds for one loop iteration concurrently
// instead of serializing them; each individual chain is still
// `volatile`-serialized against ITSELF, but the four chains overlap with each
// other, cutting the exposed critical-path length ~4x.
static long independent_chains(long ops) { // defines independent_chains(): helper function
                                           // used by this example
    volatile long x0 = 0, x1 = 0, x2 = 0,
                  x3 = 0;                // => co-22: four separate accumulators, no cross-deps
    for (long i = 0; i < ops / 4; i++) { // => co-22: ops/4 iterations * 4 chains = same total OPS
        x0 = x0 + 1;                     // => co-22: these four statements are mutually
        x1 = x1 + 1;                     //    independent -- the CPU can run them in parallel
        x2 = x2 + 1;                     // assigns x2
        x3 = x3 + 1;                     // assigns x3
    }
    return x0 + x1 + x2 + x3; // => co-22: combined only ONCE, at the very end
}

int main(void) {                               // program entry point
    double t0 = now_seconds();                 // declares t0
    long dep_result = dependent_chain(OPS);    // => co-20: the latency-bound baseline
    double t1 = now_seconds();                 // declares t1
    long ilp_result = independent_chains(OPS); // => co-22: the throughput-bound, overlapped version
    double t2 = now_seconds();                 // declares t2

    double secs_dep = t1 - t0; // declares secs_dep
    double secs_ilp = t2 - t1; // declares secs_ilp
    printf("OPS=%ld total increments in each version\n",
           OPS); // prints a report line
    printf("dependent chain (1 accumulator):    result=%ld, %.4f s\n", dep_result,
           secs_dep);                                                                          // prints a report line
    printf("independent chains (4 accumulators): result=%ld, %.4f s\n", ilp_result, secs_ilp); // prints a report line
    double speedup = secs_dep / secs_ilp;                                                      // => co-22: how much overlap the 4 independent chains bought
    printf("independent chains are %.2fx faster -> %s\n",
           speedup,                                                              // prints a report line
           (dep_result == ilp_result && speedup > 1.1)                           // continues the printf(...) call above
               ? "PASS (identical result, independent chains measurably faster)" // continues the printf(...) call above
               : "FAIL");                                                        // continues the printf(...) call above
    return (dep_result == ilp_result && speedup > 1.1) ? 0 : 1;                  // returns the computed result
}
