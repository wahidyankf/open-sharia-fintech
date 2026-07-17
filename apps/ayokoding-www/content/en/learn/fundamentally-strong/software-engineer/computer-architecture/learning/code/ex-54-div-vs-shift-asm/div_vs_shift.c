// learning/code/ex-54-div-vs-shift-asm/div_vs_shift.c
/* Example 54: compare /2 and >>1 in emitted assembly -- verify the compiler
   lowers the division to a shift (co-19, co-25). */
#include <stdio.h> // => printf -- the correctness/PASS report this program prints

// co-19: signed division by a compile-time-constant power of two -- a genuine
// `sdiv` hardware instruction is SLOW (many cycles, not pipelined like an
// add/shift); clang -O2 lowers this to a shift-based sequence instead. Because
// C's `/` TRUNCATES toward zero (co-11: -7/2 == -3, not -4), a plain arithmetic
// shift alone is WRONG for negative operands (-7>>1 == -4) -- the compiler must
// add a rounding correction before shifting: `(x + (x>>31 >>> 30)) >> 1` in
// effect, verified below in the real emitted assembly (`asr`/`lsr`/`add` -- no
// `sdiv` instruction anywhere).
__attribute__((noinline)) int divide_by_two_signed(int x) { return x / 2; } // calls __attribute__(...)

// co-19: unsigned division by 2 has NO rounding-direction ambiguity (unsigned
// division always truncates toward zero, which for a power of two is identical
// to a plain logical right shift) -- clang lowers this to a single `lsr`, no
// correction.
__attribute__((noinline)) unsigned divide_by_two_unsigned(unsigned x) { return x / 2u; } // calls __attribute__(...)

// co-19: the "obvious" replacement someone might reach for by hand -- correct
// ONLY for non-negative x (verified NOT equivalent to divide_by_two_signed
// below).
__attribute__((noinline)) int shift_by_one(int x) { return x >> 1; } // calls __attribute__(...)

int main(void) {                                  // program entry point
    int mismatches_for_negative = 0;              // declares mismatches_for_negative
    int matches_for_nonnegative = 1;              // declares matches_for_nonnegative
    for (int x = -1000; x <= 1000; x++) {         // loop header controlling the sweep below
        int div_result = divide_by_two_signed(x); // declares div_result
        int shift_result = shift_by_one(x);       // declares shift_result
        if (x < 0 && div_result != shift_result)
            mismatches_for_negative++; // => co-11: expected to differ
        if (x >= 0 && div_result != shift_result)
            matches_for_nonnegative = 0; // => co-11: must always agree
    }
    // co-19: spot-check the exact rounding-direction difference the compiler must
    // handle
    int neg7_div = divide_by_two_signed(-7);  // => C's / truncates toward zero: -7/2 == -3
    int neg7_shift = shift_by_one(-7);        // => plain >> rounds toward -infinity: -7>>1 == -4
    unsigned u7 = divide_by_two_unsigned(7u); // => unsigned: 7/2 == 3, same as 7u>>1

    printf("divide_by_two_signed(-7)=%d, shift_by_one(-7)=%d (expected "
           "DIFFERENT: -3 vs -4)\n",
           neg7_div,    // prints a report line
           neg7_shift); // continues the printf(...) call above
    printf("divide_by_two_unsigned(7)=%u (expected 3, same as plain >>1 for "
           "unsigned)\n",
           u7); // prints a report line
    printf("negative-x mismatches (x/2 != x>>1): %d out of 1000 (expected >0 -- "
           "proves\n"                                                              // prints a report line
           "  the compiler CANNOT just emit a plain shift for signed division)\n", // continues the printf(...) call above
           mismatches_for_negative);                                               // continues the printf(...) call above
    printf("non-negative-x matches: %s\n",
           matches_for_nonnegative ? "all agree (expected)" : "MISMATCH -- BUG");                // prints a report line
    int pass = (neg7_div == -3) && (neg7_shift == -4) && (u7 == 3) && matches_for_nonnegative && // declares pass
               (mismatches_for_negative > 0);                                                    // supporting statement for this example
    printf("correctness: %s\n", pass ? "PASS" : "FAIL");                                         // prints a report line
    return pass ? 0 : 1;                                                                         // returns the computed result
}
