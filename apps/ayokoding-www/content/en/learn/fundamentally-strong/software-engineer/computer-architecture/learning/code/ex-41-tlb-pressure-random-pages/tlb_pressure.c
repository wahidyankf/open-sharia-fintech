// learning/code/ex-41-tlb-pressure-random-pages/tlb_pressure.c
/* Example 41: random access across many distinct pages vs a compact
   footprint -- verify TLB pressure dominates the many-page case (co-08,
   co-09). */
#include <stdio.h>  // => printf -- the timing/PASS report this program prints
#include <stdlib.h> // => malloc/free/rand -- the buffers and their random visiting orders
#include <time.h>   // => clock_gettime -- the portable wall-clock timer used below

#define PAGE_BYTES \
    16384                                        // => co-08: this machine's real page size
                                                 //    (confirmed: `vm_stat` reports 16384 B pages)
#define INTS_PER_PAGE (PAGE_BYTES / sizeof(int)) // => co-08: 4096 ints span exactly one page
#define NPAGES_BIG \
    100000                 // => co-09: 100,000 distinct pages (~1.6 GB) -- far more
                           //    distinct pages than any realistic TLB can hold
#define NPAGES_SMALL 8     // => co-09: 8 pages (~128 KB) -- trivially TLB-resident
#define ACCESSES 20000000L // => co-09: SAME total access count, both patterns

static double now_seconds(void) {                        // => co-25: shared wall-clock helper, this topic's standard pattern
    struct timespec ts;                                  // supporting statement for this example
    clock_gettime(CLOCK_MONOTONIC, &ts);                 // calls clock_gettime(...)
    return (double)ts.tv_sec + (double)ts.tv_nsec / 1e9; // returns the computed result
}

static void shuffle(int *arr,
                    int n) {          // => co-09: Fisher-Yates -- a random PAGE visiting order,
    for (int i = 0; i < n; i++)       // => co-09: initializes the identity permutation first
        arr[i] = i;                   //    so the TLB cannot rely on any stride pattern
    for (int i = n - 1; i > 0; i--) { // loop header controlling the sweep below
        int j = rand() % (i + 1);     // declares j
        int tmp = arr[i];             // => co-09: standard 3-step swap, first half
        arr[i] = arr[j];              // => co-09: standard 3-step swap, second half
        arr[j] = tmp;                 // declares tmp
    }
}

// co-09: touches exactly ONE int per page (offset 0), so every access that
// crosses into a NEW page requires a virtual->physical translation; if that
// page's translation isn't already cached in the TLB, the MMU must walk the
// page table -- extra latency ON TOP OF whatever the data cache would cost.
static long touch_pages(const int *buf, const int *page_order, int npages,
                        long accesses) {         // defines touch_pages(): helper
                                                 // function used by this example
    long total = 0;                              // declares total
    for (long i = 0; i < accesses; i++) {        // loop header controlling the sweep below
        int p = page_order[i % npages];          // => co-09: cycles through npages repeatedly --
        total += buf[(size_t)p * INTS_PER_PAGE]; //    with NPAGES_BIG, the TLB never stays warm;
    } //    with NPAGES_SMALL, it warms up almost immediately
    return total; // returns the computed result
}

int main(void) {                                                                 // program entry point
    srand(11);                                                                   // => co-25: fixed seed -- reproducible page orders
    int *buf_big = malloc((size_t)NPAGES_BIG * INTS_PER_PAGE * sizeof(int));     // => ~1.6 GB, safely within RAM
    int *buf_small = malloc((size_t)NPAGES_SMALL * INTS_PER_PAGE * sizeof(int)); // => ~128 KB
    int *order_big = malloc((size_t)NPAGES_BIG * sizeof(int));                   // heap-allocates memory for order_big
    int *order_small = malloc((size_t)NPAGES_SMALL * sizeof(int));               // heap-allocates memory for order_small
    if (!buf_big || !buf_small || !order_big || !order_small) {                  // => co-09: guards all four allocations at once
        fprintf(stderr, "alloc failed\n");                                       // prints a report line
        return 1;                                                                // returns the computed result
    } // => co-09: nonzero exit -- allocation failure is not this example's claim
    for (long i = 0; i < (long)NPAGES_BIG * INTS_PER_PAGE; i++)   // => co-09: touches every page of buf_big once
        buf_big[i] = (int)(i % 97);                               // loop header controlling the sweep below
    for (long i = 0; i < (long)NPAGES_SMALL * INTS_PER_PAGE; i++) // => co-09: touches every page of buf_small once
        buf_small[i] = (int)(i % 97);                             // loop header controlling the sweep below
    shuffle(order_big,
            NPAGES_BIG);                // => co-09: one random order over 100,000 pages
    shuffle(order_small, NPAGES_SMALL); // => co-09: one random order over 8 pages

    double t0 = now_seconds();                                            // declares t0
    long sum_big = touch_pages(buf_big, order_big, NPAGES_BIG, ACCESSES); // declares sum_big
    double t1 = now_seconds();                                            // declares t1
    long sum_small = touch_pages(buf_small, order_small, NPAGES_SMALL,
                                 ACCESSES); // declares sum_small
    double t2 = now_seconds();              // declares t2

    double secs_big = t1 - t0;   // declares secs_big
    double secs_small = t2 - t1; // declares secs_small
    printf("ACCESSES=%ld, PAGE_BYTES=%d\n", ACCESSES,
           PAGE_BYTES); // prints a report line
    printf("many pages (%d, ~%.1f MB): sum=%ld, %.4f s (%.2f ns/access)\n",
           NPAGES_BIG, // prints a report line
           (double)(NPAGES_BIG * PAGE_BYTES) / (1024.0 * 1024.0), sum_big,
           secs_big,                   // continues the printf(...) call above
           secs_big * 1e9 / ACCESSES); // continues the printf(...) call above
    printf("compact (%d, ~%.1f KB):    sum=%ld, %.4f s (%.2f ns/access)\n",
           NPAGES_SMALL, // prints a report line
           (double)(NPAGES_SMALL * PAGE_BYTES) / 1024.0, sum_small,
           secs_small,                                                                                 // continues the printf(...) call above
           secs_small * 1e9 / ACCESSES);                                                               // continues the printf(...) call above
    double ratio = secs_big / secs_small;                                                              // => co-09: how much slower the many-page pattern is
    printf("many-page/compact ratio: %.2fx -> %s\n", ratio,                                            // prints a report line
           ratio > 1.3 ? "PASS (TLB/page pressure measurably dominates the many-page case)" : "FAIL"); // continues the printf(...) call above
    free(buf_big);                                                                                     // releases buf_big's heap memory
    free(buf_small);                                                                                   // releases buf_small's heap memory
    free(order_big);                                                                                   // releases order_big's heap memory
    free(order_small);                                                                                 // releases order_small's heap memory
    return ratio > 1.3 ? 0 : 1;                                                                        // returns the computed result
}
