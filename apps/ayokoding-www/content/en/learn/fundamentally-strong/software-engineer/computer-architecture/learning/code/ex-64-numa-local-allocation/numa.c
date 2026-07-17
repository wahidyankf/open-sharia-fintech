// learning/code/ex-64-numa-local-allocation/numa.c
/* Example 64: NUMA-local vs NUMA-remote first-touch allocation -- an honest
 * UMA-machine test. */
#include <pthread.h> // => co-01: a second thread stands in for "the remote node's CPU" in this test
#include <stdio.h>   // stdio.h: standard library header
#include <stdlib.h>  // stdlib.h: standard library header
#include <time.h>    // time.h: standard library header

// co-01: 128M ints = 512 MB -- far bigger than this machine's 4 MiB L2, so
// every read below is a real DRAM round trip, not a cache hit. That is
// deliberate: NUMA latency differences only show up once you are actually
// leaving cache and hitting a memory controller.
#define N (128L * 1024 * 1024) // constant N = (128L * 1024 * 1024)
#define TRIALS \
    5 // => co-25: best-of-N wall-clock methodology, same rule this whole topic
      // uses

// ex-64: on real NUMA hardware (multi-socket Xeon/EPYC servers, `numactl
// --membind=0
// --cpunodebind=0 ./prog`), the OS's default "first-touch" policy binds each
// virtual page to whichever NUMA node's CPU first WRITES to it (not the CPU
// that allocates it with malloc -- malloc alone only reserves virtual address
// space). If a thread pinned to node 0 touches a page, that page's physical
// frame lives in node 0's local DRAM; a thread on node 1 reading it later pays
// an extra cross-socket interconnect hop -- typically 1.3x-1.8x the local
// latency in published NUMA benchmarks. `numactl --cpunodebind=N --membind=N`
// is how you force both the compute AND the allocation onto the same node to
// get the fast, local path.
static void touch_local(int *buf,
                        long n) { // defines touch_local(): helper function used by this example
    for (long i = 0; i < n; i++)
        buf[i] = (int)(i & 0xff); // => co-01: first-touch -- allocates the physical page
}

// ex-64: this thread stands in for "the other NUMA node's CPU" doing the
// first-touch -- on real NUMA hardware, running this on a thread pinned to node
// 1 would bind buf_remote's physical pages to node 1's local DRAM, making every
// later read from node 0 a remote (slow) access.
static void *touch_thread(void *arg) { // defines touch_thread(): helper function used by this example
    touch_local((int *)arg, N);        // calls touch_local(...)
    return NULL;                       // returns the computed result
}

// co-01: the actual latency measurement -- a plain sequential read-sum over the
// whole buffer, repeated TRIALS times, reporting the fastest run (removes
// scheduler/OS noise, not the physical memory-controller cost this example is
// trying to isolate).
static double time_read(const int *buf,
                        long n) {            // defines time_read(): helper function used by this example
    double best = -1.0;                      // declares best
    for (int t = 0; t < TRIALS; t++) {       // loop header controlling the sweep below
        struct timespec t0, t1;              // supporting statement for this example
        volatile long sum = 0;               // => volatile: stop the optimizer from deleting the "unused" read
        clock_gettime(CLOCK_MONOTONIC, &t0); // calls clock_gettime(...)
        for (long i = 0; i < n; i++)
            sum += buf[i];                                                       // loop header controlling the sweep below
        clock_gettime(CLOCK_MONOTONIC, &t1);                                     // calls clock_gettime(...)
        (void)sum;                                                               // discards sum to silence an unused-variable warning
        double secs = (t1.tv_sec - t0.tv_sec) + (t1.tv_nsec - t0.tv_nsec) / 1e9; // declares secs
        if (best < 0 || secs < best)
            best = secs; // conditional check
    }
    return best; // returns the computed result
}

int main(void) { // program entry point
    // ex-64: "local" buffer -- first-touched by THIS thread (the one that will
    // also read it back), the exact allocation pattern `numactl --cpunodebind=N
    // --membind=N` forces on real NUMA hardware.
    int *buf_local = malloc(sizeof(int) * N); // heap-allocates memory for buf_local
    // ex-64: "remote" buffer -- first-touched by a DIFFERENT thread, standing in
    // for a first-touch on another NUMA node's CPU. On this machine there IS no
    // other node, so this is the honest, direct test of whether that distinction
    // matters here at all.
    int *buf_remote = malloc(sizeof(int) * N); // heap-allocates memory for buf_remote
    if (!buf_local || !buf_remote) {
        fprintf(stderr, "alloc failed\n");
        return 1;
    } // prints a report line

    touch_local(buf_local, N); // => co-01: first touch happens on the main thread

    pthread_t th; // declares th
    pthread_create(&th, NULL, touch_thread,
                   buf_remote); // => co-01: first touch happens on a second thread
    pthread_join(th, NULL);     // calls pthread_join(...)

    // co-01: both buffers are now fully paged in; read BOTH from the main thread
    // so any latency gap measured here can only come from which thread
    // first-touched the pages, not from who is reading.
    double t_local = time_read(buf_local, N);   // declares t_local
    double t_remote = time_read(buf_remote, N); // declares t_remote
    double ratio = t_remote / t_local;          // declares ratio

    printf("N=%ld ints (%.1f MB per buffer) -- this machine has NO discrete NUMA "
           "node (single-package\n",
           N,                                              // prints a report line
           (double)(sizeof(int) * N) / (1024.0 * 1024.0)); // continues the printf(...) call above
    printf("Apple Silicon UMA, no `numactl` here) -- this is the direct, honest "
           "test of that fact\n");                                                                // prints a report line
    printf("local  (first-touched by reading thread): best of %d = %.4f s\n", TRIALS, t_local);   // prints a report line
    printf("remote (first-touched by OTHER thread):    best of %d = %.4f s\n", TRIALS, t_remote); // prints a report line
    printf("remote/local ratio: %.3fx\n", ratio);                                                 // prints a report line
    // co-01: on real NUMA hardware this ratio would reliably exceed ~1.3x; here
    // we expect it to sit close to 1.0 within ordinary run-to-run noise, because
    // there is only one memory controller.
    int pass = (ratio > 0.85 && ratio < 1.15); // declares pass
    printf("PASS (no significant local/remote gap, consistent with "
           "single-package UMA -- no NUMA nodes\n"); // prints a report line
    printf(" to be local or remote TO -- on real multi-socket NUMA hardware this "
           "ratio would instead\n"); // prints a report line
    printf(" exceed ~1.3x): %s\n",
           pass ? "PASS" : "FAIL (unexpected gap on UMA hardware -- investigate)"); // prints a
                                                                                    // report
                                                                                    // line

    free(buf_local);  // releases buf_local's heap memory
    free(buf_remote); // releases buf_remote's heap memory
    return 0;         // returns the computed result
}
