// learning/code/ex-37-branchless-max/branchless_max.c
/* Example 37: replace a conditional max with a branchless bit-trick --
   verify identical output and a speedup on unpredictable (random) data
   (co-21). */
#include <stdio.h>  // => printf -- the timing/PASS report this program prints
#include <stdlib.h> // => malloc/free/rand -- the random input arrays
#include <time.h>   // => clock_gettime -- the portable wall-clock timer used below

#define N \
    50000000     // => co-21: 50M random pairs -- enough to average out predictor
                 // noise
#define TRIALS 3 // => co-25: best-of-3 -- shared-machine noise smoothing

static double now_seconds(void) {                        // => co-25: shared wall-clock helper, this topic's standard pattern
    struct timespec ts;                                  // supporting statement for this example
    clock_gettime(CLOCK_MONOTONIC, &ts);                 // calls clock_gettime(...)
    return (double)ts.tv_sec + (double)ts.tv_nsec / 1e9; // returns the computed result
}

// co-21: the OBVIOUS implementation -- a data-dependent branch that the CPU
// must predict every iteration. On uniformly random a/b, "a > b" is true about
// half the time with NO pattern, so the branch predictor is wrong roughly half
// the time -- every mispredict flushes the in-flight pipeline (co-20). VERIFIED
// CAVEAT (found while building this example): clang -O2 on arm64 aggressively
// converts a plain
// `(a>b)?a:b` into a branchless `cmp+csel` on its OWN -- disassembly confirmed
// no branch survived, even behind a memory-only asm barrier (that barrier
// doesn't pin the VALUE, only memory ordering, so if-conversion still merged
// the two arms). The `"+r"(v)` per-value asm barrier below is the standard
// "DoNotOptimize" idiom (as used by Google Benchmark): it forces the SPECIFIC
// register holding each candidate value through an opaque no-op instruction, so
// LLVM can no longer prove the two arms compute equivalent values and cannot
// fold them into one csel.
static long sum_branchy_max(const int *a, const int *b,
                            int n) {        // defines sum_branchy_max(): helper function used by this example
    long total = 0;                         // declares total
    for (int i = 0; i < n; i++) {           // loop header controlling the sweep below
        if (a[i] > b[i]) {                  // => co-21: a REAL conditional branch (cmp+b.le) --
            int v = a[i];                   //    two value-pinned arms so clang cannot merge
            __asm__ volatile("" : "+r"(v)); //    them back into a single conditional-select
            total += v;                     // updates total
        } else {                            // alternate branch
            int v = b[i];                   //    same value-pinning trick on the other arm
            __asm__ volatile("" : "+r"(v)); // supporting statement for this example
            total += v;                     // updates total
        }
    }
    return total; // returns the computed result
}

// co-21: the BRANCHLESS trick -- computes max(a,b) with pure arithmetic/bitwise
// ops, no conditional jump at all, so there is nothing for the branch predictor
// to get wrong: diff = a-b; mask = diff's sign bit smeared across all 32 bits
// (all 1s if a<b, all 0s if a>=b); result = a - (diff & mask) -- selects a or b
// without a jump. vectorize(disable) keeps this scalar so the comparison
// isolates the branch-vs-branchless difference, not a scalar-vs-SIMD difference
// (that's ex-47's and ex-48's job, not this one's).
static long sum_branchless_max(const int *a, const int *b,
                               int n) {                   // defines sum_branchless_max(): helper
                                                          // function used by this example
    long total = 0;                                       // declares total
#pragma clang loop vectorize(disable) interleave(disable) // supporting statement for this example
    for (int i = 0; i < n; i++) {                         // loop header controlling the sweep below
        int diff = a[i] - b[i];                           // => co-21: negative iff a[i] < b[i]
        int mask = diff >> 31;                            // => co-21: arithmetic shift smears the sign bit --
                                                          //    all-1s (mask=-1) if diff<0, all-0s if diff>=0
        int m = a[i] - (diff & mask);                     // => co-21: mask=0 -> m=a[i]-0=a[i]; mask=-1 ->
        total += m;                                       //    m=a[i]-diff=a[i]-(a[i]-b[i])=b[i] -- zero branches
    }
    return total; // returns the computed result
}

int main(void) {                              // program entry point
    srand(2024);                              // => co-25: fixed seed -- reproducible dataset
    int *a = malloc((size_t)N * sizeof(int)); // heap-allocates memory for a
    int *b = malloc((size_t)N * sizeof(int)); // heap-allocates memory for b
    if (!a || !b) {
        fprintf(stderr, "alloc failed\n");
        return 1;
    } // prints a report line
    for (int i = 0; i < N; i++) {               // => uniformly random pairs -- no exploitable pattern
        a[i] = (int)(rand() % 200001) - 100000; // assigns a[i]
        b[i] = (int)(rand() % 200001) - 100000; // assigns b[i]
    }

    double best_branchy = 1e18, best_branchless = 1e18; // declares best_branchy
    long sum_branchy = 0, sum_branchless = 0;           // declares sum_branchy
    for (int t = 0; t < TRIALS; t++) {                  // => co-25: best-of-N -- keep the fastest clean run
        double t0 = now_seconds();                      // declares t0
        sum_branchy = sum_branchy_max(a, b, N);         // assigns sum_branchy
        double t1 = now_seconds();                      // declares t1
        if (t1 - t0 < best_branchy)
            best_branchy = t1 - t0; // conditional check

        double t2 = now_seconds();                    // declares t2
        sum_branchless = sum_branchless_max(a, b, N); // assigns sum_branchless
        double t3 = now_seconds();                    // declares t3
        if (t3 - t2 < best_branchless)
            best_branchless = t3 - t2; // conditional check
    }

    printf("branchy    sum=%ld, best of %d: %.4f s\n", sum_branchy, TRIALS,
           best_branchy); // prints a report line
    printf("branchless sum=%ld, best of %d: %.4f s\n", sum_branchless, TRIALS,
           best_branchless);                                // prints a report line
    double speedup = best_branchy / best_branchless;        // => co-21: how much the branchless rewrite recovered
    printf("branchless is %.2fx faster -> %s\n", speedup,   // prints a report line
           (sum_branchy == sum_branchless && speedup > 1.1) // continues the printf(...) call above
               ? "PASS (identical output, branchless measurably faster on random "
                 "data)"                                             // continues the printf(...) call above
               : "FAIL");                                            // continues the printf(...) call above
    free(a);                                                         // releases a's heap memory
    free(b);                                                         // releases b's heap memory
    return (sum_branchy == sum_branchless && speedup > 1.1) ? 0 : 1; // returns the computed result
}
