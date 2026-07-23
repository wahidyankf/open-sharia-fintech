// learning/code/ex-26-registers-in-asm/three_arg_fn.c
/* Example 26: Registers in Asm -- 3 int args land in AAPCS64's x0/x1/x2
 * argument registers. */

// ex-26: three plain int parameters, no struct/array indirection -- the
// SIMPLEST case for seeing the AAPCS64 (ARM's 64-bit calling convention)
// argument-register rule: the first NGRN (up to 8) integer/pointer arguments go
// in x0..x7 (w0..w7 for 32-bit)
int weighted_sum(int a, int b,
                 int c) {         // => co-19: a lands in w0, b in w1, c in w2 -- BEFORE
                                  // the prologue even runs
    return a * 2 + b * 3 + c * 5; // => co-19: pure arithmetic -- no loads needed
                                  // for the ARGUMENTS themselves
}
