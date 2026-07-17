// learning/code/ex-06-unsigned-underflow-loop-bug/unsigned_underflow_loop_bug.c
/* Example 6: Unsigned Underflow Loop Bug -- the classic `size_t i >= 0`
 * infinite loop. */

#include <stddef.h> // => co-12: size_t -- the UNSIGNED index type that causes this whole bug
#include <stdio.h>  // => co-12: printf -- traces both the bug and the fix

// ex-06: BUG DEMONSTRATION -- `for (size_t i = n-1; i >= 0; i--)` never
// terminates because size_t is unsigned: `i >= 0` is a TAUTOLOGY (always true),
// so the loop can only be stopped by a watchdog, never by its own condition. We
// trace 6 steps instead of running it forever -- long enough to SHOW i wrap
// past zero without ever satisfying `i < 0` (which is impossible for an
// unsigned type).
static void trace_buggy_condition(size_t n) { // => co-12: n=3 traces a non-empty case; n=0 traces empty
    printf("n = %zu: i = n - 1 starts at %zu\n", n,
           n - 1);                                     // => co-12: n=0 underflows HERE, before any loop body runs
    size_t i = n - 1;                                  // => co-12: for n=0 this is already SIZE_MAX -- immediate danger
    for (int watchdog = 0; watchdog < 6; watchdog++) { // => co-12: SAFETY CAP -- the real bug has no such cap
        int condition_true = (i >= 0);                 // => co-12: always 1 for size_t -- this IS the bug
        printf("  step %d: i = %-20zu  (i >= 0) = %d\n", watchdog, i,
               condition_true); // prints a report line
        if (!condition_true)
            break; // => co-12: dead code -- size_t can never fail i >= 0
        i--;       // => co-12: decrements past 0 -> wraps to SIZE_MAX, not -1
    }
    printf("  (stopped by watchdog, NOT by the loop condition -- the real bug "
           "never stops)\n"); // => co-12: honesty note
}

// ex-06: THE FIX -- `for (size_t i = n; i-- > 0; )` terminates correctly for n
// == 0 (the post-decrement is evaluated once, `0 > 0` is false, body never
// runs) and for n > 0 (iterates i = n-1 .. 0, then the final post-decrement
// makes `0 > 0` false)
static long sum_reverse_fixed(const int *array, size_t n,
                              size_t *iterations_out) { // defines sum_reverse_fixed(): helper function
                                                        // used by this example
    long total = 0;                                     // => co-12: accumulator -- long avoids overflow for this demo
    size_t iterations = 0;                              // => co-12: counts loop bodies actually executed
    for (size_t i = n; i-- > 0;) {                      // => co-12: THE FIX -- no i >= 0 tautology, terminates always
        total += array[i];                              // => co-12: safe: i is always a valid index 0..n-1 here
        iterations++;                                   // => co-12: one increment per valid index visited
    }
    *iterations_out = iterations; // => co-12: reported back so the caller can
                                  // verify termination
    return total;                 // => co-12: sum of all elements, order-independent
}

int main(void) {                                    // program entry point
    printf("--- bug trace: non-empty (n=3) ---\n"); // => co-12: section header
                                                    // for the non-empty bug trace
    trace_buggy_condition(3);                       // => co-12: shows i=2,1,0 then wraps to SIZE_MAX and beyond
    printf("\n--- bug trace: empty (n=0) ---\n");   // => co-12: section header for
                                                    // the empty-array bug trace
    trace_buggy_condition(0);                       // => co-12: shows the underflow happens on the VERY FIRST line

    printf("\n--- fix: non-empty array {10, 20, 30} ---\n");         // => co-12: section
                                                                     // header for the fixed
                                                                     // non-empty case
    int data[3] = {10, 20, 30};                                      // => co-12: expected sum 60, expected iterations 3
    size_t iters_nonempty = 0;                                       // => co-12: filled in by sum_reverse_fixed
    long sum_nonempty = sum_reverse_fixed(data, 3, &iters_nonempty); // => co-12: runs the FIXED idiom for real
    printf("sum = %ld, iterations = %zu\n", sum_nonempty,
           iters_nonempty); // prints a report line

    printf("\n--- fix: empty array {} ---\n"); // => co-12: section header for the
                                               // fixed empty case
    size_t iters_empty = 0;                    // => co-12: filled in by sum_reverse_fixed
    long sum_empty = sum_reverse_fixed(data, 0,
                                       &iters_empty); // => co-12: n=0 -- must terminate with 0 iterations
    printf("sum = %ld, iterations = %zu\n", sum_empty,
           iters_empty); // prints a report line

    int correct =                                    // => co-12: the assertion this whole example checks
        sum_nonempty == 60 && iters_nonempty == 3 && // => co-12: non-empty fix ran exactly 3 times, summed 60
        sum_empty == 0 && iters_empty == 0;          // => co-12: empty fix ran ZERO times -- proves it terminates
    printf("\n%s\n",
           correct // => co-12: PASS/FAIL verdict
               ? "PASS: fixed reverse loop terminates correctly on both empty and "
                 "non-empty arrays"                                 // supporting statement for this example
               : "FAIL: fixed loop did not terminate as expected"); // supporting
                                                                    // statement for
                                                                    // this example

    return correct ? 0 : 1; // => co-12: nonzero exit on assertion failure
}
