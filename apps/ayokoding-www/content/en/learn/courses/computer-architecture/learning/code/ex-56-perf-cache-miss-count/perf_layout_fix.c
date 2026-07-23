// learning/code/ex-56-perf-cache-miss-count/perf_layout_fix.c
/* Example 56: measure the effect of a layout fix "before" and "after" --
   verify the cost drops (co-25, co-05). PLATFORM NOTE (mandatory): the
   real tool for this on Linux is `perf stat -e cache-misses ./binary`; on
   macOS (this machine) the equivalent is Instruments' "CPU Counters"
   template, or `sudo dtrace` with the right PMC provider -- neither is
   scriptable headlessly in this shell/sandbox. This example measures the
   REAL, established wall-clock proxy this whole topic uses instead
   (see ex-58 in the advanced tier for the same honest methodology): the
   layout fix's effect on wall-clock time is a direct, legitimate
   consequence of its effect on cache-miss traffic, even without a raw
   hardware counter reading. */
#include <stdio.h>  // => printf -- the "before/after profile" report this program prints
#include <stdlib.h> // => malloc/free -- both layouts under test are heap-allocated
#include <time.h>   // => clock_gettime -- the portable wall-clock timer used below

// co-25: VERIFIED CAVEAT (found while building this example, via a scratch
// sweep -- see the delivery.md notes for this ex-NN): a SMALL 48 B record (only
// x,y,z hot + vx,vy,vz cold) gave a barely-measurable effect (1.0x-1.1x) even
// at huge sizes -- this machine's streaming prefetcher hides most of a
// SEQUENTIAL small-stride bandwidth waste (the same real hardware behavior
// already found in ex-35's prefetch and ex-45's write-cost examples). A
// REALISTIC 128 B simulation record (one full cache line: position + velocity +
// mass + id + color + flags, matching co-17's stated packed-struct shape) gives
// a real, stable, reproducible signal instead -- AND REPEATS (co-04's
// temporal-locality technique, same fix ex-55 uses) makes it stable run-to-run:
// a compact SoA working set that fits in L2 stays fast on every repeated pass,
// while a bloated AoS one pays the same per-line waste every time.
#define N \
    300000          // => co-05: 300K points -- SoA x[] (2.3 MB) comfortably fits this
                    // machine's
                    //    4 MiB L2; AoS (36.6 MB) is far bigger than any on-chip cache
#define REPEATS 150 // => co-04: revisit the data this many times -- amplifies the signal
#define TRIALS 3    // => co-25: best-of-3 -- shared-machine noise smoothing

// co-17: a "particle" record -- 3 hot doubles (x,y,z) this kernel needs, PLUS a
// realistic cold payload (velocity, mass, id, color, flags) padded to exactly
// one 128 B cache line -- so fetching ONE cache line to read 8 B of x wastes
// 15/16 of it.
typedef struct {       // struct layout definition
    double x, y, z;    // => co-17: HOT -- what this kernel sums
    double vx, vy, vz; // => co-17: COLD -- never read here
    double mass;       // => co-17: COLD -- simulation payload
    long id;           // => co-17: COLD -- simulation payload
    char color[4];     // => co-17: COLD -- render payload
    char flags;        // => co-17: COLD -- state payload
    char pad[59];      // => co-17: rounds sizeof(Point) up to
} Point;               //    exactly 128 B -- one cache line

static double now_seconds(void) {                        // => co-25: shared wall-clock helper, this topic's standard pattern
    struct timespec ts;                                  // supporting statement for this example
    clock_gettime(CLOCK_MONOTONIC, &ts);                 // calls clock_gettime(...)
    return (double)ts.tv_sec + (double)ts.tv_nsec / 1e9; // returns the computed result
}

// co-25: "PROFILE" step -- the kernel AS GIVEN, walking the full 48 B AoS
// record to read 8 of those 48 bytes (x) per point, REPEATS times over the SAME
// memory (co-04: this is what turns a one-shot bandwidth measurement into a
// stable cache-residency signal).
__attribute__((noinline)) static double sum_x_aos(const Point *pts, int n, int repeats,
                                                  double salt) { // calls __attribute__(...)
    double total = salt;                                         // declares total
    for (int r = 0; r < repeats; r++) {                          // loop header controlling the sweep below
        for (int i = 0; i < n; i++)
            total += pts[i].x; // => co-17: pulls in a full 128 B Point cache line
    } //    per iteration -- 36.6 MB AoS never fits this
    return total; //    machine's 4 MiB L2, so EVERY repeated pass
} //    repays the same miss cost

// co-25: "FIX" step -- same computation, over a dense x[] array holding ONLY
// the field this kernel reads, REPEATS times over the SAME memory.
__attribute__((noinline)) static double sum_x_soa(const double *x, int n, int repeats,
                                                  double salt) { // calls __attribute__(...)
    double total = salt;                                         // declares total
    for (int r = 0; r < repeats; r++) {                          // loop header controlling the sweep below
        for (int i = 0; i < n; i++)
            total += x[i]; // => co-17: 2.3 MB SoA fits comfortably inside this
    } //    machine's 4 MiB L2 -- later passes stay
    return total; //    fully cache-resident
}

int main(void) {                                    // program entry point
    Point *pts = malloc((size_t)N * sizeof(Point)); // => co-17: 128 B * 300K ~= 36.6 MB -- far bigger than L2
    double *x = malloc((size_t)N * sizeof(double)); // => co-17: 8 B * 300K ~= 2.3 MB -- 16x smaller footprint
    if (!pts || !x) {
        fprintf(stderr, "alloc failed\n");
        return 1;
    } // prints a report line
    for (int i = 0; i < N; i++) {           // loop header controlling the sweep below
        double v = (double)(i % 997) * 0.5; // declares v
        pts[i].x = v;
        pts[i].y = v;
        pts[i].z = v; // assigns pts[i].x
        pts[i].vx = 0.1;
        pts[i].vy = 0.2;
        pts[i].vz = 0.3; // => cold, never-read velocity payload
        pts[i].mass = 1.0;
        pts[i].id = i; // => cold, never-read simulation payload
        pts[i].color[0] = 'r';
        pts[i].flags = 0; // => cold, never-read render/state payload
        x[i] = v;         // assigns x[i]
    }

    double best_before = 1e18, best_after = 1e18;                       // declares best_before
    double sum_before = 0, sum_after = 0;                               // declares sum_before
    for (int t = 0; t < TRIALS; t++) {                                  // => co-25: best-of-N -- keep the fastest clean run
        double t0 = now_seconds();                                      // declares t0
        sum_before = sum_x_aos(pts, N, REPEATS, (double)t) - (double)t; // => co-25: the "profile" (before) measurement
        double t1 = now_seconds();                                      // declares t1
        if (t1 - t0 < best_before)
            best_before = t1 - t0; // conditional check

        double t2 = now_seconds();                                   // declares t2
        sum_after = sum_x_soa(x, N, REPEATS, (double)t) - (double)t; // => co-25: the "re-profile" (after) measurement
        double t3 = now_seconds();                                   // declares t3
        if (t3 - t2 < best_after)
            best_after = t3 - t2; // conditional check
    }

    printf("N=%d points, REPEATS=%d, sizeof(Point)=%zu B (%.0f MB AoS), SoA x[] "
           "= %.0f MB\n",
           N, REPEATS, // prints a report line
           sizeof(Point),
           (double)(sizeof(Point) * N) / (1024.0 * 1024.0),                                                   // continues the printf(...) call above
           (double)(sizeof(double) * N) / (1024.0 * 1024.0));                                                 // continues the printf(...) call above
    printf("BEFORE (AoS, profiled layout): sum=%.2f, best of %d: %.4f s\n", sum_before, TRIALS, best_before); // prints a report line
    printf("AFTER  (SoA, fixed layout):    sum=%.2f, best of %d: %.4f s\n", sum_after, TRIALS, best_after);   // prints a report line
    double speedup = best_before / best_after;                                                                // declares speedup
    double abs_diff = sum_before - sum_after;                                                                 // declares abs_diff
    if (abs_diff < 0)
        abs_diff = -abs_diff; // conditional check
    printf("speedup: %.2fx, |sum diff|=%.6f -> %s\n", speedup,
           abs_diff,                                                             // prints a report line
           (abs_diff < 1e-3 && speedup > 1.3)                                    // continues the printf(...) call above
               ? "PASS (identical result, layout fix measurably drops the cost)" // continues the printf(...) call above
               : "FAIL");                                                        // continues the printf(...) call above
    free(pts);                                                                   // releases pts's heap memory
    free(x);                                                                     // releases x's heap memory
    return (abs_diff < 1e-3 && speedup > 1.3) ? 0 : 1;                           // returns the computed result
}
