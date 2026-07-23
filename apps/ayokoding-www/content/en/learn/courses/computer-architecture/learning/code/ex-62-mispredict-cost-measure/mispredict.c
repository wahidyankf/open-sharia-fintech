// learning/code/ex-62-mispredict-cost-measure/mispredict.c
/* Example 62: measure the real wall-clock cost of a branch misprediction. */
#include <stdio.h>  // stdio.h: standard library header
#include <stdlib.h> // stdlib.h: standard library header
#include <time.h>   // time.h: standard library header

#define N \
    200000000 // => co-21: 200M branches -- large enough to average out timer-call
              // overhead

// ex-62: PREDICTABLE pattern -- long runs of the same flag value (256 zeros,
// then 256 ones, repeating). A branch predictor locks onto "same as last time"
// almost perfectly.
static unsigned char *make_predictable(long n) { // defines make_predictable(): helper function used
                                                 // by this example
    unsigned char *flags = malloc((size_t)n);    // heap-allocates memory for flags
    for (long i = 0; i < n; i++)
        flags[i] = (unsigned char)((i / 256) % 2); // => co-21: long runs
    return flags;                                  // returns the computed result
}

// ex-62: RANDOM pattern -- an independent coin flip per index. No predictor can
// do meaningfully better than chance on a genuinely random sequence.
static unsigned char *make_random(long n) {            // defines make_random(): helper function used by this example
    unsigned char *flags = malloc((size_t)n);          // heap-allocates memory for flags
    unsigned seed = 99u;                               // declares seed
    for (long i = 0; i < n; i++) {                     // loop header controlling the sweep below
        seed = seed * 1103515245u + 12345u;            // assigns seed
        flags[i] = (unsigned char)((seed >> 24) & 1u); // => co-21: unpredictable 0/1
    }
    return flags; // returns the computed result
}

// ex-62: the branch whose mispredict cost this example measures -- a genuinely
// data-dependent conditional the compiler cannot turn into a `cmov`/`csel`
// because the two arms have different side effects the optimizer must preserve
// in order (accumulator sign). co-21: `optnone` is load-bearing here, not
// decorative. Even with loop-vectorization disabled, clang's scalar
// if-converter still rewrites the branch below into a branchless `csinv`
// (conditional-select) instruction at -O2 -- verified by inspecting `-S` output
// -- which leaves NO branch for the CPU to mispredict at all. `optnone` forces
// this one function to skip that optimization so the measurement is honest: a
// real `cmp`+`b.ne`.
__attribute__((noinline, optnone)) static long sum_with_branch(const unsigned char *flags,
                                                               long n) { // calls __attribute__(...)
    long acc = 0;                                                        // declares acc
    for (long i = 0; i < n; i++) {                                       // loop header controlling the sweep below
        if (flags[i]) {                                                  // => co-21: THIS branch is what the CPU must predict every
                                                                         // iteration
            acc += 3;                                                    // updates acc
        } else {                                                         // alternate branch
            acc -= 1;                                                    // updates acc
        }
    }
    return acc; // returns the computed result
}

static double time_it(const unsigned char *flags, long n,
                      long *out_sum) {                                           // defines time_it(): helper function used by this example
    struct timespec t0, t1;                                                      // supporting statement for this example
    double best = -1.0;                                                          // declares best
    long sum = 0;                                                                // declares sum
    for (int trial = 0; trial < 3; trial++) {                                    // loop header controlling the sweep below
        clock_gettime(CLOCK_MONOTONIC, &t0);                                     // calls clock_gettime(...)
        sum = sum_with_branch(flags, n);                                         // assigns sum
        clock_gettime(CLOCK_MONOTONIC, &t1);                                     // calls clock_gettime(...)
        double secs = (t1.tv_sec - t0.tv_sec) + (t1.tv_nsec - t0.tv_nsec) / 1e9; // declares secs
        if (best < 0 || secs < best)
            best = secs; // conditional check
    }
    *out_sum = sum; // supporting statement for this example
    return best;    // returns the computed result
}

int main(void) {                                // program entry point
    unsigned char *pred = make_predictable(N);  // declares pred
    unsigned char *rand_flags = make_random(N); // declares rand_flags

    long sum_pred, sum_rand;                           // declares sum_pred
    double t_pred = time_it(pred, N, &sum_pred);       // declares t_pred
    double t_rand = time_it(rand_flags, N, &sum_rand); // declares t_rand

    double ns_per_iter_pred = (t_pred / N) * 1e9;                   // declares ns_per_iter_pred
    double ns_per_iter_rand = (t_rand / N) * 1e9;                   // declares ns_per_iter_rand
    double extra_ns_per_iter = ns_per_iter_rand - ns_per_iter_pred; // declares extra_ns_per_iter
    // A genuinely random independent 0/1 sequence is wrong roughly half the time
    // no matter how good the predictor is -- so the extra per-iteration cost,
    // divided by the ~50% misprediction rate, approximates the cost of ONE
    // misprediction.
    double ns_per_mispredict = extra_ns_per_iter / 0.5; // declares ns_per_mispredict

    printf("N=%d branches\n", N); // prints a report line
    printf("predictable pattern: %.4f s total, %.3f ns/iter (sum=%ld)\n", t_pred,
           ns_per_iter_pred, // prints a report line
           sum_pred);        // continues the printf(...) call above
    printf("random pattern:      %.4f s total, %.3f ns/iter (sum=%ld)\n", t_rand,
           ns_per_iter_rand, // prints a report line
           sum_rand);        // continues the printf(...) call above
    printf("extra cost per iteration on random input: %.3f ns\n",
           extra_ns_per_iter); // prints a report line
    printf("approx cost per misprediction (extra / ~0.5 misprediction rate): "
           "%.3f ns\n",        // prints a report line
           ns_per_mispredict); // continues the printf(...) call above
    printf("(no `perf`/cycle counter on macOS -- this machine's Apple Silicon "
           "core clock\n"); // prints a report line
    printf(" frequency isn't exposed via a stable public API, so this is "
           "reported in nanoseconds,\n"); // prints a report line
    printf(" not cycles; at a multi-GHz clock a few nanoseconds is a "
           "double-digit number of cycles,\n"); // prints a report line
    printf(" the expected order of magnitude for a deep out-of-order core's "
           "pipeline-flush cost.)\n");                                          // prints a report line
    int pass = (extra_ns_per_iter > 0.3) && (sum_pred != 0) && (sum_rand != 0); // real, positive, non-trivial cost
    printf("PASS (measurable mispredict cost > 0.3 ns/iter): %s\n",
           pass ? "PASS" : "FAIL"); // prints a report line

    free(pred);       // releases pred's heap memory
    free(rand_flags); // releases rand_flags's heap memory
    return 0;         // returns the computed result
}
