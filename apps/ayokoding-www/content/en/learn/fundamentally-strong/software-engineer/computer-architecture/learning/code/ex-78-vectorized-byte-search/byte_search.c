// learning/code/ex-78-vectorized-byte-search/byte_search.c
/* Example 78: a SIMD memchr-style byte search vs a scalar byte-by-byte loop. */
#include <arm_neon.h> // => co-23: NEON -- this machine is arm64, so NEON is the real SIMD ISA
#include <stdio.h>    // stdio.h: standard library header
#include <stdlib.h>   // stdlib.h: standard library header
#include <time.h>     // time.h: standard library header

#define BUF_SIZE \
    (64L * 1024 * 1024) // => co-23: 64 MB -- large enough that a byte-at-a-time scalar
                        // scan takes real, measurable time, especially worst-case

// ex-78: SCALAR search -- co-23: one comparison, one byte, per loop iteration.
// This is exactly what a hand-written `memchr` replacement looks like before
// anyone reaches for SIMD.
__attribute__((noinline)) static long scalar_find(const unsigned char *buf, long n,
                                                  unsigned char target) { // calls __attribute__(...)
    for (long i = 0; i < n; i++) {                                        // loop header controlling the sweep below
        if (buf[i] == target)
            return i; // => co-23: 1 byte compared per iteration
    }
    return -1; // returns the computed result
}

// ex-78: NEON search -- co-23: compares 16 bytes AT ONCE against the target
// with `vceqq_u8`, then `vmaxvq_u8` collapses the 16-lane comparison mask down
// to a single "did ANY lane match?" byte in one instruction -- only when that
// check is nonzero does the loop pay for a scalar scan to pin down the EXACT
// matching byte within that one 16-byte chunk (a rare event compared to how
// often the fast "no match in this chunk" path is taken).
__attribute__((noinline)) static long neon_find(const unsigned char *buf, long n,
                                                unsigned char target) { // calls __attribute__(...)
    uint8x16_t vtarget = vdupq_n_u8(target);                            // => co-23: broadcast the target byte into all 16 lanes
    long i = 0;                                                         // declares i
    for (; i + 16 <= n; i += 16) {                                      // loop header controlling the sweep below
        uint8x16_t chunk = vld1q_u8(buf + i);                           // => co-23: load 16 bytes in ONE instruction
        uint8x16_t cmp = vceqq_u8(chunk, vtarget);                      // => co-23: 16 parallel byte-equality comparisons
        if (vmaxvq_u8(cmp) != 0) {                                      // => co-23: "any lane nonzero?" reduction, ONE instruction
            for (int j = 0; j < 16; j++) {                              // => co-23: rare slow path -- pin down the exact byte
                if (buf[i + j] == target)
                    return i + j; // conditional check
            }
        }
    }
    for (; i < n; i++) { // => co-23: scalar tail for n not a multiple of 16
        if (buf[i] == target)
            return i; // conditional check
    }
    return -1; // returns the computed result
}

int main(void) {                           // program entry point
    unsigned char *buf = malloc(BUF_SIZE); // heap-allocates memory for buf
    if (!buf) {
        fprintf(stderr, "alloc failed\n");
        return 1;
    } // prints a report line
    for (long i = 0; i < BUF_SIZE; i++)
        buf[i] = (unsigned char)((i * 7 + 3) & 0x7F); // => never 0xFF anywhere

    unsigned char target = 0xFF;    // => co-23: a byte value that appears NOWHERE except
    long plant_at = BUF_SIZE - 100; // ...one planted position near the very END --
    buf[plant_at] = target;         // the worst case for a linear scan either way

    // co-23: both searches are called through a `volatile` function-pointer
    // VARIABLE -- ex-74's markdown documents in full why this is load-bearing:
    // scalar_find/neon_find are side-effect-free calls with the SAME arguments
    // every trial, and without this indirection clang's call-CSE folds all 5
    // timing trials into one real computation (measured during authoring: 0.0000
    // s and a "nanx" speedup for BOTH searches -- a benchmarking artifact, not a
    // real number).
    long (*volatile scalar_fn)(const unsigned char *, long, unsigned char) = scalar_find; // declares function pointer scalar_fn
    long (*volatile neon_fn)(const unsigned char *, long, unsigned char) = neon_find;     // declares function pointer neon_fn

    struct timespec t0, t1;                                                      // supporting statement for this example
    double best_scalar = -1.0, best_neon = -1.0;                                 // declares best_scalar
    long found_scalar = -1, found_neon = -1;                                     // declares found_scalar
    for (int trial = 0; trial < 5; trial++) {                                    // loop header controlling the sweep below
        clock_gettime(CLOCK_MONOTONIC, &t0);                                     // calls clock_gettime(...)
        found_scalar = scalar_fn(buf, BUF_SIZE, target);                         // assigns found_scalar
        clock_gettime(CLOCK_MONOTONIC, &t1);                                     // calls clock_gettime(...)
        double secs = (t1.tv_sec - t0.tv_sec) + (t1.tv_nsec - t0.tv_nsec) / 1e9; // declares secs
        if (best_scalar < 0 || secs < best_scalar)
            best_scalar = secs; // conditional check
    }
    for (int trial = 0; trial < 5; trial++) {                                    // loop header controlling the sweep below
        clock_gettime(CLOCK_MONOTONIC, &t0);                                     // calls clock_gettime(...)
        found_neon = neon_fn(buf, BUF_SIZE, target);                             // assigns found_neon
        clock_gettime(CLOCK_MONOTONIC, &t1);                                     // calls clock_gettime(...)
        double secs = (t1.tv_sec - t0.tv_sec) + (t1.tv_nsec - t0.tv_nsec) / 1e9; // declares secs
        if (best_neon < 0 || secs < best_neon)
            best_neon = secs; // conditional check
    }

    printf("BUF_SIZE=%ld bytes, target planted at index %ld (near end -- worst "
           "case)\n",
           BUF_SIZE, plant_at); // prints a report line
    printf("scalar search: best of 5 = %.4f s, found at index %ld\n", best_scalar,
           found_scalar); // prints a report line
    printf("NEON search:   best of 5 = %.4f s, found at index %ld\n", best_neon,
           found_neon);                                                   // prints a report line
    int correct = (found_scalar == plant_at) && (found_neon == plant_at); // declares correct
    double speedup = best_scalar / best_neon;                             // declares speedup
    printf("both found the SAME index: %s\n",
           correct ? "yes" : "NO -- BUG"); // prints a report line
    printf("speedup: %.2fx (PASS: correct + NEON faster) -> %s\n",
           speedup,                                       // prints a report line
           (correct && speedup > 1.5) ? "PASS" : "FAIL"); // continues the printf(...) call above

    free(buf); // releases buf's heap memory
    return 0;  // returns the computed result
}
