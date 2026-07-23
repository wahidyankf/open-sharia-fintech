// learning/code/ex-36-branch-predictable-vs-random/branch_predict.c
/* Example 36: sum-if-positive over sorted vs shuffled data -- verify the
   sorted (predictable) pass runs faster than the shuffled (random) one
   (co-21). */
#include <stdio.h>  // => printf -- the timing/PASS report this program prints
#include <stdlib.h> // => malloc/free/rand/qsort -- data generation, sorting, and shuffling
#include <time.h>   // => clock_gettime -- the portable wall-clock timer used below

#define N \
    1000000 // => co-21: 1M elements, 4 MB -- fits inside this machine's 4 MiB L2,
            // so
            //    the loop is BRANCH/compute-bound, not memory-bandwidth-bound (a
            //    50M-element streaming array hid the mispredict cost behind DRAM
            //    bandwidth -- verified by first trying that shape and seeing no
            //    effect)
#define PASSES \
    200          // => co-21: repeat the full-array pass this many times -- builds a
                 // stable,
                 //    multi-millisecond signal out of a small, cache-resident array
#define TRIALS 3 // => co-25: best-of-3 -- shared-machine noise smoothing

static double now_seconds(void) {                        // => co-25: shared wall-clock helper, this topic's standard pattern
    struct timespec ts;                                  // supporting statement for this example
    clock_gettime(CLOCK_MONOTONIC, &ts);                 // calls clock_gettime(...)
    return (double)ts.tv_sec + (double)ts.tv_nsec / 1e9; // returns the computed result
}

// co-21: EVERY iteration hits this branch -- with sorted input, the outcome is
// the same ("no") for a long run then the same ("yes") for a long run, so the
// branch predictor's history table learns the pattern almost perfectly. With
// shuffled input, the outcome flips unpredictably, defeating the predictor on
// roughly half the iterations -- each mispredict flushes the pipeline (co-20)
// for tens of cycles. VERIFIED CAVEAT (found while building this example):
// clang -O2 on arm64 recognizes `if (x>=0) sum+=x;` as equivalent to `sum +=
// max(x,0)` and silently rewrites it into a branchless `bic/asr` bit-trick on
// its OWN (disassembly confirmed zero branch instructions survived plain code,
// even with vectorize(disable)). The `"+r"(v)` per-value asm barrier below is
// the same "DoNotOptimize" idiom used in ex-37: it pins each candidate value
// through an opaque register operation so LLVM can no longer prove the two arms
// are equivalent and cannot fold them back into one branchless selection.
static long sum_if_positive(const int *arr,
                            int n) {        // defines sum_if_positive(): helper function used by this example
    long total = 0;                         // declares total
    for (int i = 0; i < n; i++) {           // loop header controlling the sweep below
        if (arr[i] >= 0) {                  // => co-21: the data-dependent branch under test --
            int v = arr[i];                 //    two value-pinned arms so clang cannot merge
            __asm__ volatile("" : "+r"(v)); //    them back into a single bic/asr bit-trick
            total += v;                     // => taken only when the (unpredictable) sign says so
        } else {                            // alternate branch
            int v = 0;                      //    the "skip" arm, equally value-pinned
            __asm__ volatile("" : "+r"(v)); // supporting statement for this example
            total += v;                     // updates total
        }
    }
    return total; // returns the computed result
}

// co-21: repeats the pass PASSES times so a small, cache-resident array still
// produces a measurable multi-millisecond total, keeping the branch (not memory
// bandwidth) as the bottleneck this example is isolating.
static long sum_if_positive_repeated(const int *arr, int n,
                                     int passes) { // defines sum_if_positive_repeated():
                                                   // helper function used by this example
    long total = 0;                                // declares total
    for (int p = 0; p < passes; p++) {             // loop header controlling the sweep below
        total += sum_if_positive(arr, n);          // => co-21: identical work every pass, same data
    }
    return total; // returns the computed result
}

static int cmp_int(const void *a,
                   const void *b) {                 // defines cmp_int(): helper function used by this example
    int ia = *(const int *)a, ib = *(const int *)b; // declares ia
    return (ia > ib) - (ia < ib);                   // => standard three-way qsort comparator
}

int main(void) {                                     // program entry point
    srand(99);                                       // => co-25: fixed seed -- reproducible dataset
    int *sorted = malloc((size_t)N * sizeof(int));   // heap-allocates memory for sorted
    int *shuffled = malloc((size_t)N * sizeof(int)); // heap-allocates memory for shuffled
    if (!sorted || !shuffled) {
        fprintf(stderr, "alloc failed\n");
        return 1;
    } // prints a report line

    for (int i = 0; i < N; i++) {            // loop header controlling the sweep below
        int v = (int)(rand() % 2001) - 1000; // => values in [-1000, 1000] -- roughly half negative
        sorted[i] = v;                       // assigns sorted[i]
        shuffled[i] = v;                     // => SAME multiset of values in both arrays
    }
    qsort(sorted, N, sizeof(int),
          cmp_int); // => co-21: sorted -> long predictable runs of sign
    // shuffled stays in its original random order -- co-21: sign flips
    // unpredictably

    double best_sorted = 1e18, best_shuffled = 1e18;              // declares best_sorted
    long sum_sorted = 0, sum_shuffled = 0;                        // declares sum_sorted
    for (int t = 0; t < TRIALS; t++) {                            // => co-25: best-of-N -- keep the fastest clean run
        double t0 = now_seconds();                                // declares t0
        sum_sorted = sum_if_positive_repeated(sorted, N, PASSES); // assigns sum_sorted
        double t1 = now_seconds();                                // declares t1
        if (t1 - t0 < best_sorted)
            best_sorted = t1 - t0; // conditional check

        double t2 = now_seconds();                                    // declares t2
        sum_shuffled = sum_if_positive_repeated(shuffled, N, PASSES); // assigns sum_shuffled
        double t3 = now_seconds();                                    // declares t3
        if (t3 - t2 < best_shuffled)
            best_shuffled = t3 - t2; // conditional check
    }

    printf("N=%d elements x %d passes (4 MB array, L2-resident)\n", N,
           PASSES); // prints a report line
    printf("sorted   sum=%ld, best of %d: %.4f s\n", sum_sorted, TRIALS,
           best_sorted); // prints a report line
    printf("shuffled sum=%ld, best of %d: %.4f s\n", sum_shuffled, TRIALS,
           best_shuffled);                                         // prints a report line
    double speedup = best_shuffled / best_sorted;                  // => co-21: how much slower the mispredicting pass was
    printf("sorted is %.2fx faster -> %s\n", speedup,              // prints a report line
           (sum_sorted == sum_shuffled && speedup > 1.2)           // continues the printf(...) call above
               ? "PASS (identical sums, sorted measurably faster)" // continues the
                                                                   // printf(...)
                                                                   // call above
               : "FAIL");                                          // continues the printf(...) call above
    free(sorted);                                                  // releases sorted's heap memory
    free(shuffled);                                                // releases shuffled's heap memory
    return (sum_sorted == sum_shuffled && speedup > 1.2) ? 0 : 1;  // returns the computed result
}
