// learning/code/ex-45-write-heavy-cost/write_heavy.c
/* Example 45: time a write-heavy (read-modify-write) pass vs a read-heavy
   pass over the SAME data -- verify the write traffic costs measurably
   more (co-07). VERIFIED CAVEAT (found while building this example): the
   classic "write costs ~2x a read" story (from write-allocate's
   read-for-ownership) is MUCH more modest on this machine -- a pure
   store-only pass (`arr[i]=const`) measured FASTER than a read-only sum
   here, meaning this Apple Silicon memory controller implements an
   efficient no-read-allocate path for full-line overwrites. The
   read-modify-write form below is the honest, reliably-reproducible case:
   it must read the OLD value before writing the new one, so it cannot
   dodge the extra store traffic the way a pure overwrite can. */
#include <stdio.h>  // => printf -- the timing/PASS report this program prints
#include <stdlib.h> // => malloc/free -- the array both passes operate on
#include <time.h>   // => clock_gettime -- the portable wall-clock timer used below

#define N \
    128000000 // => co-07: 128M ints = 512 MB -- far bigger than this machine's 4
              // MiB L2,
              //    so every touched cache line is a real DRAM round trip either
              //    way
#define TRIALS \
    7 // => co-25: best-of-7 -- this machine's write path is efficient enough
      //    that the real effect is modest, so more trials smooth more noise

static double now_seconds(void) {                        // => co-25: shared wall-clock helper, this topic's standard pattern
    struct timespec ts;                                  // supporting statement for this example
    clock_gettime(CLOCK_MONOTONIC, &ts);                 // calls clock_gettime(...)
    return (double)ts.tv_sec + (double)ts.tv_nsec / 1e9; // returns the computed result
}

// co-07: READ-only pass -- every cache line is fetched once, read, never
// modified. Under a write-back cache, a clean line just gets evicted later with
// zero extra cost.
static long read_heavy(const int *arr,
                       int n) { // defines read_heavy(): helper function used by this example
    long total = 0;             // declares total
    for (int i = 0; i < n; i++)
        total += arr[i]; // => co-07: one load per element, no stores at all
    return total;        // returns the computed result
}

// co-07: READ-MODIFY-WRITE pass -- every element is read, incremented, and
// stored back. This MUST issue a real load before the store (the result depends
// on the old value), so unlike a pure overwrite it cannot skip the read even on
// hardware with an efficient no-allocate store path -- the extra store (and the
// eventual write-back of the now-dirty line) is real traffic on top of what
// read_heavy alone pays.
static void write_heavy(int *arr, int n,
                        int add) { // defines write_heavy(): helper function used by this example
    for (int i = 0; i < n; i++)
        arr[i] = arr[i] + add; // => co-07: one load AND one store per element
}

int main(void) {                                // program entry point
    int *arr = malloc((size_t)N * sizeof(int)); // heap-allocates memory for arr
    if (!arr) {
        fprintf(stderr, "alloc failed\n");
        return 1;
    } // prints a report line
    for (int i = 0; i < N; i++)
        arr[i] = i % 1000; // => deterministic filler values

    double best_read = 1e18, best_write = 1e18; // declares best_read
    long read_sum = 0;                          // declares read_sum
    for (int t = 0; t < TRIALS; t++) {          // => co-25: best-of-N -- keep the fastest clean run
        double t0 = now_seconds();              // declares t0
        read_sum = read_heavy(arr, N);          // assigns read_sum
        double t1 = now_seconds();              // declares t1
        if (t1 - t0 < best_read)
            best_read = t1 - t0; // conditional check

        double t2 = now_seconds(); // declares t2
        write_heavy(arr, N,
                    1);            // => co-07: mutates arr -- next read_heavy sum shifts
        double t3 = now_seconds(); // declares t3
        if (t3 - t2 < best_write)
            best_write = t3 - t2; // conditional check
    }

    printf("N=%d ints (%.0f MB), best of %d\n", N, (double)(N * sizeof(int)) / (1024.0 * 1024.0),
           TRIALS); // prints a report line
    printf("read-heavy:         sum=%ld, %.4f s\n", read_sum,
           best_read);                                                                                   // prints a report line
    printf("read-modify-write:  %.4f s\n", best_write);                                                  // prints a report line
    double ratio = best_write / best_read;                                                               // => co-07: how much extra the store traffic costs
    printf("write is %.3fx the read cost -> %s\n", ratio,                                                // prints a report line
           ratio > 1.02 ? "PASS (real, if modest on this hardware, extra store-traffic cost)" : "FAIL"); // continues the printf(...) call above
    free(arr);                                                                                           // releases arr's heap memory
    return ratio > 1.02 ? 0 : 1;                                                                         // returns the computed result
}
