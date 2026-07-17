// learning/code/ex-63-branch-to-lookup-table/lookup.c
/* Example 63: a data-dependent branch chain vs a lookup table, on random input.
 */
#include <stdio.h>  // stdio.h: standard library header
#include <stdlib.h> // stdlib.h: standard library header
#include <time.h>   // time.h: standard library header

#define N \
    300000000 // => co-21: 300M random exam scores -- large enough to dominate
              // loop overhead

static char grade_of(int score) { // => co-21: single source of truth for BOTH
                                  // classifiers' correctness
    if (score >= 90)
        return 'A'; // conditional check
    else if (score >= 80)
        return 'B'; // alternate conditional branch
    else if (score >= 70)
        return 'C'; // alternate conditional branch
    else if (score >= 60)
        return 'D'; // alternate conditional branch
    else
        return 'F'; // alternate branch
}

// ex-63: BRANCHY sum -- classifies every score with the same comparison chain
// as grade_of, inline in the hot loop (no per-element function-call overhead to
// dilute the branch cost). `optnone` keeps clang's if-converter from turning
// this into a branchless select the way it did in ex-62 -- verified by
// inspecting `-S` output during authoring.
__attribute__((noinline, optnone)) static unsigned long sum_branchy(const int *scores, long n) { // calls __attribute__(...)
    unsigned long sum = 0;                                                                       // declares sum
    for (long i = 0; i < n; i++) {                                                               // loop header controlling the sweep below
        int s = scores[i];                                                                       // declares s
        char g;                                                                                  // declares g
        if (s >= 90)
            g = 'A'; // => co-21: 4 data-dependent comparisons, genuinely
                     // unpredictable
        else if (s >= 80)
            g = 'B'; // on uniformly random 0..100 input
        else if (s >= 70)
            g = 'C'; // alternate conditional branch
        else if (s >= 60)
            g = 'D'; // alternate conditional branch
        else
            g = 'F';             // alternate branch
        sum += (unsigned char)g; // updates sum
    }
    return sum; // returns the computed result
}

// ex-63: LOOKUP-TABLE sum -- one 101-byte table (fits in a single 128 B cache
// line on this machine), built once, indexed directly. No branch anywhere in
// the hot loop.
static char grade_table[101];         // declares grade_table
static void build_grade_table(void) { // defines build_grade_table(): helper function used by this example
    for (int s = 0; s <= 100; s++)
        grade_table[s] = grade_of(s); // loop header controlling the sweep below
}
__attribute__((noinline)) static unsigned long sum_lookup(const int *scores, long n) { // calls __attribute__(...)
    unsigned long sum = 0;                                                             // declares sum
    for (long i = 0; i < n; i++) {                                                     // loop header controlling the sweep below
        sum += (unsigned char)grade_table[scores[i]];                                  // => co-21: one array load, zero branches
    }
    return sum; // returns the computed result
}

// ex-63: shared timing harness -- both sum_branchy and sum_lookup share this
// exact signature, so one best-of-3 driver measures them identically; out_sum
// forces every trial's checksum to escape the function, so the compiler can
// never treat a "discarded" call as dead and skip it.
static double best_of(unsigned long (*fn)(const int *, long), const int *scores,
                      long n,                                                    // declares function pointer fn
                      unsigned long *out_sum) {                                  // supporting statement for this example
    double best = -1.0;                                                          // declares best
    for (int t = 0; t < 3; t++) {                                                // loop header controlling the sweep below
        struct timespec t0, t1;                                                  // supporting statement for this example
        clock_gettime(CLOCK_MONOTONIC, &t0);                                     // calls clock_gettime(...)
        unsigned long s = fn(scores, n);                                         // declares s
        clock_gettime(CLOCK_MONOTONIC, &t1);                                     // calls clock_gettime(...)
        double secs = (t1.tv_sec - t0.tv_sec) + (t1.tv_nsec - t0.tv_nsec) / 1e9; // declares secs
        if (best < 0 || secs < best)
            best = secs; // conditional check
        *out_sum = s;    // => every trial computes and stores a real sum -- nothing
                         // here is ever dead
    }
    return best; // returns the computed result
}

// ex-63: main() builds the lookup table, generates one shared random-score
// array both classifiers run against, spot-checks correctness on a 5M-score
// sample, THEN times both full-N passes -- correctness is settled before speed
// is compared, never the other way round.
int main(void) {                            // program entry point
    build_grade_table();                    // calls build_grade_table(...)
    int *scores = malloc(sizeof(int) * N);  // heap-allocates memory for scores
    unsigned seed = 5u;                     // declares seed
    for (long i = 0; i < N; i++) {          // loop header controlling the sweep below
        seed = seed * 1103515245u + 12345u; // assigns seed
        scores[i] = (int)(seed % 101u);     // => uniform random 0..100 -- genuinely
                                            // unpredictable per-branch
    }

    // co-21: correctness -- every one of the first 5M scores must classify
    // identically both ways.
    long mismatches = 0;                          // declares mismatches
    for (long i = 0; i < N && i < 5000000; i++) { // loop header controlling the sweep below
        char via_branch;                          // declares via_branch
        int s = scores[i];                        // declares s
        if (s >= 90)
            via_branch = 'A'; // conditional check
        else if (s >= 80)
            via_branch = 'B'; // alternate conditional branch
        else if (s >= 70)
            via_branch = 'C'; // alternate conditional branch
        else if (s >= 60)
            via_branch = 'D'; // alternate conditional branch
        else
            via_branch = 'F'; // alternate branch
        if (via_branch != grade_table[s])
            mismatches++; // conditional check
    }

    unsigned long sum_b, sum_l;                                 // declares sum_b
    double t_branchy = best_of(sum_branchy, scores, N, &sum_b); // declares t_branchy
    double t_lookup = best_of(sum_lookup, scores, N, &sum_l);   // declares t_lookup

    printf("N=%d random scores (0-100)\n", N); // prints a report line
    printf("branchy classifier: best of 3 = %.4f s (sum=%lu)\n", t_branchy,
           sum_b); // prints a report line
    printf("lookup-table classifier: best of 3 = %.4f s (sum=%lu)\n", t_lookup,
           sum_l); // prints a report line
    printf("classification mismatches (sampled 5M): %ld\n",
           mismatches); // prints a report line
    printf("checksums match (both sum the same grade letters): %s\n",
           sum_b == sum_l ? "yes" : "NO -- BUG"); // prints a report line
    double speedup = t_branchy / t_lookup;        // declares speedup
    printf("speedup: %.2fx (PASS: identical classification, lookup faster on "
           "random input) -> %s\n", // prints a report line
           speedup,
           (mismatches == 0 && sum_b == sum_l && speedup > 1.05) ? "PASS" : "FAIL"); // continues the printf(...) call above
    free(scores);                                                                    // releases scores's heap memory
    return 0;                                                                        // returns the computed result
}
