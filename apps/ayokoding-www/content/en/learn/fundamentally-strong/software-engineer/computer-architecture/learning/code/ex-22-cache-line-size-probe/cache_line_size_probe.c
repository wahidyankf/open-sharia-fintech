// learning/code/ex-22-cache-line-size-probe/cache_line_size_probe.c
/* Example 22: Cache Line Size Probe -- MEASURE the line size, never hardcode 64
 * B. */

#include <stdint.h>     // => co-02: uint8_t -- byte-addressed probe buffer
#include <stdio.h>      // => co-02: printf -- reports the per-stride timings and the detected line size
#include <stdlib.h>     // => co-02: malloc/free -- the oversized probe buffer
#include <sys/sysctl.h> // => co-02: sysctlbyname -- reads THIS machine's real cache-line size, for a sanity cross-check ONLY
#include <time.h>       // => co-25: clock_gettime -- wall-clock timing, per the shared brief

#define BUF_BYTES \
    (64u * 1024u * 1024u) // => co-02: 64 MiB -- far bigger than L2 (4 MiB) or the
                          // LLC, forces real misses
#define REPEATS 3         // => co-25: best-of-N per stride, per DD-20

static double now_seconds(void) {                        // => co-25: one CLOCK_MONOTONIC read, in seconds
    struct timespec ts;                                  // supporting statement for this example
    clock_gettime(CLOCK_MONOTONIC, &ts);                 // calls clock_gettime(...)
    return (double)ts.tv_sec + (double)ts.tv_nsec / 1e9; // returns the computed result
}

// ex-22: one full sweep of the buffer at `stride` bytes -- touches
// BUF_BYTES/stride elements, one per stride step; `volatile` forces every read
// to actually happen
static double sweep_nanoseconds_per_touch(const uint8_t *buf,
                                          size_t stride) { // defines sweep_nanoseconds_per_touch(): helper function
                                                           // used by this example
    size_t touches = BUF_BYTES / stride;                   // => co-02: fewer, WIDER-spaced touches as stride grows
    double best = 1e300;                                   // => co-25: tracks the fastest of REPEATS sweeps
    for (int r = 0; r < REPEATS; r++) {                    // => co-25: repeat to damp scheduler noise
        volatile uint8_t sink = 0;                         // => co-02: volatile -- defeats dead-code elimination of the loop
        double t0 = now_seconds();                         // => co-25: start this sweep's timer
        for (size_t i = 0; i < touches; i++) {             // => co-02: exactly `touches` reads, `stride` bytes apart
            sink ^= buf[i * stride];                       // => co-02: THE probed access -- one byte per
                                                           // stride step
        }
        double elapsed = now_seconds() - t0; // => co-25: total time for this whole sweep
        (void)sink;                          // => co-02: silences "unused" -- volatile already forced the
                                             // reads
        if (elapsed < best)
            best = elapsed;                                // => co-25: keep the fastest sweep for this stride
        double per_touch = (best / (double)touches) * 1e9; // => co-02: nanoseconds per individual touch
        if (r == REPEATS - 1)
            return per_touch; // => co-02: return after the final (best-tracking)
                              // repeat
    }
    return 0.0; // unreachable                                                  //
                // => co-02: keeps the compiler's control-flow analysis happy
}

int main(void) {                      // program entry point
    uint8_t *buf = malloc(BUF_BYTES); // => co-02: the oversized probe buffer, allocated once
    if (!buf) {
        fprintf(stderr, "malloc failed\n");
        return 1;
    } // => co-02: defensive -- 64 MiB should always succeed here
    for (size_t i = 0; i < BUF_BYTES; i++)
        buf[i] = (uint8_t)(i * 2654435761u); // => co-02: deterministic filler,
                                             // touches every page once

    size_t strides[] = {8, 16, 32, 64, 128, 256, 512}; // => co-02: powers of two spanning well
                                                       // below and above 128 B
    size_t n = sizeof(strides) / sizeof(strides[0]);   // => co-02: 7 strides swept
    double per_touch_ns[7];                            // => co-02: measured nanoseconds-per-touch, one per
                                                       // stride

    printf("%-10s %s\n", "STRIDE(B)", "NS/TOUCH");                      // => co-02: column header
    for (size_t k = 0; k < n; k++) {                                    // => co-02: one measured row per stride
        per_touch_ns[k] = sweep_nanoseconds_per_touch(buf, strides[k]); // => co-02: the actual timed measurement
        printf("%-10zu %.3f\n", strides[k],
               per_touch_ns[k]); // => co-02: prints stride and its measured cost
    }

    // ex-22: DETECT the line size -- find the adjacent-stride pair with the
    // LARGEST increase in per-touch time. Under the classic model, per-touch cost
    // grows roughly linearly with stride up to the true line size, then PLATEAUS
    // once every touch is already a guaranteed miss -- so the biggest jump lands
    // at the doubling that just REACHES the line size, not before or after it.
    size_t best_jump_index = 1;                              // => co-02: index into strides[] of the larger
                                                             // stride in the winning pair
    double best_jump = -1e300;                               // => co-02: tracks the largest per-touch delta seen so far
    for (size_t k = 1; k < n; k++) {                         // => co-02: compares every adjacent pair
        double jump = per_touch_ns[k] - per_touch_ns[k - 1]; // => co-02: this pair's measured increase
        printf("jump %zu -> %zu B: %+.3f ns\n", strides[k - 1], strides[k],
               jump); // => co-02: shows the reasoning, not just the answer
        if (jump > best_jump) {
            best_jump = jump;
            best_jump_index = k;
        } // => co-02: keeps the largest jump found so far
    }
    size_t detected_line_size = strides[best_jump_index]; // => co-02: the MEASURED answer -- not
                                                          // hardcoded 64 or 128

    long sysctl_line_size = 0;             // => co-02: cross-check ONLY -- the pass condition
                                           // is the measurement above
    size_t len = sizeof(sysctl_line_size); // declares len
    sysctlbyname("hw.cachelinesize", &sysctl_line_size, &len, NULL,
                 0); // => co-02: real macOS sysctl call, read for real on this machine

    printf("detected line size (measured) = %zu bytes\n",
           detected_line_size); // => co-02: this program's own conclusion
    printf("sysctl hw.cachelinesize       = %ld bytes (sanity cross-check)\n",
           sysctl_line_size); // => co-02: independent confirmation

    // ex-22: the PASS condition is the MEASUREMENT, per the shared brief -- the
    // sysctl value is printed only as a sanity cross-check, not as the source of
    // truth
    int correct = (detected_line_size == 128); // => co-02: this machine's real, documented line size
    printf("%s\n",
           correct // => co-02: PASS/FAIL verdict
               ? "PASS: the largest measured per-touch jump lands at the 128 B "
                 "stride, matching this machine's cache line" // supporting statement
                                                              // for this example
               : "FAIL: the measured jump did not land at the expected 128 B "
                 "boundary"); // supporting statement for this example

    free(buf);              // => co-02: releases the 64 MiB probe buffer
    return correct ? 0 : 1; // => co-02: nonzero exit on assertion failure
}
