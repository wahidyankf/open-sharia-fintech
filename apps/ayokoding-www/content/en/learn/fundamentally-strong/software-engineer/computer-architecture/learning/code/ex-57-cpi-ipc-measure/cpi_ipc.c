// learning/code/ex-57-cpi-ipc-measure/cpi_ipc.c
/* Example 57: CPI/IPC measure -- compare a dependent-chain loop against an
 * independent-4-accumulator loop with the SAME known instruction count per
 * iteration, and derive an approximate relative cycles-per-instruction (CPI)
 * from wall-clock time. macOS has no scriptable hardware instruction/cycle
 * counter here (no `perf`; Instruments/`dtrace` are GUI/privileged) -- this
 * derives a RELATIVE CPI ratio from real wall-clock time and a hand-counted
 * instruction count, not a raw hardware counter reading (co-25 honesty rule).
 */
#include <stdio.h> // stdio.h: standard library header
#include <time.h>  // time.h: standard library header

#define N 200000000 // => co-22: 200M loop iterations per variant
#define TRIALS 5    // constant TRIALS = 5

// co-25: VERIFIED BUG #1 (found while verifying this example, same root cause
// as ex-47/48/49/50/55/56): calling sum_dependent(N)/sum_independent4(N) with
// the IDENTICAL argument N on every one of the 5 best-of-N trials let LLVM's
// cross-call redundant-computation elimination prove trials 2..5 return the
// SAME value as trial 1 and hoist the real work out of them entirely.
// Fixed with the established "salt parameter" technique: each trial passes
// its own trial index `t` as an extra addend, making every call's result
// provably distinct so the compiler cannot fold repeat calls.
//
// co-25: VERIFIED BUG #2 (found via -O2 -S disassembly AFTER fixing bug #1,
// still measured 0.0000 s): `for(i=0;i<n;i++) acc+=1;` has no side effect
// LLVM can't see through -- its scalar-evolution pass proved the WHOLE loop is
// algebraically equivalent to `acc = salt + n` and replaced all 200M
// iterations with a single `add` instruction (disassembly confirmed: the
// entire function compiled to 3 instructions, `bic`/`add`/`ret`, no loop at
// all). Fixed the same way ex-38/ex-40 avoid this: mark the accumulator(s)
// `volatile`, forcing a REAL memory read-modify-write every iteration that
// the optimizer cannot algebraically collapse.

// ex-57: DEPENDENT chain -- each add depends on the PREVIOUS iteration's
// result, so the core cannot start iteration i+1's add until iteration i's add
// retires. co-20/co-22: this forces near-fully-serial execution regardless of
// how many execution ports are free -- 1 add instruction "retired" per
// dependency-chain latency
__attribute__((noinline)) static long sum_dependent(long n, long salt) { // calls __attribute__(...)
    volatile long acc = salt;                                            // => co-25: volatile -- blocks the loop-collapse
                                                                         // (see bug #2 above);
    for (long i = 0; i < n; i++) {                                       //    salt distinguishes each trial's call (see bug #1 above)
        acc = acc + 1;                                                   // => 1 add instruction, fully serialized by the acc dependency
    }
    return acc; // returns the computed result
}

// ex-57: INDEPENDENT 4-accumulator chain -- the SAME total instruction count
// (4 adds per 4 iterations = 1 add/iteration, identical to the dependent
// version) but split across 4 accumulators with NO dependency between them, so
// a superscalar out-of-order core (co-22) can issue several in the same cycle
__attribute__((noinline)) static long sum_independent4(long n, long salt) { // calls __attribute__(...)
    volatile long a0 = salt, a1 = 0, a2 = 0,
                  a3 = 0;        // => co-25: volatile -- blocks loop-collapse on ALL 4;
    long i = 0;                  //    salt on a0 distinguishes each trial's call
    for (; i + 4 <= n; i += 4) { // loop header controlling the sweep below
        a0 = a0 + 1;             // => co-22: these 4 adds have NO dependency on each other --
        a1 = a1 + 1;             //    the core can issue/execute them in the same or adjacent
        a2 = a2 + 1;             //    cycles instead of waiting for the prior add to retire
        a3 = a3 + 1;             // assigns a3
    }
    long acc = a0 + a1 + a2 + a3; // declares acc
    for (; i < n; i++)
        acc += 1; // => scalar tail for n not a multiple of 4
    return acc;   // returns the computed result
}

static double best_of_seconds(long (*fn)(long, long), long n,
                              long *out_result) { // declares function pointer fn
    double best = -1.0;                           // declares best
    long result = 0;                              // declares result
    for (int t = 0; t < TRIALS; t++) {            // loop header controlling the sweep below
        struct timespec t0, t1;                   // supporting statement for this example
        clock_gettime(CLOCK_MONOTONIC, &t0);      // calls clock_gettime(...)
        result = fn(n, (long)t) - (long)t;        // => co-25: salted call, then subtract the salt back out --
        clock_gettime(CLOCK_MONOTONIC,
                      &t1);                                                      //    each of the 5 calls is now provably distinct to the compiler
        double secs = (t1.tv_sec - t0.tv_sec) + (t1.tv_nsec - t0.tv_nsec) / 1e9; // declares secs
        if (best < 0 || secs < best)
            best = secs; // conditional check
    }
    *out_result = result; // supporting statement for this example
    return best;          // returns the computed result
}

int main(void) {                                                       // program entry point
    long r_dep_check = 0, r_ind_check = 0;                             // declares r_dep_check
    double t_dep = best_of_seconds(sum_dependent, N, &r_dep_check);    // declares t_dep
    double t_ind = best_of_seconds(sum_independent4, N, &r_ind_check); // declares t_ind
    long r1 = r_dep_check, r2 = r_ind_check;                           // declares r1
    printf("dependent result=%ld independent4 result=%ld (must match: %s)\n", r1,
           r2,                                // prints a report line
           (r1 == r2) ? "yes" : "NO -- BUG"); // continues the printf(...) call above

    // => co-25: both variants execute the SAME N add instructions total (one add
    // per logical unit of work) -- so time-per-instruction is a direct, honest
    // proxy for relative CPI here (fewer seconds per identical instruction count
    // == lower CPI == higher IPC)
    double cpi_proxy_dep = t_dep / (double)N; // => "seconds per instruction" -- relative CPI proxy
    double cpi_proxy_ind = t_ind / (double)N; // declares cpi_proxy_ind

    printf("N=%d add instructions (identical count, both variants)\n",
           N); // prints a report line
    printf("dependent chain:      best of %d = %.4f s -> %.4f ns/instruction "
           "(relative CPI proxy)\n", // prints a report line
           TRIALS, t_dep,
           cpi_proxy_dep * 1e9); // continues the printf(...) call above
    printf("independent 4-accum:  best of %d = %.4f s -> %.4f ns/instruction "
           "(relative CPI proxy)\n", // prints a report line
           TRIALS, t_ind,
           cpi_proxy_ind * 1e9); // continues the printf(...) call above
    printf("independent/dependent ns-per-instruction ratio: %.3fx (lower = "
           "better, higher throughput)\n", // prints a report line
           cpi_proxy_ind / cpi_proxy_dep); // continues the printf(...) call above
    printf("(no `perf`/hardware IPC counter on macOS -- this is a "
           "wall-clock-derived RELATIVE CPI\n"); // prints a report line
    printf(" proxy from a KNOWN, identical instruction count, not a raw hardware "
           "counter reading)\n");             // prints a report line
    int pass = (r1 == r2) && (t_ind < t_dep); // declares pass
    printf("PASS (identical results, independent-accumulator variant has lower "
           "effective CPI): %s\n",  // prints a report line
           pass ? "PASS" : "FAIL"); // continues the printf(...) call above
    return 0;                       // returns the computed result
}
