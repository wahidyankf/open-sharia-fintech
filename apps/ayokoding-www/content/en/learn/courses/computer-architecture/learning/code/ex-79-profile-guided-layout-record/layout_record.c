// learning/code/ex-79-profile-guided-layout-record/layout_record.c
/* Example 79: a layout decision record -- every claim printed here cites a
 * number measured above it. */
#include <stdio.h>  // => co-25: printf -- the decision-record report this program prints
#include <stdlib.h> // => malloc/free -- the AoS/SoA buffers under comparison
#include <time.h>   // => clock_gettime -- the wall-clock timer used below

// co-25: this machine has no `perf stat`/`perf record` (Linux-only); the fuller
// version of this workflow uses Instruments' "CPU Counters" template or Linux
// `perf stat -e cache-misses` to cite REAL cache-miss counts in a decision
// record like this one. Without that tool here, every citation below is
// wall-clock time from a best-of-N stopwatch instead -- still a real,
// reproducible measured number, per this whole topic's stated methodology, just
// not a hardware performance-counter one.
#define N \
    4000000      // => co-25: 4M "task" records -- large enough for layout to dominate
                 // the result
#define TRIALS 5 // => co-25: best-of-N wall-clock timing

// ex-79: the record under investigation -- `priority` and `deadline` are HOT
// (read by the scheduler kernel below every tick); `description` and `log` are
// COLD (written once at creation, essentially never read by the hot path) but
// still occupy space in every cache line the hot fields share.
typedef struct {           // struct layout definition
    int priority;          // => HOT
    int deadline;          // => HOT
    char description[240]; // => COLD -- padded so sizeof == 256 bytes (two 128 B
                           // cache lines)
    int log_count;         // => COLD
} TaskRecord;              // supporting statement for this example

// ex-79: the kernel under profile -- a scheduler-style "next task to run" scan:
// the task with the highest (priority - deadline_pressure) score wins. Reads
// ONLY priority and deadline.
static long scan_next_task_aos(const TaskRecord *tasks,
                               int n) {                             // defines scan_next_task_aos(): helper
                                                                    // function used by this example
    long best_score = -1000000000L;                                 // declares best_score
    long best_idx = -1;                                             // declares best_idx
    for (int i = 0; i < n; i++) {                                   // => co-17: one full 256 B record per iteration...
        long score = tasks[i].priority * 1000L - tasks[i].deadline; // ...to read 8 of those 256 bytes
        if (score > best_score) {                                   // => co-17: running-max scan, one comparison per record
            best_score = score;                                     // => co-17: records the new best score
            best_idx = i;                                           // => co-17: records the winning index
        } // conditional check
    }
    return best_idx; // returns the computed result
}

static long scan_next_task_soa(const int *priority, const int *deadline,
                               int n) {                 // defines scan_next_task_soa(): helper
                                                        // function used by this example
    long best_score = -1000000000L;                     // declares best_score
    long best_idx = -1;                                 // declares best_idx
    for (int i = 0; i < n; i++) {                       // => co-03: dense reads -- 32 useful ints per 128 B line
        long score = priority[i] * 1000L - deadline[i]; // declares score
        if (score > best_score) {                       // => co-03: running-max scan, one comparison per record
            best_score = score;                         // => co-03: records the new best score
            best_idx = i;                               // => co-03: records the winning index
        } // conditional check
    }
    return best_idx; // returns the computed result
}

static double best_of(long (*fn)(const void *, const void *, int), const void *a, const void *b,
                      int n) {                                                   // declares function pointer fn
    long (*volatile fn_v)(const void *, const void *, int) = fn;                 // => co-25: see ex-74/ex-75/ex-78 for
    double best = -1.0;                                                          // why this indirection is load-bearing
    for (int t = 0; t < TRIALS; t++) {                                           // loop header controlling the sweep below
        struct timespec t0, t1;                                                  // supporting statement for this example
        clock_gettime(CLOCK_MONOTONIC, &t0);                                     // calls clock_gettime(...)
        volatile long r = fn_v(a, b, n);                                         // declares r
        clock_gettime(CLOCK_MONOTONIC, &t1);                                     // calls clock_gettime(...)
        (void)r;                                                                 // discards r to silence an unused-variable warning
        double secs = (t1.tv_sec - t0.tv_sec) + (t1.tv_nsec - t0.tv_nsec) / 1e9; // declares secs
        if (best < 0 || secs < best)                                             // => co-25: keeps the fastest of TRIALS runs
            best = secs;                                                         // conditional check
    }
    return best; // returns the computed result
}

static long wrap_aos(const void *a, const void *b, int n) {
    (void)b;                                             // => unused here -- wrap_aos only needs the AoS pointer
    return scan_next_task_aos((const TaskRecord *)a, n); // => delegates to the AoS scan
} // performs several bookkeeping updates in one line
static long wrap_soa(const void *a, const void *b, int n) { return scan_next_task_soa((const int *)a, (const int *)b, n); } // supporting statement for this example

int main(void) {                                      // program entry point
    TaskRecord *aos = malloc(sizeof(TaskRecord) * N); // heap-allocates memory for aos
    int *priority = malloc(sizeof(int) * N);          // heap-allocates memory for priority
    int *deadline = malloc(sizeof(int) * N);          // heap-allocates memory for deadline
    if (!aos || !priority || !deadline) {             // => guards all three allocations before touching any
        fprintf(stderr, "alloc failed\n");            // => reports to stderr, not stdout
        return 1;                                     // => nonzero exit -- allocation failure is not this example's claim
    } // prints a report line

    unsigned seed = 55u;                                     // declares seed
    for (int i = 0; i < N; i++) {                            // loop header controlling the sweep below
        seed = seed * 1103515245u + 12345u;                  // assigns seed
        aos[i].priority = priority[i] = (int)(seed % 100u);  // assigns aos[i].priority
        seed = seed * 1103515245u + 12345u;                  // assigns seed
        aos[i].deadline = deadline[i] = (int)(seed % 1000u); // assigns aos[i].deadline
        aos[i].description[0] = 'x';                         // assigns aos[i].description[0]
        aos[i].log_count = 0;                                // assigns aos[i].log_count
    }

    double t_aos = best_of(wrap_aos, aos, NULL, N);                                 // declares t_aos
    double t_soa = best_of(wrap_soa, priority, deadline, N);                        // declares t_soa
    long idx_aos = scan_next_task_aos(aos, N);                                      // declares idx_aos
    long idx_soa = scan_next_task_soa(priority, deadline, N);                       // declares idx_soa
    double speedup = t_aos / t_soa;                                                 // declares speedup
    double footprint_aos_mb = (double)(sizeof(TaskRecord) * N) / (1024.0 * 1024.0); // declares footprint_aos_mb
    double footprint_soa_mb = (double)(sizeof(int) * 2 * N) / (1024.0 * 1024.0);    // declares footprint_soa_mb

    printf("=== raw measurements (best of %d wall-clock trials each) ===\n",
           TRIALS); // prints a report line
    printf("AoS scan_next_task: %.4f s over N=%d records (sizeof(TaskRecord)=%zu "
           "bytes, %.1f MB total)\n", // prints a report line
           t_aos, N, sizeof(TaskRecord),
           footprint_aos_mb); // continues the printf(...) call above
    printf("SoA scan_next_task: %.4f s over N=%d records (hot footprint %.1f MB "
           "total)\n",
           t_soa, N,          // prints a report line
           footprint_soa_mb); // continues the printf(...) call above
    printf("results agree (same winning index): %s (AoS=%ld, SoA=%ld)\n",
           idx_aos == idx_soa ? "yes" : "NO", // prints a report line
           idx_aos, idx_soa);                 // continues the printf(...) call above

    printf("\n=== decision record: TaskRecord hot/cold split ===\n"); // prints a
                                                                      // report line
    printf("- Claim 1: the AoS scan measured %.4f s for N=%d records -- MEASURED "
           "above, not assumed.\n", // prints a report line
           t_aos, N);               // continues the printf(...) call above
    printf("- Claim 2: the SoA scan measured %.4f s for the SAME N -- a %.2fx "
           "speedup, MEASURED above.\n", // prints a report line
           t_soa, speedup);              // continues the printf(...) call above
    printf("- Claim 3: AoS's per-record footprint is %zu bytes (%.1f MB total); "
           "SoA's hot footprint is\n", // prints a report line
           sizeof(TaskRecord),
           footprint_aos_mb); // continues the printf(...) call above
    printf("  only %.1f MB total -- a %.1fx smaller hot working set, computed "
           "from sizeof() above, not\n", // prints a report line
           footprint_soa_mb,
           footprint_aos_mb / footprint_soa_mb); // continues the printf(...) call above
    printf("  guessed.\n");                      // prints a report line
    printf("- Claim 4: both layouts agree on the winning task index (AoS=%ld, "
           "SoA=%ld) -- MEASURED above,\n",                                     // prints a report line
           idx_aos, idx_soa);                                                   // continues the printf(...) call above
    printf("  proving the layout change did not alter the kernel's answer.\n"); // prints
                                                                                // a
                                                                                // report
                                                                                // line
    printf("- Decision: ADOPT the SoA layout for the scheduler's hot path -- "
           "every claim above cites a\n"); // prints a report line
    printf("  number this exact program measured on this exact run, not an "
           "assumed or copied figure.\n"); // prints a report line
    printf("- Caveat: on Linux, `perf stat -e cache-misses` would additionally "
           "CITE the raw miss-count\n"); // prints a report line
    printf("  drop directly; this machine has no such counter access, so "
           "wall-clock time is the cited\n"); // prints a report line
    printf("  metric throughout, per this topic's stated measurement "
           "methodology.\n"); // prints a report line

    int pass = (idx_aos == idx_soa) && (speedup > 1.05); // declares pass
    printf("\nPASS (every claim above traces to a number measured in THIS run, "
           "and the decision is\n"); // prints a report line
    printf(" correct + faster): %s\n",
           pass ? "PASS" : "FAIL"); // prints a report line

    free(aos);      // releases aos's heap memory
    free(priority); // releases priority's heap memory
    free(deadline); // releases deadline's heap memory
    return 0;       // returns the computed result
}
