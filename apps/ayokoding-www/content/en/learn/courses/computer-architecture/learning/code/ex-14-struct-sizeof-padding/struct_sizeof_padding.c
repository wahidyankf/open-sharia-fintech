// learning/code/ex-14-struct-sizeof-padding/struct_sizeof_padding.c
/* Example 14: Struct Sizeof Padding -- sizeof exceeds the raw field-byte sum.
 */

#include <stddef.h> // => co-16: offsetof -- the standard, portable way to ask "where does this field start?"
#include <stdio.h>  // => co-16: printf -- reports sizeof and each field's offset

// ex-14: char(1) + int(4) + char(1) = 6 raw bytes, but the COMPILER inserts
// padding so `b` (a 4-byte int) starts at a 4-byte-aligned offset -- this is
// the struct the whole padding/alignment sub-arc (ex-14..ex-18) is built around
struct Mixed {
    char a; // => co-16: 1 byte, offset 0
    int b;  // => co-16: 4 bytes, but needs 4-byte ALIGNMENT -- forces padding
    char c; // => co-16: 1 byte, placed right after b
};

int main(void) { // => co-16: single-file, no args -- fully self-contained
    printf("sizeof(char)     = %zu\n",
           sizeof(char)); // => co-16: 1 -- the baseline unit
    printf("sizeof(int)      = %zu\n",
           sizeof(int));                               // => co-16: 4 on this platform -- also int's natural alignment
    printf("raw field sum    = %zu\n",                 // => co-16: 1 + 4 + 1 = 6 -- what a naive
                                                       // reader might expect
           sizeof(char) + sizeof(int) + sizeof(char)); // => co-16: the naive sum, computed with no struct involved
    printf("sizeof(Mixed)    = %zu\n",
           sizeof(struct Mixed)); // => co-16: the ACTUAL size, inflated by
                                  // inserted padding

    printf("offsetof(a)      = %zu\n", offsetof(struct Mixed,
                                                a)); // => co-16: 0 -- first field, no padding needed before it
    printf("offsetof(b)      = %zu\n", offsetof(struct Mixed,
                                                b)); // => co-16: 4 -- 3 padding bytes inserted after `a`
    printf("offsetof(c)      = %zu\n", offsetof(struct Mixed,
                                                c)); // => co-16: 8 -- right after `b`, no gap needed here

    // ex-14: the claim -- sizeof(Mixed) is STRICTLY GREATER than the naive 6-byte
    // sum, because the compiler must pad `a` out to 4 bytes before `b` can start
    // aligned
    int correct = sizeof(struct Mixed) > 6; // => co-16: padding inflated the struct beyond the raw field sum
    printf("%s\n",
           correct // => co-16: PASS/FAIL verdict
               ? "PASS: sizeof(Mixed) exceeds the 6-byte raw field sum due to "
                 "alignment padding"                                                  // => co-16: PASS branch text
               : "FAIL: sizeof(Mixed) did not exceed the raw field sum as expected"); // => co-16: FAIL branch text

    return correct ? 0 : 1; // => co-16: nonzero exit on assertion failure
}
