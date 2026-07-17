// learning/code/ex-75-superscalar-port-contention/port_contention.c
/* Example 75: sweeping independent-chain count to find where execution-port
 * throughput plateaus. */
#include <stdint.h> // stdint.h: standard library header
#include <stdio.h>  // stdio.h: standard library header
#include <time.h>   // time.h: standard library header

// co-22: integer DIVISION is the probe operation -- it is one of the few ops
// where even a wide, deep out-of-order core has a FINITE, small number of
// divide-capable execution resources (unlike add/multiply, which are cheap
// enough in silicon to duplicate generously). A first attempt at this example
// compared just 2 independent chains against 1 and found them scaling to ~1.94x
// -- ALMOST perfectly linear, meaning this specific core has enough divide
// throughput that 2 streams do NOT contend. The real contention only appears
// once concurrency is pushed further, below.
#define N \
    160000000L // => co-22: total divisions performed by EVERY benchmark variant,
               // however many independent chains it splits that total across

// ex-75: K independent division chains, interleaved in program order, each
// doing N/K divisions. `vectorize(disable)` keeps clang's SLP vectorizer from
// folding these back into fewer, WIDER NEON `fdiv.2d`-style instructions
// (verified during authoring: without it, even 2 "independent chains" got
// auto-vectorized into ONE 2-lane vector division, which measures SIMD
// throughput, not superscalar port count -- a different mechanism, co-23, not
// what this example is testing).
#define MAKE_CHAIN(NAME, K)                                 /* macro MAKE_CHAIN(...): expands inline at compile time */ \
    __attribute__((noinline)) static int64_t NAME(long n) { /* calls __attribute__(...) */                              \
        int64_t a[K];                                       /* declares a */                                            \
        for (int k = 0; k < K; k++)                                                                                     \
            a[k] = 100000000 + k * 37;                               /* distinct per-chain seed */                      \
        long q = n / K;                                              /* declares q */                                   \
        _Pragma("clang loop vectorize(disable) interleave(disable)") /* calls                                           \
                                                                        _Pragma(...)                                    \
                                                                      */                                                \
            for (long i = 0; i < q; i++) {                           /* loop header controlling the sweep below */      \
            for (int k = 0; k < K; k++)                                                                                 \
                a[k] = (9999999999999LL + k) / (a[k] + 3 + k); /* co-22: chain k */                                     \
        }                                                                                                               \
        int64_t s = 0; /* declares s */                                                                                 \
        for (int k = 0; k < K; k++)                                                                                     \
            s += a[k]; /* loop header controlling the sweep below */                                                    \
        return s;      /* returns the computed result */                                                                \
    }

MAKE_CHAIN(chain1,
           1)         // => co-22: baseline -- 1 dependency chain, pure division LATENCY
MAKE_CHAIN(chain2, 2) // => co-22: 2 independent chains -- expect NEAR 2x if the
                      // core has >=2 divide slots
MAKE_CHAIN(chain8,
           8) // => co-22: 8 independent chains -- pushes concurrency further
MAKE_CHAIN(chain16,
           16) // => co-22: 16 independent chains -- if throughput STILL scales,
               // the core has an enormous amount of divide throughput; if it
               // plateaus, THAT plateau is the port count

// ex-75: same volatile-function-pointer-indirection fix ex-74's markdown
// documents in full -- these are side-effect-free calls with the same argument
// every trial, and without this indirection clang's call-CSE collapses all 5
// timing trials into one real computation (measured during authoring: 0.0000 s
// for every trial after the first, a benchmarking artifact, not a real number).
static double time_it(int64_t (*fn)(long), long n,
                      int64_t *out) {                                            // declares function pointer fn
    int64_t (*volatile fn_indirect)(long) = fn;                                  // declares function pointer fn_indirect
    struct timespec t0, t1;                                                      // supporting statement for this example
    double best = -1.0;                                                          // declares best
    int64_t result = 0;                                                          // declares result
    for (int trial = 0; trial < 5; trial++) {                                    // loop header controlling the sweep below
        clock_gettime(CLOCK_MONOTONIC, &t0);                                     // calls clock_gettime(...)
        result = fn_indirect(n);                                                 // assigns result
        clock_gettime(CLOCK_MONOTONIC, &t1);                                     // calls clock_gettime(...)
        double secs = (t1.tv_sec - t0.tv_sec) + (t1.tv_nsec - t0.tv_nsec) / 1e9; // declares secs
        if (best < 0 || secs < best)
            best = secs; // conditional check
    }
    *out = result; // supporting statement for this example
    return best;   // returns the computed result
}

int main(void) {                           // program entry point
    int64_t r;                             // declares r
    double t1v = time_it(chain1, N, &r);   // declares t1v
    double t2v = time_it(chain2, N, &r);   // declares t2v
    double t8v = time_it(chain8, N, &r);   // declares t8v
    double t16v = time_it(chain16, N, &r); // declares t16v

    double rate1 = (double)N / t1v, rate2 = (double)N / t2v, rate8 = (double)N / t8v, rate16 = (double)N / t16v; // declares rate1
    double ratio2 = rate2 / rate1, ratio8 = rate8 / rate1,
           ratio16 = rate16 / rate1; // declares ratio2

    printf("N=%ld total divisions per benchmark, split across K independent "
           "chains\n",
           N); // prints a report line
    printf("K=1  chains: %.4f s, %.1fM divs/s (1.00x, baseline)\n", t1v,
           rate1 / 1e6);                                                                             // prints a report line
    printf("K=2  chains: %.4f s, %.1fM divs/s (%.2fx of ideal 2x)\n", t2v, rate2 / 1e6, ratio2);     // prints a report line
    printf("K=8  chains: %.4f s, %.1fM divs/s (%.2fx of ideal 8x)\n", t8v, rate8 / 1e6, ratio8);     // prints a report line
    printf("K=16 chains: %.4f s, %.1fM divs/s (%.2fx of ideal 16x)\n", t16v, rate16 / 1e6, ratio16); // prints a report line
    printf("\nlow concurrency (K=2) scales NEAR-linearly (this core has more "
           "than 1 divide-capable\n"); // prints a report line
    printf("execution resource); high concurrency (K=16) does NOT reach anywhere "
           "near the naive 16x --\n"); // prints a report line
    printf("that shortfall IS the execution-port/resource ceiling this example "
           "set out to find.\n"); // prints a report line

    // co-22: the claim is "throughput caps below the independent-op rate" -- true
    // at K=2 (this machine has enough capacity there) is NOT the point; the point
    // is that it becomes STRIKINGLY true once concurrency is pushed past the
    // real, finite port count, which K=16 exposes.
    int pass = (ratio2 > 1.5) && // low concurrency: genuinely scales (rules out a trivially
                                 // "everything always serializes" measurement bug)
               (ratio16 < 8.0);  // high concurrency: achieves LESS THAN HALF of the naive ideal 16x
    printf("\nPASS (K=2 scales near-linearly, but K=16 throughput caps well "
           "below the naive 16x --\n"); // prints a report line
    printf(" evidence of a finite, shared execution resource): %s\n",
           pass ? "PASS" : "FAIL"); // prints a report line
    return 0;                       // returns the computed result
}
