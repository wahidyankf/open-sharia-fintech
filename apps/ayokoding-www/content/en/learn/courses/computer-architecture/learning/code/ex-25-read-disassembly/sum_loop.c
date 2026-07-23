// learning/code/ex-25-read-disassembly/sum_loop.c
/* Example 25: Read Disassembly -- a tiny sum function, compiled to arm64
 * assembly at -O0. */

// ex-25: kept deliberately tiny and UNOPTIMIZED-friendly -- at -O0 the compiler
// emits assembly that maps almost 1:1 to this source, making
// load/store/arithmetic instructions easy to spot for a reader new to reading
// emitted assembly
int sum_loop(const int *array,
             int count) {             // => co-19: takes a pointer and a count -- forces
                                      // real LOADS, not constants
    int total = 0;                    // => co-19: local accumulator -- lives in a STACK slot at -O0
    for (int i = 0; i < count; i++) { // => co-19: a real loop -- forces a
                                      // branch/compare in the assembly
        total += array[i];            // => co-19: array[i] is a LOAD; += is an ADD; total is a
                                      // STORE back
    }
    return total; // => co-19: the final value, returned in the ABI's return
                  // register
}
