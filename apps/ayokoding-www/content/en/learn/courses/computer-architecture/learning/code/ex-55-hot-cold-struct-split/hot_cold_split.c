// learning/code/ex-55-hot-cold-struct-split/hot_cold_split.c
/* Example 55: split a rarely-used cold field out of a hot struct -- verify
   a hot-loop speedup, amplified across REPEATED passes (co-17, co-04). */
#include <stdio.h>  // => printf -- the timing/PASS report this program prints
#include <stdlib.h> // => malloc/free -- both record layouts under test are heap-allocated
#include <string.h> // => memset -- fills the cold bytes with realistic non-zero payload
#include <time.h>   // => clock_gettime -- the portable wall-clock timer used below

#define N \
    500000 // => co-04: 500K records -- chosen so the SPLIT hot array (2 MB) fits
           //    comfortably in this machine's 4 MiB L2, while the COMBINED array
           //    (128 MB) does not -- co-04's temporal-locality payoff needs
           //    REPEATS
#define REPEATS \
    50           // => co-04: revisit the hot field this many times -- a compact working
                 //    set stays cache-resident across every pass; a bloated one does not
#define TRIALS 3 // => co-25: best-of-3 -- shared-machine noise smoothing

// co-17: the record as it "naturally" arrives -- one hot `score` field the loop
// below actually needs, wrapped in 252 cold bytes (a name buffer + metadata)
// that this loop never touches, making sizeof(Combined) == 256 B (two 128 B
// cache lines).
typedef struct {    // struct layout definition
    int score;      // => co-17: the ONE field this hot loop reads
    char cold[252]; // => co-17: cold payload -- never read by sum_hot
} Combined;         // supporting statement for this example

static double now_seconds(void) {                        // => co-25: shared wall-clock helper, this topic's standard pattern
    struct timespec ts;                                  // supporting statement for this example
    clock_gettime(CLOCK_MONOTONIC, &ts);                 // calls clock_gettime(...)
    return (double)ts.tv_sec + (double)ts.tv_nsec / 1e9; // returns the computed result
}

// co-17/co-04: repeatedly sums the hot field over N records, REPEATS times --
// each pass revisits the SAME memory, so whether that memory fits in cache
// (co-04) governs whether pass 2..REPEATS are fast (cache-resident) or pay the
// SAME miss cost as pass 1.
__attribute__((noinline)) static long sum_combined(const Combined *records, int n,
                                                   int repeats, // calls __attribute__(...)
                                                   int salt) {  // supporting statement for this example
    long total = salt;                                          // => co-25: salt distinguishes each trial's call (see ex-47/48)
    for (int r = 0; r < repeats; r++) {                         // loop header controlling the sweep below
        for (int i = 0; i < n; i++)
            total += records[i].score; // => co-17: pulls in a full 256 B record's
    } //    worth of cache lines for 4 B of real data
    return total; // returns the computed result
}

__attribute__((noinline)) static long sum_split(const int *hot, int n, int repeats,
                                                int salt) { // calls __attribute__(...)
    long total = salt;                                      // declares total
    for (int r = 0; r < repeats; r++) {                     // loop header controlling the sweep below
        for (int i = 0; i < n; i++)
            total += hot[i]; // => co-17: every fetched cache line is 100% hot data
    }
    return total; // returns the computed result
}

int main(void) {                                               // program entry point
    Combined *combined = malloc((size_t)N * sizeof(Combined)); // => co-17: 128 MB -- far bigger than L2
    int *hot = malloc((size_t)N * sizeof(int));                // => co-17: 2 MB -- comfortably L2-resident
    if (!combined || !hot) {
        fprintf(stderr, "alloc failed\n");
        return 1;
    } // prints a report line
    for (int i = 0; i < N; i++) {      // loop header controlling the sweep below
        int value = (i * 7919) % 1009; // => deterministic filler value
        combined[i].score = value;     // assigns combined[i].score
        memset(combined[i].cold, 'x',
               sizeof(combined[i].cold)); // => realistic non-zero cold payload
        hot[i] = value;                   // => co-17: SAME logical values, split layout
    }

    double best_combined = 1e18, best_split = 1e18;        // declares best_combined
    long sum_c = 0, sum_s = 0;                             // declares sum_c
    for (int t = 0; t < TRIALS; t++) {                     // => co-25: best-of-N -- keep the fastest clean run
        double t0 = now_seconds();                         // declares t0
        sum_c = sum_combined(combined, N, REPEATS, t) - t; // assigns sum_c
        double t1 = now_seconds();                         // declares t1
        if (t1 - t0 < best_combined)
            best_combined = t1 - t0; // conditional check

        double t2 = now_seconds();                 // declares t2
        sum_s = sum_split(hot, N, REPEATS, t) - t; // assigns sum_s
        double t3 = now_seconds();                 // declares t3
        if (t3 - t2 < best_split)
            best_split = t3 - t2; // conditional check
    }

    printf("N=%d, REPEATS=%d, sizeof(Combined)=%zu B (%.1f MB total), split hot "
           "array=%.1f MB\n",
           N, // prints a report line
           REPEATS, sizeof(Combined),
           (double)(sizeof(Combined) * N) / (1024.0 * 1024.0),                                              // continues the printf(...) call above
           (double)(sizeof(int) * N) / (1024.0 * 1024.0));                                                  // continues the printf(...) call above
    printf("combined (hot+cold interleaved): sum=%ld, best of %d: %.4f s\n", sum_c, TRIALS, best_combined); // prints a report line
    printf("split (hot field only):          sum=%ld, best of %d: %.4f s\n", sum_s, TRIALS, best_split);    // prints a report line
    double speedup = best_combined / best_split;                                                            // declares speedup
    printf("split is %.2fx faster -> %s\n", speedup,                                                        // prints a report line
           (sum_c == sum_s && speedup > 1.3) ? "PASS (identical sums, split measurably faster)" : "FAIL");  // continues the printf(...) call above
    free(combined);                                                                                         // releases combined's heap memory
    free(hot);                                                                                              // releases hot's heap memory
    return (sum_c == sum_s && speedup > 1.3) ? 0 : 1;                                                       // returns the computed result
}
