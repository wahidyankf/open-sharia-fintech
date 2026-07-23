// learning/code/ex-15-struct-reorder-shrink/struct_reorder_shrink.c
/* Example 15: Struct Reorder Shrink -- largest-field-first reordering shrinks
 * sizeof. */

#include <stdio.h> // => co-16: printf -- reports both struct sizes for a direct comparison

// ex-14's field order, reproduced here so this file is fully self-contained (no
// cross-example #include, per DD-20)
struct Mixed {
    char a; // => co-16: 1 byte, offset 0
    int b;  // => co-16: 4 bytes -- forces 3 bytes of padding before it
    char c; // => co-16: 1 byte
};

// ex-15: the SAME three fields, reordered LARGEST-first -- the int now starts
// already aligned at offset 0, so no padding is needed before it; the two
// 1-byte chars can share the remaining space in the int's trailing alignment
// slack
struct MixedReordered {
    int b;  // => co-16: 4 bytes, offset 0 -- naturally aligned already
    char a; // => co-16: 1 byte, offset 4 -- no padding needed here
    char c; // => co-16: 1 byte, offset 5 -- packs right next to `a`
};

int main(void) {
    printf("sizeof(Mixed)           = %zu\n",
           sizeof(struct Mixed)); // => co-16: ex-14's original, padded size
    printf("sizeof(MixedReordered)  = %zu\n",
           sizeof(struct MixedReordered)); // => co-16: this example's reordered size

    // ex-15: the claim -- reordering fields largest-first produces a STRICTLY
    // SMALLER struct than ex-14's char-int-char order, for the identical set of
    // fields
    int correct = sizeof(struct MixedReordered) < sizeof(struct Mixed); // => co-16: direct size comparison
    printf("%s\n",
           correct // => co-16: PASS/FAIL verdict
               ? "PASS: largest-first field order shrinks sizeof vs the original "
                 "char-int-char order"
               : "FAIL: reordered struct was not smaller than the original");

    return correct ? 0 : 1; // => co-16: nonzero exit on assertion failure
}
