// learning/code/ex-72-roofline-bandwidth-vs-compute/roofline.c
/* Example 72: a self-calibrated roofline -- a bandwidth-bound kernel vs a
 * compute-bound kernel. */
#include <arm_neon.h> // => co-23: NEON FMA -- the compute-only calibration below needs a KNOWN,
                      // fixed flop count per instruction, which explicit intrinsics guarantee
                      // (auto-vectorization output can vary by compiler version -- intrinsics don't).
#include <stdio.h>    // stdio.h: standard library header
#include <stdlib.h>   // stdlib.h: standard library header
#include <time.h>     // time.h: standard library header

// co-25: this machine has no `perf`/roofline-toolkit (Linux-only tools); the
// methodology below is the honest substitute -- CALIBRATE this machine's own
// achievable bandwidth and compute rate with two microbenchmarks, then check
// that a memory-bound kernel and a compute-bound kernel each land where THOSE
// self-measured ceilings, not a fabricated vendor spec sheet, predict they
// should.

#define BIG_N \
    (32L * 1024 * 1024)                                // => co-01: 32M floats = 128 MB per array -- far bigger than the
                                                       // 4 MiB L2, so this is a genuine DRAM-bandwidth-bound workload
static double now_secs(void) {                         // defines now_secs(): helper function used by this example
    struct timespec t;                                 // supporting statement for this example
    clock_gettime(CLOCK_MONOTONIC, &t);                // calls clock_gettime(...)
    return (double)t.tv_sec + (double)t.tv_nsec / 1e9; // returns the computed result
}

// ex-72: BANDWIDTH CALIBRATION -- an elementwise "scale-copy" (`dst[i] = src[i]
// * k`): 1 read + 1 write per element, and a trivially cheap single multiply
// that keeps every element INDEPENDENT of every other (no reduction dependency
// chain). co-01: this measures the closest thing to "this machine's achievable
// DRAM read+write bandwidth" a userspace C program can honestly produce without
// a vendor spec sheet. Two earlier designs were tried and rejected during
// authoring: a pure `dst[i]=src[i]` copy gets rewritten by clang's
// loop-idiom-recognition pass into a `memcpy` call that can complete via a
// copy-on-write VM remap instead of physically moving bytes (measured at
// effectively 0 s -- "inf GB/s"); a read-only SUM reduction has a serial add
// dependency chain that caps throughput on FP-add latency, not on bandwidth
// (measured far BELOW kernel A's own elementwise-store bandwidth below, which
// is a contradiction -- a calibration ceiling cannot be lower than a real
// kernel that supposedly sits AT that ceiling). The multiply-by-constant avoids
// both traps: not a byte-identical copy (no idiom rewrite), and no
// cross-element dependency chain.
__attribute__((noinline)) static double calibrate_bandwidth_gbs(const float *src, float *dst,
                                                                long n) { // calls __attribute__(...)
    double best = -1.0;                                                   // declares best
    for (int t = 0; t < 7; t++) {                                         // => best-of-7: this is a shared dev machine,
                                                                          // not an isolated bench rig
        double t0 = now_secs();                                           // declares t0
        for (long i = 0; i < n; i++)
            dst[i] = src[i] * 1.0000001f; // => co-01: 1 read + 1 write, independent per element
        double secs = now_secs() - t0;    // declares secs
        if (best < 0 || secs < best)
            best = secs; // conditional check
    }
    double bytes = (double)n * 2.0 * sizeof(float); // => 1 read + 1 write, 4 bytes each
    return (bytes / best) / 1e9;                    // => GB/s
}

// ex-72: COMPUTE CALIBRATION -- 4 independent NEON FMA chains, entirely
// register-resident (no array, no memory traffic at all after the initial
// constants). co-23: 4 independent chains give the core enough independent work
// to fill its FMA pipeline's latency, so this approaches the throughput ceiling
// for THIS exact FMA pattern on THIS core, not a fabricated number.
#define COMPUTE_ITERS 100000000L                                                        // constant COMPUTE_ITERS = 100000000L
__attribute__((noinline)) static float compute_calibration_gflops(double *out_gflops) { // calls __attribute__(...)
    float32x4_t acc0 = vdupq_n_f32(1.0f),
                acc1 = vdupq_n_f32(1.0001f); // declares acc0
    float32x4_t acc2 = vdupq_n_f32(0.9998f),
                acc3 = vdupq_n_f32(1.0003f);   // declares acc2
    float32x4_t mul = vdupq_n_f32(1.0000001f); // => co-23: fractionally above 1.0 -- bounded growth
    float32x4_t add = vdupq_n_f32(0.0000001f); // over COMPUTE_ITERS (e^10 ~= 22026, nowhere
                                               // near float overflow)
    double t0 = now_secs();                    // declares t0
    for (long i = 0; i < COMPUTE_ITERS; i++) { // loop header controlling the sweep below
        acc0 = vmlaq_f32(add, acc0, mul);      // => co-23: acc0 = add + acc0*mul -- 4
                                               // lanes x (1 mul + 1 add) = 8 flops
        acc1 = vmlaq_f32(add, acc1, mul);      // => 4 independent chains -- keeps the
                                               // FMA pipeline fed every cycle
        acc2 = vmlaq_f32(add, acc2, mul);      // assigns acc2
        acc3 = vmlaq_f32(add, acc3, mul);      // assigns acc3
    }
    double secs = now_secs() - t0;                                                                                   // declares secs
    float32x4_t sum = vaddq_f32(vaddq_f32(acc0, acc1), vaddq_f32(acc2, acc3));                                       // => combine so nothing is dead
    float total = vgetq_lane_f32(sum, 0) + vgetq_lane_f32(sum, 1) + vgetq_lane_f32(sum, 2) + vgetq_lane_f32(sum, 3); // declares total
    double flops = (double)COMPUTE_ITERS * 4.0 /* chains */ * 4.0 /* lanes */ * 2.0 /* mul+add */;
    *out_gflops = (flops / secs) / 1e9; // supporting statement for this example
    return total;                       // => returned and printed so the whole calibration can never be
                                        // dead-code-eliminated
}

// ex-72: KERNEL A -- memory-bound "triad" (c[i] = a[i] + s*b[i]) over huge
// arrays. co-01: 3 arrays touched per element (2 reads + 1 write = 12 bytes), 2
// flops (1 mul + 1 add) -- arithmetic intensity = 2/12 ~= 0.167 flops/byte,
// deliberately tiny, so bandwidth should dominate its runtime. `noinline`, and
// `c`'s contents are checksummed by the caller after this returns -- both are
// load-bearing: without them, main() never actually OBSERVES a single byte of
// `c`, and clang's interprocedural dead-store elimination is legally entitled
// to (and, verified during authoring, DID) delete the entire loop -- reads of
// a[]/b[] included -- reporting a suspicious near-0 s runtime ("inf GFLOP/s",
// another benchmarking artifact caught by comparing against the isolated
// single-function test this example's markdown documents running first).
__attribute__((noinline)) static double kernel_a_triad(const float *a, const float *b, float *c,
                                                       long n, // calls __attribute__(...)
                                                       double scalar, double *out_gflops,
                                                       double *out_gbs) { // declares scalar
    double best = -1.0;                                                   // declares best
    for (int t = 0; t < 7; t++) {                                         // => best-of-7, matching the bandwidth
                                                                          // calibration's trial count above
        double t0 = now_secs();                                           // declares t0
        for (long i = 0; i < n; i++)
            c[i] = a[i] + (float)scalar * b[i]; // => co-01: 2 mul+add flops, 12 bytes moved
        double secs = now_secs() - t0;          // declares secs
        if (best < 0 || secs < best)
            best = secs; // conditional check
    }
    double bytes = (double)n * 3.0 * sizeof(float); // declares bytes
    double flops = (double)n * 2.0;                 // declares flops
    *out_gflops = (flops / best) / 1e9;             // supporting statement for this example
    *out_gbs = (bytes / best) / 1e9;                // supporting statement for this example
    return best;                                    // returns the computed result
}

// ex-72: KERNEL B -- compute-bound: a SMALL array (fits comfortably in this
// machine's 64 KiB L1d) touched by many FMA passes per outer repeat. co-01:
// after the first touch, EVERY later access is served from L1d, so DRAM
// bandwidth is nearly irrelevant here -- arithmetic intensity is huge, and
// runtime should track the compute calibration above, not the bandwidth
// calibration.
#define SMALL_N 4096 // => 4096 floats = 16 KB -- comfortably inside the 64 KiB L1d
#define SMALL_REPEATS \
    40000 // => co-01: enough outer repeats to make L1-resident compute dominate
          // the timing
__attribute__((noinline)) static double kernel_b_compute(float *arr, long n, long repeats,
                                                         double *out_gflops) { // calls __attribute__(...)
    double t0 = now_secs();                                                    // declares t0
    float m = 1.0000003f, a = 0.0000002f;                                      // => same "bounded FMA drift" trick as
                                                                               // the calibration above
    for (long r = 0; r < repeats; r++) {                                       // loop header controlling the sweep below
        for (long i = 0; i < n; i++) {                                         // loop header controlling the sweep below
            arr[i] = arr[i] * m + a;                                           // => co-01: 1 mul + 1 add per element, ALL from L1d after r=0
        }
    }
    double secs = now_secs() - t0;                    // declares secs
    double flops = (double)n * (double)repeats * 2.0; // declares flops
    *out_gflops = (flops / secs) / 1e9;               // supporting statement for this example
    return secs;                                      // returns the computed result
}

int main(void) {                                    // program entry point
    float *big_a = malloc(sizeof(float) * BIG_N);   // heap-allocates memory for big_a
    float *big_b = malloc(sizeof(float) * BIG_N);   // heap-allocates memory for big_b
    float *big_c = malloc(sizeof(float) * BIG_N);   // heap-allocates memory for big_c
    float *big_d = malloc(sizeof(float) * BIG_N);   // => scratch destination for the bandwidth calibration
    float *small = malloc(sizeof(float) * SMALL_N); // heap-allocates memory for small
    if (!big_a || !big_b || !big_c || !big_d || !small) {
        fprintf(stderr, "alloc failed\n");
        return 1;
    } // prints a report line
    for (long i = 0; i < BIG_N; i++) {
        big_a[i] = (float)(i % 97) * 0.01f;
        big_b[i] = (float)(i % 53) * 0.02f;
    } // loop header controlling the sweep below
    for (long i = 0; i < SMALL_N; i++)
        small[i] = 1.0f + (float)(i % 7) * 0.001f; // loop header controlling the sweep below

    double bw_calibration_gbs = calibrate_bandwidth_gbs(big_a, big_d, BIG_N); // declares bw_calibration_gbs
    // co-01: OBSERVE big_d's contents for the same interprocedural-DCE reason as
    // big_c below.
    volatile float d_checksum = 0.0f; // declares d_checksum
    for (long i = 0; i < BIG_N; i += 4093)
        d_checksum += big_d[i];                                         // loop header controlling the sweep below
    double compute_gflops;                                              // declares compute_gflops
    float compute_result = compute_calibration_gflops(&compute_gflops); // declares compute_result

    double a_gflops, a_gbs; // declares a_gflops
    double a_secs = kernel_a_triad(big_a, big_b, big_c, BIG_N, 2.5, &a_gflops,
                                   &a_gbs); // declares a_secs
    (void)a_secs;                           // discards a_secs to silence an unused-variable warning
    // co-01: OBSERVE big_c's contents -- without this, main() never reads a
    // single byte kernel_a_triad wrote, and (verified during authoring) clang's
    // interprocedural DCE deletes the whole loop.
    volatile float c_checksum = 0.0f; // declares c_checksum
    for (long i = 0; i < BIG_N; i += 4093)
        c_checksum += big_c[i]; // => sparse sample -- cheap, still a real read

    double b_gflops; // declares b_gflops
    double b_secs = kernel_b_compute(small, SMALL_N, SMALL_REPEATS,
                                     &b_gflops); // declares b_secs
    (void)b_secs;                                // discards b_secs to silence an unused-variable warning
    volatile float small_checksum = 0.0f;        // => same reasoning -- OBSERVE `small`'s post-kernel-B contents
    for (long i = 0; i < SMALL_N; i++)
        small_checksum += small[i]; // loop header controlling the sweep below

    double ai_a = 2.0 / (3.0 * sizeof(float));             // => flops per byte for the triad
    double predicted_a_gflops = ai_a * bw_calibration_gbs; // => roofline's bandwidth-bound prediction

    printf("--- calibration (this machine's own measured ceilings, not a vendor "
           "spec) ---\n"); // prints a report line
    printf("streaming scale-copy bandwidth: %.2f GB/s (d-checksum=%.4f, ignore "
           "-- proves no dead-store elim)\n", // prints a report line
           bw_calibration_gbs,
           (double)d_checksum); // continues the printf(...) call above
    printf("register-only FMA compute: %.2f GFLOP/s (sink=%.4f, ignore -- proves "
           "no dead-code elim)\n", // prints a report line
           compute_gflops,
           (double)compute_result); // continues the printf(...) call above
    printf("\n--- kernel A: memory-bound triad, arithmetic intensity=%.4f "
           "flops/byte ---\n",
           ai_a); // prints a report line
    printf("measured: %.2f GFLOP/s, %.2f GB/s (c-checksum=%.4f, ignore -- proves "
           "no dead-store elim)\n",
           a_gflops,                   // prints a report line
           a_gbs, (double)c_checksum); // continues the printf(...) call above
    printf("roofline-predicted GFLOP/s (= intensity * measured bandwidth): %.2f "
           "GFLOP/s\n",
           predicted_a_gflops); // prints a report line
    printf("\n--- kernel B: compute-bound, %d floats resident in L1d, %d repeats "
           "---\n",
           SMALL_N, SMALL_REPEATS); // prints a report line
    printf("measured: %.2f GFLOP/s (small-checksum=%.4f, ignore -- proves no "
           "dead-store elim)\n",
           b_gflops,                // prints a report line
           (double)small_checksum); // continues the printf(...) call above

    double a_predicted_ratio = a_gflops / predicted_a_gflops; // declares a_predicted_ratio
    double b_vs_compute_ratio = b_gflops / compute_gflops;    // declares b_vs_compute_ratio
    double b_vs_a_ratio = b_gflops / a_gflops;                // declares b_vs_a_ratio
    printf("\nkernel A sits within %.0f%% of its bandwidth-bound roofline "
           "prediction\n",
           a_predicted_ratio * 100.0); // prints a report line
    printf("kernel B reaches %.0f%% of the register-only compute ceiling\n",
           b_vs_compute_ratio * 100.0); // prints a report line
    printf("kernel B outruns kernel A by %.1fx in GFLOP/s despite touching far "
           "less DRAM bandwidth\n", // prints a report line
           b_vs_a_ratio);           // continues the printf(...) call above

    // co-25: this is a general-purpose dev machine, not a perf-isolated
    // benchmarking rig -- run-to-run noise (thermal state, background processes)
    // moves the bandwidth calibration by up to ~2x between runs (observed during
    // authoring). The tolerance band below is deliberately an ORDER-OF-MAGNITUDE
    // check, not a tight one: it verifies kernel A sits on the bandwidth-bound
    // roofline LINE, not at an exact point on it -- which is exactly what the
    // roofline MODEL itself predicts, no more precisely.
    int pass = (a_predicted_ratio > 0.25 && a_predicted_ratio < 4.0) && // A tracks its bandwidth-bound prediction
               (b_vs_compute_ratio > 0.05) &&                           // B is genuinely compute-bound, not stalled
               (b_vs_a_ratio > 1.2);                                    // B's higher intensity really pays off
    printf("PASS (A sits on the bandwidth-bound roofline, B sits far closer to "
           "the compute roofline): %s\n", // prints a report line
           pass ? "PASS" : "FAIL");       // continues the printf(...) call above

    free(big_a);
    free(big_b);
    free(big_c);
    free(big_d);
    free(small); // releases big_a's heap memory
    return 0;    // returns the computed result
}
