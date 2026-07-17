// learning/code/ex-21-latency-hierarchy-table/latency_hierarchy_table.c
/* Example 21: Latency Hierarchy Table -- textbook order-of-magnitude cycle
 * costs, printed increasing. */

#include <stdio.h> // => co-01: printf -- renders the table this example verifies

// ex-21: these are WELL-KNOWN order-of-magnitude figures from the CS:APP /
// Drepper literature (see the syllabus's "Read more" section), NOT numbers
// measured on this machine -- this program never claims otherwise; it only
// checks their RELATIVE ordering is internally consistent (each level strictly
// slower than the one above)
struct LatencyRow {     // struct layout definition
    const char *level;  // => co-01: the memory-hierarchy level's name
    long approx_cycles; // => co-01: an order-of-magnitude cycle count, from the
                        // literature
};

static const struct LatencyRow TABLE[] = {
    // => co-01: registers -> L1 -> L2 -> L3 -> DRAM, strictly increasing
    {"register", 1},  // => co-01: ~1 cycle -- effectively free, the CPU's own storage
    {"L1 cache", 4},  // => co-01: ~4 cycles -- CS:APP's commonly cited L1 hit latency
    {"L2 cache", 12}, // => co-01: ~10-20 cycles -- one order of magnitude above L1
    {"L3 cache", 40}, // => co-01: ~30-70 cycles -- another step up, shared across cores
    {"DRAM", 200},    // => co-01: ~100-300 cycles -- Drepper's cpumemory.pdf range
};
#define TABLE_ROWS \
    (sizeof(TABLE) / sizeof(TABLE[0])) // => co-01: number of rows -- 5, computed
                                       // rather than hardcoded

int main(void) { // program entry point
    printf("Approximate memory-hierarchy access costs (order of magnitude, "
           "from\n"); // => co-01: citation header
    printf("CS:APP / Drepper's \"What Every Programmer Should Know About "
           "Memory\"):\n");                   // prints a report line
    printf("%-12s %s\n", "LEVEL", "~CYCLES"); // => co-01: column header
    for (size_t i = 0; i < TABLE_ROWS; i++) { // => co-01: one printed row per hierarchy level
        printf("%-12s %ld\n", TABLE[i].level,
               TABLE[i].approx_cycles); // => co-01: level name and its approximate cost
    }

    // ex-21: the claim -- the sequence printed above is STRICTLY INCREASING,
    // matching the memory hierarchy's own capacity-for-latency tradeoff (co-01)
    int strictly_increasing = 1;                                    // => co-01: accumulates the ordering check across all rows
    for (size_t i = 1; i < TABLE_ROWS; i++) {                       // => co-01: compares each row to the one before it
        if (TABLE[i].approx_cycles <= TABLE[i - 1].approx_cycles) { // => co-01: a violation would mean the
                                                                    // table is out of order
            strictly_increasing = 0;                                // => co-01: records the violation
            printf("ORDER VIOLATION: %s (%ld) <= %s (%ld)\n",       // prints a report line
                   TABLE[i].level,
                   TABLE[i].approx_cycles, // continues the printf(...) call above
                   TABLE[i - 1].level,
                   TABLE[i - 1].approx_cycles); // continues the printf(...) call above
        }
    }

    printf("%s\n",
           strictly_increasing // => co-01: PASS/FAIL verdict
               ? "PASS: printed latency sequence is strictly increasing register -> "
                 "... -> DRAM"                                          // supporting statement for this example
               : "FAIL: latency sequence was not strictly increasing"); // supporting
                                                                        // statement
                                                                        // for this
                                                                        // example

    return strictly_increasing ? 0 : 1; // => co-01: nonzero exit on assertion failure
}
