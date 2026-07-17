// learning/code/ex-19-pointer-arithmetic-stride/pointer_arithmetic_stride.c
/* Example 19: Pointer Arithmetic Stride -- p+1 advances by sizeof(T), not by 1
 * byte. */

#include <stdint.h> // => co-17: uintptr_t -- the portable integer type wide enough to hold a pointer
#include <stdio.h>  // => co-17: printf -- reports the raw address delta produced by p+1

struct Point { // => co-17: a multi-field struct -- sizeof(Point) is NOT 1
    int x;     // => co-17: 4 bytes
    int y;     // => co-17: 4 bytes
    int z;     // => co-17: 4 bytes -- sizeof(struct Point) expected to be 12
};

int main(void) { // program entry point
    struct Point points[4] = {
        // => co-17: a small array so `p` and `p+1` both stay in-bounds
        {1, 2, 3},
        {4, 5, 6},
        {7, 8, 9},
        {10, 11, 12} // supporting statement for this example
    };

    struct Point *p = &points[0]; // => co-17: pointer to the FIRST element
    struct Point *p_next = p + 1; // => co-17: pointer arithmetic -- C scales by sizeof(*p), not by 1

    uintptr_t addr_p = (uintptr_t)p;         // => co-17: raw address of p, as an integer
    uintptr_t addr_next = (uintptr_t)p_next; // => co-17: raw address of p+1, as an integer
    uintptr_t stride = addr_next - addr_p;   // => co-17: the ACTUAL byte distance the increment moved

    printf("sizeof(struct Point) = %zu\n",
           sizeof(struct Point));                     // => co-17: expected 12 -- 3 ints, no padding
                                                      // needed here
    printf("address of p         = %p\n", (void *)p); // => co-17: p's raw address
    printf("address of p+1       = %p\n",
           (void *)p_next); // => co-17: p+1's raw address
    printf("measured stride      = %lu bytes\n",
           (unsigned long)stride); // => co-17: the difference this example verifies

    // ex-19: the claim -- p+1 advances the raw address by EXACTLY sizeof(struct
    // Point) bytes, never by 1 byte, because pointer arithmetic is TYPE-scaled in
    // C
    int correct = (stride == sizeof(struct Point)); // => co-17: direct equality check
    printf("%s\n", correct                          // => co-17: PASS/FAIL verdict
                       ? "PASS: p+1 advanced the address by exactly "
                         "sizeof(struct Point) bytes" // supporting statement for
                                                      // this example
                       : "FAIL: measured stride did not equal sizeof(struct "
                         "Point)"); // supporting statement for this example

    return correct ? 0 : 1; // => co-17: nonzero exit on assertion failure
}
