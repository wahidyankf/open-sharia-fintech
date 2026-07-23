// learning/code/ex-28-cache-miss-stride-sweep/stride_sweep.c
// Example 28: sweep access stride 1..1024 elements and find the cache-line-size
// performance cliff on this machine (co-02, co-05).
#include <stdio.h>  // => co-25: printf -- reports the ns/access table and PASS/FAIL verdict
#include <stdlib.h> // => co-01: malloc/free -- the 256 MiB buffer under test
#include <time.h>   // => co-25: clock_gettime -- the wall-clock timer used below

#define BUF_MB 256UL // => co-05: 256 MiB buffer, far larger than any cache on this machine
#define ACCESSES \
    8000000L // => co-05: fixed access count per stride -- same work, only stride
             // varies

static double now_seconds(void) { // => co-25: wall-clock via clock_gettime, portable timer
    struct timespec ts;           // => co-25: POSIX timespec -- seconds + nanoseconds
    clock_gettime(CLOCK_MONOTONIC,
                  &ts);                                  // => co-25: monotonic clock -- immune to wall-clock adjustment
    return (double)ts.tv_sec + (double)ts.tv_nsec / 1e9; // => co-25: combine into one double-seconds value
}

int main(void) {
    // => co-02: the hypothesis under test -- consecutive small-stride accesses
    // => share a 128 B cache line and pay for only ONE miss among many touches,
    // => while a stride >= one line's worth of ints pays a fresh miss every time
    size_t n_ints = (BUF_MB * 1024UL * 1024UL) / sizeof(int); // => co-01: element count, a power of two by construction
    // => co-01: 256 MiB is far past this machine's 4 MiB L2, so a small stride's
    // => "fast" case below is genuinely spatial-locality inside one cache line,
    // => not the whole buffer secretly fitting in cache
    int *buf = malloc(n_ints * sizeof(int)); // => co-01: one big flat array -- the memory under test
    if (buf == NULL) {                       // => co-25: guard the 256 MiB allocation before touching it
        fprintf(stderr, "alloc failed\n");   // => co-25: reports to stderr, not stdout
        return 1;                            // => co-25: nonzero exit -- allocation failure is not this example's claim
    } // => co-25: fail loudly rather than measure garbage
    for (size_t i = 0; i < n_ints; i++) // => co-01: one pass over every element, ascending
        buf[i] = (int)i;                // => co-01: touch every page once so faults don't skew timing

    size_t mask = n_ints - 1;                                              // => co-02: n_ints is a power of two -- mask replaces slow modulo
    int strides[] = {1, 2, 4, 8, 16, 24, 32, 48, 64, 128, 256, 512, 1024}; // => co-02: elements per step,
                                                                           // sweeping past 32 (=128B/4B)
    int n_strides = (int)(sizeof(strides) / sizeof(strides[0]));           // => co-02: array length, computed
                                                                           // rather than hardcoded

    printf("cache line size on this machine: %d bytes (%d ints)\n", 128,
           128 / (int)sizeof(int)); // => co-02: known via sysctl
    printf("%8s %12s %10s\n", "stride", "ns/access",
           "elems/line"); // => co-25: column header for the table printed below

    double baseline_ns = 0.0;                        // => co-05: ns/access at the smallest stride -- the "all hits" floor
    double cliff_ns = 0.0;                           // => co-05: ns/access once stride exceeds the cache-line size
    for (int s = 0; s < n_strides; s++) {            // => co-02: one timed pass per candidate stride
        volatile long sum = 0;                       // => co-25: volatile sink -- forces the load to really happen
        size_t idx = 0;                              // => co-02: running index, wrapped with the power-of-two mask
        double t0 = now_seconds();                   // => co-25: start the clock for this stride's run
        for (long i = 0; i < ACCESSES; i++) {        // => co-05: fixed number of accesses, identical across strides
            idx = (idx + (size_t)strides[s]) & mask; // => co-02: advance by `stride` elements, wrap via mask
            sum += buf[idx];                         // => co-05: the actual memory access under measurement
        }
        double t1 = now_seconds();                                 // => co-25: stop the clock
        double ns_per_access = (t1 - t0) * 1e9 / (double)ACCESSES; // => co-25: normalize to a per-access cost
        printf("%8d %12.2f %10.1f\n", strides[s],
               ns_per_access,                               // => co-25: print this stride's real measured cost
               128.0 / (strides[s] * (double)sizeof(int))); // => co-02: how many strides fit in one 128 B line
        if (strides[s] == 1)
            baseline_ns = ns_per_access; // => co-05: smallest stride -- best-case,
                                         // all same-line hits
        if (strides[s] == 32)
            cliff_ns = ns_per_access; // => co-02: exactly one cache line (128B/4B) per step
        (void)sum;                    // => co-25: sum only exists to defeat dead-code elimination
    }

    double ratio = cliff_ns / baseline_ns; // => co-05: how much slower the one-miss-per-access case is
    printf("\nstride=1 baseline: %.2f ns/access\n",
           baseline_ns); // => co-25: restate the floor for the reader
    printf("stride=32 (one cache line/access): %.2f ns/access\n",
           cliff_ns); // => co-05: restate the cliff for the reader
    printf("cliff ratio: %.2fx -> %s\n",
           ratio,                                                                                  // => co-25: the program judges its OWN claim, not the reader
           ratio > 1.5 ? "PASS (clear cliff at the cache-line stride)" : "FAIL (no clear cliff)"); // => co-05: the assertion
    free(buf);                                                                                     // => co-01: release the 256 MiB buffer before exiting
    return ratio > 1.5 ? 0 : 1;                                                                    // => co-25: a real process exit code reflecting the PASS/FAIL
}
