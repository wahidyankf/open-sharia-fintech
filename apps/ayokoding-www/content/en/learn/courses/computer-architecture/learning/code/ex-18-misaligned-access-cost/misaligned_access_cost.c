// learning/code/ex-18-misaligned-access-cost/misaligned_access_cost.c
/* Example 18: Misaligned Access Cost -- aligned vs 1-byte-shifted uint64_t
 * reads, timed. */

#include <stdint.h> // => co-16: uint64_t -- the 8-byte value being read aligned vs misaligned
#include <stdio.h>  // => co-16: printf -- reports both timings and the honest verdict
#include <stdlib.h> // => co-16: malloc/free -- the buffer both pointers read from
#include <time.h>   // => co-25: clock_gettime -- portable wall-clock timing (see the shared brief)

#define BUF_BYTES \
    (64u * 1024u * 1024u) // => co-16: 64 MiB -- far bigger than any cache level
                          // on this machine
#define PASSES 5          // => co-25: best-of-N -- DD-20 requires re-running noisy timings

static double now_seconds(void) { // => co-25: one monotonic-clock read, converted to seconds
    struct timespec ts;           // => co-25: CLOCK_MONOTONIC -- immune to wall-clock adjustments
    clock_gettime(CLOCK_MONOTONIC,
                  &ts);                                  // => co-25: POSIX call, portable to any Unix (per the shared brief)
    return (double)ts.tv_sec + (double)ts.tv_nsec / 1e9; // => co-25: whole seconds + fractional nanoseconds
}

// ex-18: sums every 8th byte read as a uint64_t starting at `start` --
// `volatile` forces the compiler to actually perform each load rather than
// optimizing the whole loop away, which -O2 would otherwise do since the sum is
// never used meaningfully
static uint64_t sum_stride8(const unsigned char *start,
                            size_t buf_bytes) {                // defines sum_stride8(): helper
                                                               // function used by this example
    volatile uint64_t total = 0;                               // => co-16: volatile defeats dead-code elimination of the reads
    size_t count = (buf_bytes - 8) / 8;                        // => co-16: number of full 8-byte reads that fit before the end
    for (size_t i = 0; i < count; i++) {                       // => co-16: one read per 8-byte stride step
        const uint64_t *p = (const uint64_t *)(start + i * 8); // => co-16: pointer into the buffer,
                                                               // offset by `start`'s shift
        total += *p;                                           // => co-16: THE misaligned-or-aligned read under test
    }
    return total; // => co-16: unused beyond preventing optimization
}

int main(void) {                                // program entry point
    unsigned char *buf = malloc(BUF_BYTES + 8); // => co-16: +8 headroom so the misaligned pass
                                                // never reads past the end
    if (!buf) {
        fprintf(stderr, "malloc failed\n");
        return 1;
    } // => co-16: defensive -- 64 MiB should always succeed here
    for (size_t i = 0; i < BUF_BYTES + 8; i++)
        buf[i] = (unsigned char)(i * 2654435761u); // => co-16: deterministic filler pattern

    double aligned_best = 1e300,
           misaligned_best = 1e300; // => co-25: best-of-N trackers, start at "worse than anything"
    uint64_t sink = 0;              // => co-16: accumulates results so the compiler can't discard passes

    for (int pass = 0; pass < PASSES; pass++) { // => co-25: PASSES repetitions, keep the fastest of each
        double t0 = now_seconds();              // => co-25: start the aligned-read timer
        sink += sum_stride8(buf,
                            BUF_BYTES); // => co-16: buf is malloc-aligned -- ALIGNED 8-byte reads
        double t1 = now_seconds();      // => co-25: stop the aligned-read timer
        if (t1 - t0 < aligned_best)
            aligned_best = t1 - t0; // => co-25: keep the fastest aligned run so far

        double t2 = now_seconds(); // => co-25: start the misaligned-read timer
        sink += sum_stride8(buf + 1,
                            BUF_BYTES); // => co-16: buf+1 shifts every 8-byte read off alignment
        double t3 = now_seconds();      // => co-25: stop the misaligned-read timer
        if (t3 - t2 < misaligned_best)
            misaligned_best = t3 - t2; // => co-25: keep the fastest misaligned run so far
    }

    double ratio = misaligned_best / aligned_best; // => co-25: relative comparison, not a
                                                   // hardcoded absolute number
    printf("aligned best of %d    = %.6f s\n", PASSES,
           aligned_best); // => co-25: fastest aligned pass
    printf("misaligned best of %d = %.6f s\n", PASSES,
           misaligned_best); // => co-25: fastest misaligned pass
    printf("misaligned / aligned  = %.3fx\n",
           ratio); // => co-25: >1.0 means misaligned was slower
    printf("sink (ignore)         = %llu\n",
           (unsigned long long)sink); // => co-16: proves the reads were not optimized away

    // ex-18: HONEST VERDICT -- Apple Silicon's load/store unit tolerates
    // misaligned accesses in hardware (unlike strict-alignment ISAs, e.g. classic
    // ARMv5/MIPS, which trap with SIGBUS), so the measured gap here is expected
    // to be SMALL and possibly within run-to-run noise -- we report the real
    // ratio rather than forcing a "misaligned is dramatically slower" narrative
    // this machine does not support.
    if (ratio > 1.05) { // => co-25: a real, if modest, measured slowdown
        printf("VERDICT: misaligned reads measured %.1f%% slower on this run\n",
               (ratio - 1.0) * 100.0);                                           // prints a report line
    } else {                                                                     // => co-25: the honest, machine-accurate outcome
        printf("VERDICT: no reliably measurable gap on this arm64 machine -- "); // prints
                                                                                 // a
                                                                                 // report
                                                                                 // line
        printf("hardware misaligned-load support makes the two statistically "
               "close\n"); // prints a report line
    }

    free(buf); // => co-16: releases the 64 MiB buffer
    return 0;  // => co-16: this example reports, it does not assert PASS/FAIL
}
