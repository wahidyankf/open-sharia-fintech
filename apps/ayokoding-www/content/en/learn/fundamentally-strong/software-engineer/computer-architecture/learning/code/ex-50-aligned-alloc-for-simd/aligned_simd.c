// learning/code/ex-50-aligned-alloc-for-simd/aligned_simd.c
/* Example 50: use C11 aligned_alloc for NEON loads -- verify the returned
   pointer's alignment and compare an aligned vs a deliberately misaligned
   NEON summation (co-16, co-23). */
#include <arm_neon.h> // => co-23: NEON intrinsics -- vld1q_f32 is used both aligned and misaligned below
#include <stdint.h>   // => uintptr_t -- printing/checking a pointer's numeric alignment
#include <stdio.h>    // => printf -- the alignment/timing/PASS report this program prints
#include <stdlib.h>   // => aligned_alloc/free/rand -- co-16: the C11 alignment-aware allocator under test
#include <time.h>     // => clock_gettime -- the portable wall-clock timer used below

#define ALIGN \
    64 // => co-16: align to a full 64 B boundary -- comfortably covers NEON's 16
       // B
       //    vector width with room to spare (also a common SIMD-tuning alignment
       //    target)
#define N \
    100000000    // => co-23: 100M floats -- large enough for a wall-clock-visible
                 // NEON pass
#define TRIALS 5 // => co-25: best-of-5 -- shared-machine noise smoothing

static double now_seconds(void) {                        // => co-25: shared wall-clock helper, this topic's standard pattern
    struct timespec ts;                                  // supporting statement for this example
    clock_gettime(CLOCK_MONOTONIC, &ts);                 // calls clock_gettime(...)
    return (double)ts.tv_sec + (double)ts.tv_nsec / 1e9; // returns the computed result
}

// co-23: NEON summation, 4 lanes at a time -- used on BOTH the aligned buffer
// and a 1-float-shifted (deliberately misaligned) view of the SAME data.
__attribute__((noinline)) static float simd_sum(const float *p, int n, float salt) { // calls __attribute__(...)
    float32x4_t vsum = vdupq_n_f32(0.0f);                                            // declares vsum
    int i = 0;                                                                       // declares i
    for (; i + 4 <= n; i += 4) {                                                     // loop header controlling the sweep below
        float32x4_t v = vld1q_f32(&p[i]);                                            // => co-23: vld1q_f32 handles unaligned addresses
        vsum = vaddq_f32(vsum, v);                                                   //    correctly on arm64 (unlike classic x86 SSE,
    } //    which historically faulted on misaligned loads)
    float sum = vaddvq_f32(vsum); // declares sum
    for (; i < n; i++)
        sum += p[i];   // loop header controlling the sweep below
    return sum + salt; // => co-25: salt distinguishes each trial's call (see ex-47/48)
}

int main(void) { // program entry point
    // co-16: aligned_alloc requires size to be a multiple of the alignment -- pad
    // N+4 up so (N+4)*sizeof(float) is a clean multiple of ALIGN.
    size_t raw_floats = (size_t)N + 4;           // declares raw_floats
    size_t bytes = raw_floats * sizeof(float);   // declares bytes
    bytes = (bytes + ALIGN - 1) / ALIGN * ALIGN; // => co-16: round UP to the next multiple of ALIGN
    float *buf = aligned_alloc(ALIGN, bytes);    // => co-16: C11's alignment-aware allocator
    if (!buf) {
        fprintf(stderr, "alloc failed\n");
        return 1;
    } // prints a report line

    uintptr_t addr = (uintptr_t)buf;                                                                   // declares addr
    int is_aligned = (addr % ALIGN == 0);                                                              // => co-16: verify the CONTRACT aligned_alloc promises
    printf("aligned_alloc(%d, %zu) returned %p, addr %% %d == %lu -> %s\n", ALIGN, bytes, (void *)buf, // prints a report line
           ALIGN, (unsigned long)(addr % ALIGN),
           is_aligned ? "PASS (properly aligned)" : "FAIL"); // continues the printf(...) call above

    srand(41); // calls srand(...)
    for (size_t i = 0; i < raw_floats; i++)
        buf[i] = (float)(rand() % 100) * 0.01f; // loop header controlling the sweep below

    float *aligned_view = buf;                                                    // => co-16: starts exactly at the aligned address
    float *misaligned_view = buf + 1;                                             // => co-16: shifted by 1 float (4 B) -- deliberately
                                                                                  //    NOT a multiple of 16 B (NEON's natural vector width)
    printf("aligned_view addr %% 16 == %lu, misaligned_view addr %% 16 == %lu\n", // prints a report line
           (unsigned long)((uintptr_t)aligned_view % 16),
           (unsigned long)((uintptr_t)misaligned_view % 16)); // continues the printf(...) call above

    double best_aligned = 1e18, best_misaligned = 1e18;                // declares best_aligned
    float last_aligned = 0.0f, last_misaligned = 0.0f;                 // declares last_aligned
    for (int t = 0; t < TRIALS; t++) {                                 // => co-25: best-of-N -- keep the fastest clean run
        double t0 = now_seconds();                                     // declares t0
        last_aligned = simd_sum(aligned_view, N, (float)t) - (float)t; // assigns last_aligned
        double t1 = now_seconds();                                     // declares t1
        if (t1 - t0 < best_aligned)
            best_aligned = t1 - t0; // conditional check

        double t2 = now_seconds();                                           // declares t2
        last_misaligned = simd_sum(misaligned_view, N, (float)t) - (float)t; // assigns last_misaligned
        double t3 = now_seconds();                                           // declares t3
        if (t3 - t2 < best_misaligned)
            best_misaligned = t3 - t2; // conditional check
    }

    printf("N=%d floats, best of %d\n", N, TRIALS); // prints a report line
    printf("aligned NEON sum:    %.6f, %.4f s\n", last_aligned,
           best_aligned); // prints a report line
    printf("misaligned NEON sum: %.6f, %.4f s (SAME data, shifted by 1 element)\n",
           last_misaligned,                             // prints a report line
           best_misaligned);                            // continues the printf(...) call above
    double ratio = best_misaligned / best_aligned;      // declares ratio
    printf("misaligned/aligned ratio: %.3fx\n", ratio); // prints a report line
    printf(                                             // prints a report line
        "FINDING (measured, per co-25): on THIS arm64 core, NEON unaligned loads "
        "%s --\n"                                                                             // continues the printf(...) call above
        "%s\n",                                                                               // continues the printf(...) call above
        ratio > 1.05 ? "cost measurably more" : "cost essentially the same as aligned loads", // continues the
                                                                                              // printf(...) call
                                                                                              // above
        ratio > 1.05                                                                          // continues the printf(...) call above
            ? "the alignment contract aligned_alloc provides is worth real "
              "cycles here" // continues the printf(...) call above
            : "arm64's load/store unit handles unaligned NEON accesses "
              "efficiently in the common\n" // continues the printf(...) call
                                            // above
              "case -- unlike classic x86 SSE, which historically required "
              "alignment or faulted"); // continues the printf(...) call above
    free(buf);                         // releases buf's heap memory
    return is_aligned ? 0 : 1;         // => co-16: the alignment CONTRACT is this
                                       // example's hard gate
}
