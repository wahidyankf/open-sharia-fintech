// learning/code/ex-20-array-row-major-layout/array_row_major_layout.c
/* Example 20: Array Row-Major Layout -- hand-computed &a[i][j] matches C's own
 * address. */

#include <stdint.h> // => co-17: uintptr_t -- portable integer representation of an address
#include <stdio.h>  // => co-17: printf -- reports both the hand-computed and compiler-computed addresses

#define ROWS 3 // => co-17: R -- number of rows in the 2-D array under test
#define COLS 5 // => co-17: C -- number of columns in the 2-D array under test

// ex-20: the verification loop below checks EVERY cell in the array, not just
// one sample cell -- a single spot check could pass by coincidence, so this
// example deliberately sweeps the whole grid.
int main(void) {                       // program entry point
    static int a[ROWS][COLS];          // => co-17: a genuine C 2-D array -- stored
                                       // ROW-MAJOR by the standard
    for (int i = 0; i < ROWS; i++)     // => co-17: fill with a distinct value per cell, for sanity only
        for (int j = 0; j < COLS; j++) // loop header controlling the sweep below
            a[i][j] = i * 100 + j;     // => co-17: value is irrelevant to this example -- ADDRESS is

    uintptr_t base = (uintptr_t)&a[0][0]; // => co-17: the array's own base address --
                                          // everything below is relative to it

    int all_match = 1;                   // => co-17: accumulates the verdict across every (i, j) checked
    for (int i = 0; i < ROWS; i++) {     // => co-17: check several rows, not just one
        for (int j = 0; j < COLS; j++) { // => co-17: and several columns within each row
            // ex-20: row-major means element (i, j) sits at base + (i*COLS + j) *
            // sizeof(int) -- row i's COLS elements all come before row i+1 starts
            uintptr_t hand_computed = base + (uintptr_t)(i * COLS + j) * sizeof(int); // => co-17: the manual formula
            uintptr_t compiler_computed = (uintptr_t)&a[i][j];                        // => co-17: what &a[i][j] actually gives
            int match = (hand_computed == compiler_computed);                         // => co-17: per-cell equality check
            if (!match) {                                                             // => co-17: only print failures, to keep output short
                printf("MISMATCH at (%d,%d): hand=0x%lx compiler=0x%lx\n",            // prints a
                                                                                      // report line
                       i, j, (unsigned long)hand_computed,
                       (unsigned long)compiler_computed); // continues the printf(...) call above
                all_match = 0;                            // => co-17: records the failure
            }
        }
    }

    printf("checked %d x %d = %d cells\n", ROWS, COLS,
           ROWS * COLS); // => co-17: total cells verified
    printf("&a[1][2] (compiler)  = %p\n",
           (void *)&a[1][2]); // => co-17: a concrete example address,
                              // compiler-computed
    printf("base + (1*%d+2)*4    = %p\n",
           COLS,                                                      // => co-17: the SAME cell, by hand formula
           (void *)(base + (uintptr_t)(1 * COLS + 2) * sizeof(int))); // supporting statement for this example

    printf("%s\n", all_match // => co-17: PASS/FAIL verdict across all cells
                       ? "PASS: hand-computed row-major address matches &a[i][j] "
                         "for every cell checked" // supporting statement for this
                                                  // example
                       : "FAIL: at least one cell's hand-computed address "
                         "diverged"); // supporting statement for this example

    return all_match ? 0 : 1; // => co-17: nonzero exit on any mismatch
}
