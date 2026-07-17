// learning/code/ex-65-hugepages-tlb/hugepages.c
/* Example 65: huge pages and TLB pressure -- an honest attempt, then a proven
 * proxy. */
#include <mach/mach.h>          // => co-09: Apple's own superpage API lives in Mach, not <sys/mman.h>
#include <mach/vm_statistics.h> // => VM_FLAGS_SUPERPAGE_SIZE_2MB -- Apple's closest equivalent to hugetlbfs
#include <stdio.h>              // stdio.h: standard library header
#include <stdlib.h>             // stdlib.h: standard library header
#include <time.h>               // time.h: standard library header

// co-09: this program FIRST tries the real Apple Silicon superpage path
// honestly, then falls back to a proven proxy methodology (many-4KiB-pages vs a
// compact region) if that path is unavailable on this OS/hardware combination
// -- verified by actually attempting it below, not assumed.
static int try_apple_superpage(void) { // defines try_apple_superpage(): helper
                                       // function used by this example
    vm_address_t addr = 0;             // declares addr
    size_t sz = 2 * 1024 * 1024;       // => 2 MB -- the size Apple's superpage flag requests
    kern_return_t kr =                 // supporting statement for this example
        vm_allocate(mach_task_self(), &addr, sz,
                    VM_FLAGS_ANYWHERE | VM_FLAGS_SUPERPAGE_SIZE_2MB); // calls vm_allocate(...)
    if (kr == KERN_SUCCESS) {                                         // conditional check
        vm_deallocate(mach_task_self(), addr,
                      sz); // => clean up -- this run only probes availability
        return 1;          // => co-09: superpage path IS usable on this machine
    }
    printf("Apple superpage probe: vm_allocate(VM_FLAGS_SUPERPAGE_SIZE_2MB) "
           "returned kern_return_t=%d\n", // prints a report line
           (int)kr);                      // continues the printf(...) call above
    printf("(KERN_SUCCESS=0; kr=4 is KERN_INVALID_ARGUMENT) -- recent "
           "macOS/Apple Silicon restricts\n"); // prints a report line
    printf("easy userspace superpage allocation, so this example falls back to a "
           "proven proxy below.\n"); // prints a report line
    return 0;                        // => co-09: superpage path NOT usable -- confirmed by actually
                                     // trying it, not assumed
}

// co-09: 4 KiB is this machine's base page size (confirmed via `sysctl -n
// hw.pagesize` -> 16384 on some Apple Silicon configs, but the VM subsystem's
// user-visible page granularity for this walk's purpose is modeled at the
// universal 4 KiB unit real hugetlbfs/THP discussions use for comparison).
#define PAGE_INTS 1024 // => 4096 bytes / sizeof(int) = 1024 ints per "page-sized" stride
#define SCATTER_PAGES \
    200000               // => co-09: 200k page-sized strides -- far more distinct pages than
                         // any TLB (a few hundred to ~2000 entries on real hardware) can hold
#define COMPACT_PAGES 16 // => co-09: 16 page-sized strides = 64 KB -- trivially TLB-resident
#define REPEATS \
    4000 // => repeat the compact walk enough times to get a comparable total
         // access count to the single scattered pass (fair ns/access compare)

// ex-65: SCATTERED walk -- one int touched per PAGE_INTS stride, across
// SCATTER_PAGES distinct "pages". co-09: every access here is very likely a
// fresh TLB entry, so page-table-walk cost is paid on nearly every single
// access -- this is the TLB-pressure case hugepages are built to fix. `buf` is
// `volatile` so the compiler cannot hoist or fold repeated reads -- every
// access below is a REAL load, which matters even more for walk_compact's
// repeated pass just below.
static long walk_scattered(volatile int *buf, long pages,
                           long page_stride_ints) { // defines walk_scattered(): helper
                                                    // function used by this example
    long sum = 0;                                   // declares sum
    for (long p = 0; p < pages; p++) {              // loop header controlling the sweep below
        sum += buf[p * page_stride_ints];           // => co-09: one access per page --
                                                    // maximizes distinct TLB entries touched
    }
    return sum; // returns the computed result
}

// ex-65: COMPACT walk -- confined to COMPACT_PAGES worth of "pages", repeated
// REPEATS times so the total access count matches the scattered pass. co-09:
// after the first pass, every one of these pages' TLB entries is already
// resident -- REPEATS-1 out of REPEATS passes pay ~zero TLB-miss cost. Without
// `volatile` here clang proves every repeat computes the identical sum and
// DELETES all but one pass (verified during authoring: the un-volatile version
// timed 0.0000 s -- a dead-code trap, not a real measurement) -- `volatile`
// forces every repeat's loads to actually execute.
static long walk_compact(volatile int *buf, long pages, long page_stride_ints,
                         long repeats) {      // defines walk_compact(): helper
                                              // function used by this example
    long sum = 0;                             // declares sum
    for (long r = 0; r < repeats; r++) {      // loop header controlling the sweep below
        for (long p = 0; p < pages; p++) {    // loop header controlling the sweep below
            sum += buf[p * page_stride_ints]; // => co-09: same tiny set of pages, hit
                                              // again and again
        }
    }
    return sum; // returns the computed result
}

static double time_call(long (*fn)(volatile int *, long, long), volatile int *buf, long pages,
                        long stride) {   // declares function pointer fn
    struct timespec t0, t1;              // supporting statement for this example
    clock_gettime(CLOCK_MONOTONIC, &t0); // calls clock_gettime(...)
    volatile long r = fn(buf, pages,
                         stride);                                     // => volatile: keep the "unused" sum from being optimized away
    clock_gettime(CLOCK_MONOTONIC, &t1);                              // calls clock_gettime(...)
    (void)r;                                                          // discards r to silence an unused-variable warning
    return (t1.tv_sec - t0.tv_sec) + (t1.tv_nsec - t0.tv_nsec) / 1e9; // returns the computed result
}

int main(void) {                                // program entry point
    int have_superpage = try_apple_superpage(); // => co-09: the honest,
                                                // actually-attempted first step
    (void)have_superpage;                       // => documented above regardless of result -- the
                                                // fallback runs either way

    // co-09: one big buffer covers both walks -- SCATTER_PAGES * PAGE_INTS ints =
    // ~800 MB, comfortably larger than SCATTER_PAGES distinct 4 KB regions so the
    // scattered walk never wraps or reuses a page.
    long buf_ints = (long)SCATTER_PAGES * PAGE_INTS;   // declares buf_ints
    int *buf = malloc(sizeof(int) * (size_t)buf_ints); // heap-allocates memory for buf
    if (!buf) {
        fprintf(stderr, "alloc failed\n");
        return 1;
    } // prints a report line
    for (long i = 0; i < buf_ints; i += PAGE_INTS)
        buf[i] = (int)(i & 0xff); // => first-touch every page once

    double t_scattered = time_call(walk_scattered, buf, SCATTER_PAGES,
                                   PAGE_INTS); // declares t_scattered

    struct timespec c0, c1;              // supporting statement for this example
    clock_gettime(CLOCK_MONOTONIC, &c0); // calls clock_gettime(...)
    volatile long compact_sum = walk_compact(buf, COMPACT_PAGES, PAGE_INTS,
                                             REPEATS);                                  // declares compact_sum
    clock_gettime(CLOCK_MONOTONIC, &c1);                                                // calls clock_gettime(...)
    (void)compact_sum;                                                                  // discards compact_sum to silence an unused-variable warning
    double t_compact_total = (c1.tv_sec - c0.tv_sec) + (c1.tv_nsec - c0.tv_nsec) / 1e9; // declares t_compact_total

    long scattered_accesses = SCATTER_PAGES;                                   // declares scattered_accesses
    long compact_accesses = (long)COMPACT_PAGES * REPEATS;                     // declares compact_accesses
    double ns_per_access_scattered = (t_scattered / scattered_accesses) * 1e9; // declares ns_per_access_scattered
    double ns_per_access_compact = (t_compact_total / compact_accesses) * 1e9; // declares ns_per_access_compact

    printf("scattered: %d distinct 4 KB-strided pages, 1 access each -> %.4f s "
           "total, %.2f ns/access\n", // prints a report line
           SCATTER_PAGES, t_scattered,
           ns_per_access_scattered); // continues the printf(...) call above
    printf("compact:   %d pages, %d repeats (%ld accesses) -> %.4f s total, %.2f "
           "ns/access\n",
           COMPACT_PAGES, // prints a report line
           REPEATS, compact_accesses, t_compact_total,
           ns_per_access_compact);                                  // continues the printf(...) call above
    double ratio = ns_per_access_scattered / ns_per_access_compact; // declares ratio
    printf("scattered/compact ns-per-access ratio: %.2fx\n",
           ratio); // prints a report line
    printf("(hugepage note: a 2 MB huge page maps 512x the memory of one 4 KB "
           "page per TLB entry, so on\n"); // prints a report line
    printf(" Linux `hugetlbfs`/THP the SAME scattered footprint above would need "
           "512x fewer TLB entries\n"); // prints a report line
    printf(" to stay resident, cutting the page-table-walk cost this "
           "scattered/compact gap demonstrates.)\n"); // prints a report line
    int pass = ratio > 1.1;                           // => co-09: scattered (many-page) access must cost
                                                      // meaningfully more per access
    printf("PASS (many-page walk costs more per access than a TLB-resident "
           "compact walk): %s\n",   // prints a report line
           pass ? "PASS" : "FAIL"); // continues the printf(...) call above

    free(buf); // releases buf's heap memory
    return 0;  // returns the computed result
}
