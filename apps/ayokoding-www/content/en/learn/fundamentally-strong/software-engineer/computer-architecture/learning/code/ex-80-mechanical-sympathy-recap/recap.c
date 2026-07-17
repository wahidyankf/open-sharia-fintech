// learning/code/ex-80-mechanical-sympathy-recap/recap.c
/* Example 80: a final harness re-running 4 kernels from across this topic,
 * asserting cache-friendly beats cache-hostile in every single one, in one
 * program, in one run. */
#include <stdio.h>  // stdio.h: standard library header
#include <stdlib.h> // stdlib.h: standard library header
#include <time.h>   // time.h: standard library header

// co-25: EVERY timed call below goes through a `volatile` function-pointer
// VARIABLE. ex-74's markdown documents in full why this is load-bearing across
// this topic's examples: side-effect-free calls with the same arguments across
// repeated trials get folded into ONE real computation by clang's call-CSE,
// corrupting the measurement to near-0 s -- this harness re-runs 4 such kernels
// and would silently produce 4 fabricated "instant" times without this
// indirection on every one.
#define TIME_CALL(RESULT_TYPE, FN, ARGS_TYPE, ...) /* macro TIME_CALL(...): expands inline at compile time */                                     \
    ({                                                                                                                                            \
        RESULT_TYPE(*volatile fn_v)                                                                                                               \
        ARGS_TYPE = (FN);                                                                 /* declares function pointer fn_v */                    \
        struct timespec _t0, _t1;                                                         /* supporting statement for this example */             \
        double _best = -1.0;                                                              /* declares _best */                                    \
        for (int _trial = 0; _trial < 3; _trial++) {                                      /* loop header controlling the sweep below */           \
            clock_gettime(CLOCK_MONOTONIC, &_t0);                                         /* calls clock_gettime(...) */                          \
            volatile RESULT_TYPE _r = fn_v(__VA_ARGS__);                                  /* declares _r */                                       \
            clock_gettime(CLOCK_MONOTONIC, &_t1);                                         /* calls clock_gettime(...) */                          \
            (void)_r;                                                                     /* discards _r to silence an unused-variable warning */ \
            double _secs = (_t1.tv_sec - _t0.tv_sec) + (_t1.tv_nsec - _t0.tv_nsec) / 1e9; /* declares _secs */                                    \
            if (_best < 0 || _secs < _best)                                                                                                       \
                _best = _secs; /* conditional check */                                                                                            \
        }                                                                                                                                         \
        _best; /* supporting statement for this example */                                                                                        \
    })

// ==================== kernel 1: sequential-vs-random-sum (re-runs ex-23)
// ==================== co-03/co-05: same K1_N-element array, walked two ways --
// unit-stride vs a Fisher-Yates-shuffled permutation of the same indices, so
// the comparison isolates ACCESS PATTERN, not data size.
#define K1_N 4000000 // constant K1_N = 4000000
static long k1_sum_sequential(const int *a, const int *idx,
                              long n) { // defines k1_sum_sequential(): helper
                                        // function used by this example
    (void)idx;                          // discards idx to silence an unused-variable warning
    long s = 0;                         // declares s
    for (long i = 0; i < n; i++)
        s += a[i]; // => co-03: unit-stride sequential access
    return s;      // returns the computed result
}
// mirrors k1_sum_sequential() above field-for-field -- only the access pattern
// differs.
static long k1_sum_random(const int *a, const int *idx,
                          long n) { // defines k1_sum_random(): helper function used by this example
    long s = 0;                     // declares s
    for (long i = 0; i < n; i++)
        s += a[idx[i]]; // => co-05: random-index access -- cache-hostile
    return s;           // returns the computed result
}
// run_kernel1() owns kernel 1's whole lifecycle: allocate, shuffle, time both
// variants via TIME_CALL, print kernel 1's report line, free, and hand back a
// single PASS/FAIL bit to main().
static int run_kernel1(void) {             // defines run_kernel1(): helper function used by this example
    int *a = malloc(sizeof(int) * K1_N);   // heap-allocates memory for a
    int *idx = malloc(sizeof(int) * K1_N); // heap-allocates memory for idx
    for (long i = 0; i < K1_N; i++) {      // => co-03: fills a and idx in one pass
        a[i] = (int)(i % 97);              // => co-03: a small repeating pattern
        idx[i] = i;                        // => co-03: idx starts as the IDENTITY permutation
    } // loop header controlling the sweep below
    unsigned seed = 1u;                     // declares seed
    for (long i = K1_N - 1; i > 0; i--) {   // => Fisher-Yates -- idx becomes a permutation
        seed = seed * 1103515245u + 12345u; // assigns seed
        long j = seed % (unsigned)(i + 1);  // declares j
        int tmp = idx[i];                   // => co-05: standard 3-step swap, first half
        idx[i] = idx[j];                    // => co-05: standard 3-step swap, second half
        idx[j] = tmp;                       // declares tmp
    }
    double t_seq = TIME_CALL(long, k1_sum_sequential, (const int *, const int *, long), a, idx, K1_N); // declares t_seq
    double t_rand = TIME_CALL(long, k1_sum_random, (const int *, const int *, long), a, idx,
                              K1_N); // declares t_rand
    int pass = t_seq < t_rand;       // declares pass
    printf("[1] sequential-vs-random-sum:   sequential=%.4fs  random=%.4fs  "
           "speedup=%.2fx  %s\n",
           t_seq, // prints a report line
           t_rand, t_rand / t_seq,
           pass ? "PASS" : "FAIL"); // continues the printf(...) call above
    free(a);
    free(idx);   // releases a's heap memory
    return pass; // returns the computed result
}

// ==================== kernel 2: row-major-vs-col-major (re-runs ex-29)
// ==================== co-03: identical K2_N x K2_N matrix, summed with the
// loop nest transposed -- row-major walks memory the way the array is actually
// laid out; column-major strides by a full row every step.
#define K2_N 2048 // constant K2_N = 2048
static long k2_sum_row_major(const int *m,
                             long n) { // defines k2_sum_row_major(): helper
                                       // function used by this example
    long s = 0;                        // declares s
    for (long i = 0; i < n; i++)       // loop header controlling the sweep below
        for (long j = 0; j < n; j++)
            s += m[i * n + j]; // => co-03: row-major traversal of row-major storage
    return s;                  // returns the computed result
}
// mirrors k2_sum_row_major() above -- only the i/j loop nesting order is
// swapped.
static long k2_sum_col_major(const int *m,
                             long n) { // defines k2_sum_col_major(): helper
                                       // function used by this example
    long s = 0;                        // declares s
    for (long j = 0; j < n; j++)       // loop header controlling the sweep below
        for (long i = 0; i < n; i++)
            s += m[i * n + j]; // => co-03: column-major traversal -- strides by n
    return s;                  // returns the computed result
}
// run_kernel2() mirrors run_kernel1()'s shape: allocate one shared matrix, time
// both traversal orders through TIME_CALL, report, free -- the same harness
// pattern reused kernel after kernel.
static int run_kernel2(void) {                  // defines run_kernel2(): helper function used by this example
    int *m = malloc(sizeof(int) * K2_N * K2_N); // heap-allocates memory for m
    for (long i = 0; i < K2_N * K2_N; i++)      // => co-03: one pass filling the whole flat matrix
        m[i] = (int)(i % 13);                   // loop header controlling the sweep below
    double t_row = TIME_CALL(long, k2_sum_row_major, (const int *, long), m,
                             K2_N); // declares t_row
    double t_col = TIME_CALL(long, k2_sum_col_major, (const int *, long), m,
                             K2_N); // declares t_col
    int pass = t_row < t_col;       // declares pass
    printf("[2] row-major-vs-col-major-sum: row=%.4fs  col=%.4fs  speedup=%.2fx  "
           "%s\n",
           t_row, t_col, // prints a report line
           t_col / t_row,
           pass ? "PASS" : "FAIL"); // continues the printf(...) call above
    free(m);                        // releases m's heap memory
    return pass;                    // returns the computed result
}

// ==================== kernel 3: blocked-vs-naive matmul (re-runs ex-32)
// ==================== co-03: same N x N x N multiply-accumulate work, naive
// ijk order vs K3_BLOCK-tiled -- blocking keeps each tile of a, b, and c
// resident in cache while it is reused, unlike the naive sweep.
#define K3_N 512    // constant K3_N = 512
#define K3_BLOCK 32 // constant K3_BLOCK = 32
static long k3_matmul_naive(const int *a, const int *b, int *c,
                            long n) {  // defines k3_matmul_naive(): helper function used by this example
    for (long i = 0; i < n; i++)       // loop header controlling the sweep below
        for (long j = 0; j < n; j++) { // loop header controlling the sweep below
            long sum = 0;              // declares sum
            for (long k = 0; k < n; k++)
                sum += a[i * n + k] * b[k * n + j]; // => co-03: b strides by n -- bad
            c[i * n + j] = (int)sum;                // supporting statement for this example
        }
    return c[0]; // returns the computed result
}
// mirrors k3_matmul_naive() above's math exactly -- only the loop tiling
// differs.
static long k3_matmul_blocked(const int *a, const int *b, int *c,
                              long n) { // defines k3_matmul_blocked(): helper
                                        // function used by this example
    for (long i = 0; i < n; i++)        // loop header controlling the sweep below
        for (long j = 0; j < n; j++)
            c[i * n + j] = 0;                                   // loop header controlling the sweep below
    for (long ii = 0; ii < n; ii += K3_BLOCK)                   // loop header controlling the sweep below
        for (long jj = 0; jj < n; jj += K3_BLOCK)               // loop header controlling the sweep below
            for (long kk = 0; kk < n; kk += K3_BLOCK)           // loop header controlling the sweep below
                for (long i = ii; i < ii + K3_BLOCK; i++)       // loop header controlling the sweep below
                    for (long j = jj; j < jj + K3_BLOCK; j++) { // loop header controlling the sweep below
                        long sum = c[i * n + j];                // declares sum
                        for (long k = kk; k < kk + K3_BLOCK; k++)
                            sum += a[i * n + k] * b[k * n + j]; // => co-03: tiled -- both hot
                        c[i * n + j] = (int)sum;                // supporting statement for this example
                    }
    return c[0]; // returns the computed result
}
// run_kernel3() is the one kernel that ALSO diff-checks its two outputs
// cell-by-cell (mismatches) before trusting the timing -- blocking reorders
// arithmetic, so correctness isn't automatic here.
static int run_kernel3(void) {                   // defines run_kernel3(): helper function used by this example
    int *a = malloc(sizeof(int) * K3_N * K3_N);  // heap-allocates memory for a
    int *b = malloc(sizeof(int) * K3_N * K3_N);  // heap-allocates memory for b
    int *c1 = malloc(sizeof(int) * K3_N * K3_N); // heap-allocates memory for c1
    int *c2 = malloc(sizeof(int) * K3_N * K3_N); // heap-allocates memory for c2
    for (long i = 0; i < K3_N * K3_N; i++) {     // => co-03: fills both source matrices in one pass
        a[i] = (int)(i % 5);                     // => co-03: a small repeating pattern for a
        b[i] = (int)(i % 7);                     // => co-03: a different repeating pattern for b
    } // loop header controlling the sweep below
    double t_naive = TIME_CALL(long, k3_matmul_naive, (const int *, const int *, int *, long), a, b, c1, K3_N);     // declares t_naive
    double t_blocked = TIME_CALL(long, k3_matmul_blocked, (const int *, const int *, int *, long), a, b, c2, K3_N); // declares t_blocked
    long mismatches = 0;                                                                                            // declares mismatches
    for (long i = 0; i < K3_N * K3_N; i++)                                                                          // => co-03: compares every output cell, naive vs blocked
        if (c1[i] != c2[i])                                                                                         // => co-03: a mismatch would mean blocking broke correctness
            mismatches++;                                                                                           // loop header controlling the sweep below
    int pass = (t_blocked < t_naive) && (mismatches == 0);                                                          // declares pass
    printf("[3] naive-vs-blocked-matmul:    naive=%.4fs  blocked=%.4fs  "
           "speedup=%.2fx  mismatches=%ld  %s\n", // prints a report line
           t_naive, t_blocked, t_naive / t_blocked, mismatches,
           pass ? "PASS" : "FAIL"); // continues the printf(...) call above
    free(a);                        // releases a's heap memory
    free(b);                        // releases b's heap memory
    free(c1);                       // releases c1's heap memory
    free(c2);                       // releases a's heap memory
    return pass;                    // returns the computed result
}

// ==================== kernel 4: SoA-vs-AoS hot-loop (re-runs ex-30)
// ==================== co-17: the SAME K4_N `hot` values, stored two ways --
// interleaved inside a 64 B AoS record vs packed into their own contiguous SoA
// array -- summing only `hot` needs none of AoS's `cold`.
#define K4_N 4000000 // constant K4_N = 4000000
typedef struct {     // => co-17: K4Aos -- the AoS record under comparison
    int hot;         // => co-17: the ONE field the hot loop below actually reads
    int cold[15];    // => co-17: 60 bytes of padding that shares hot's cache line
} K4Aos;             // => 64 bytes -- half a 128 B cache line per record
// K4Aos: `cold` is never read by k4_sum_aos below -- it exists ONLY to
// reproduce the realistic AoS penalty of a record with unrelated fields sharing
// its cache line with the field that matters.
static long k4_sum_aos(const K4Aos *arr,
                       long n) { // defines k4_sum_aos(): helper function used by this example
    long s = 0;                  // declares s
    for (long i = 0; i < n; i++)
        s += arr[i].hot; // => co-17: 64 B touched to read 4 useful bytes
    return s;            // returns the computed result
}
// mirrors k4_sum_aos() above's arithmetic exactly -- only the storage layout
// differs.
static long k4_sum_soa(const int *hot,
                       long n) { // defines k4_sum_soa(): helper function used by this example
    long s = 0;                  // declares s
    for (long i = 0; i < n; i++)
        s += hot[i]; // => co-17: 32 useful ints per 128 B line
    return s;        // returns the computed result
}
// run_kernel4() closes out the four-kernel pattern: allocate both layouts, fill
// them with the SAME values, time both sums via TIME_CALL, report, free --
// AoS's extra bytes are pure padding.
static int run_kernel4(void) {                 // defines run_kernel4(): helper function used by this example
    K4Aos *aos = malloc(sizeof(K4Aos) * K4_N); // heap-allocates memory for aos
    int *soa = malloc(sizeof(int) * K4_N);     // heap-allocates memory for soa
    for (long i = 0; i < K4_N; i++) {          // => co-17: fills both layouts with the SAME values
        aos[i].hot = soa[i] = (int)(i % 31);   // => co-17: identical hot values across both layouts
    } // loop header controlling the sweep below
    double t_aos = TIME_CALL(long, k4_sum_aos, (const K4Aos *, long), aos,
                             K4_N); // declares t_aos
    double t_soa = TIME_CALL(long, k4_sum_soa, (const int *, long), soa,
                             K4_N); // declares t_soa
    int pass = t_soa < t_aos;       // declares pass
    printf("[4] aos-vs-soa-hot-loop:        aos=%.4fs  soa=%.4fs  speedup=%.2fx  "
           "%s\n",
           t_aos, t_soa, // prints a report line
           t_aos / t_soa,
           pass ? "PASS" : "FAIL"); // continues the printf(...) call above
    free(aos);                      // releases aos's heap memory
    free(soa);                      // releases aos's heap memory
    return pass;                    // returns the computed result
}

// main() is deliberately thin: run each of the 4 kernels' self-contained
// run_kernelN() in turn, collect their PASS/FAIL bits into one array, and gate
// the whole program's exit code on ALL four holding at once -- one honest,
// single-run verdict instead of four separate claims.
int main(void) { // program entry point
    printf("mechanical-sympathy-recap: re-running 4 kernels from across this "
           "topic, in one program\n\n"); // prints a report line
    int results[4];                      // declares results
    results[0] = run_kernel1();          // assigns results[0]
    results[1] = run_kernel2();          // assigns results[1]
    results[2] = run_kernel3();          // assigns results[2]
    results[3] = run_kernel4();          // assigns results[3]

    int total_pass = 0; // declares total_pass
    for (int i = 0; i < 4; i++)
        total_pass += results[i]; // loop header controlling the sweep below
    printf("\n%d/4 kernels: cache-friendly beat cache-hostile\n",
           total_pass); // prints a report line
    printf("PASS (ALL 4 assertions hold -- cache-friendly wins EVERY kernel in "
           "this topic's own\n"); // prints a report line
    printf(" mini-suite): %s\n",
           total_pass == 4 ? "PASS" : "FAIL"); // prints a report line
    return total_pass == 4 ? 0 : 1;            // returns the computed result
}
