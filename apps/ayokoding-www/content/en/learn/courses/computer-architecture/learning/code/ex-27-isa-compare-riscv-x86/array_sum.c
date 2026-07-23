// learning/code/ex-27-isa-compare-riscv-x86/array_sum.c
/* Example 27: ISA Compare RISC-V x86 -- the SAME function, two genuinely
 * different ISAs. */

// ex-27: no libc calls, no globals -- fully FREESTANDING so the RISC-V
// bare-metal
// (`-elf-`) cross-compiler can emit pure function assembly with no startup code
// needed
int array_sum(const int *a,
              int n) {            // => co-18: identical C source compiled for BOTH target ISAs below
    int sum = 0;                  // => co-18: accumulator -- how it's held differs per ISA
                                  // (register/stack)
    for (int i = 0; i < n; i++) { // => co-18: the loop whose CONTROL FLOW differs
                                  // across CISC vs RISC
        sum += a[i];              // => co-18: a[i] is a memory operand on x86 CISC, load+add on
                                  // RISC-V
    }
    return sum; // => co-18: returned per each ISA's OWN calling convention
}
