// learning/code/ex-47-simd-auto-vectorize/vectorize_sum.c
/* Example 47: compile the SAME sum loop at -O0 and -O3 -- verify NEON
   vector registers appear in the -O3 assembly and a real speedup over -O0
   (co-23). This file is compiled TWICE (see Compile/Run below); the C
   source itself never mentions NEON -- the compiler decides to vectorize
   it on its own at -O3. */
#include <stdio.h>  // => printf -- the timing/PASS report this program prints
#include <stdlib.h> // => malloc/free -- the array being summed
#include <time.h>   // => clock_gettime -- the portable wall-clock timer used below

#define N \
    200000000    // => co-23: 200M ints -- large enough that a vectorized inner
                 // loop's
                 //    per-element speedup shows up clearly in wall-clock time
#define TRIALS 3 // => co-25: best-of-3 -- shared-machine noise smoothing

static double now_seconds(void) { // => co-25: shared wall-clock helper, this topic's standard pattern
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return (double)ts.tv_sec + (double)ts.tv_nsec / 1e9;
}

// co-23: a plain scalar-LOOKING sum reduction -- integer addition is
// associative under C's well-defined wraparound semantics, so clang's
// auto-vectorizer is FREE to reorder these adds into SIMD lanes at -O3 without
// changing the result (this is exactly why an INT reduction (not a float one)
// is used here: float addition is NOT associative, so a float version would
// need -ffast-math to vectorize the same way). co-25: VERIFIED CAVEAT (found
// while building this example, in THREE stages): a plain noinline function
// still isn't enough -- LLVM's global-value-numbering proved this function is
// pure (same arr, same n -> same result) and CSE'd 2 of the 3 TRIALS calls into
// ONE physical call, reusing the cached result (confirmed: only one `bl
// _sum_array` survived in the -O3 assembly). The `salt` parameter makes each
// trial's call provably return a DIFFERENT value (salt=0,1,2), which defeats
// that CSE while adding only one extra scalar add per call -- negligible next
// to the N-element reduction, so it does not distort the real work being timed.
__attribute__((noinline)) static long sum_array(const int *arr, int n, int salt) {
    long total = salt;            // => co-25: seeds the accumulator with `salt` --
    for (int i = 0; i < n; i++) { //    just enough to force a distinct result per call
        total += arr[i];          // => co-23: -O0 emits one scalar add per element;
    } //    -O3 emits NEON adds processing several at once
    return total;
}

int main(void) {
    int *arr = malloc((size_t)N * sizeof(int));
    if (!arr) {
        fprintf(stderr, "alloc failed\n");
        return 1;
    }
    srand(3); // => co-25: fixed seed -- reproducible values, but
    for (int i = 0; i < N; i++)
        arr[i] = (rand() % 7) - 3; //    rand() defeats -O3's closed-form constant-fold
                                   //    of the WHOLE fill+sum pattern (verified: a pure
                                   //    arithmetic fill let -O3 collapse everything to
                                   //    a single constant, timing 0.0000 s -- rand()
                                   //    output isn't known at compile time, so it can't)

    double best = 1e18;
    long total = 0;
    for (int t = 0; t < TRIALS; t++) { // => co-25: best-of-N -- keep the fastest clean run
        double t0 = now_seconds();
        total = sum_array(arr, N, t) - t; // => co-25: subtract the salt back out for the
        double t1 = now_seconds();        //    printed value -- the REAL reduction work still
        if (t1 - t0 < best)
            best = t1 - t0; //    ran fully, every trial (see comment above sum_array)
    }

    printf("N=%d, sum=%ld, best of %d: %.4f s\n", N, total, TRIALS,
           best); // => co-23: this SAME line prints
                  //    from BOTH the -O0 and -O3
                  //    binaries -- compare their
                  //    output externally, per the
                  //    Compile/Run section below
    free(arr);
    return 0;
}
