// learning/code/ex-16-packed-struct/packed_struct.c
/* Example 16: Packed Struct -- __attribute__((packed)) removes padding, at a
 * real cost. */

#include <stdio.h> // => co-16: printf -- reports the packed size vs the unpacked size

struct Mixed { // => co-16: ex-14's original order, reproduced (self-contained)
    char a;    // => co-16: 1 byte, offset 0
    int b;     // => co-16: 4 bytes -- normally forces 3 padding bytes
    char c;    // => co-16: 1 byte
};

// ex-16: __attribute__((packed)) is a real GNU/Clang extension (documented in
// the Clang/GCC manuals) that tells the compiler to use offset =
// previous_offset + previous_size for EVERY field, ignoring each field's
// natural alignment entirely
struct __attribute__((packed)) MixedPacked {
    char a; // => co-16: 1 byte, offset 0
    int b;  // => co-16: 4 bytes, offset 1 -- MISALIGNED (not a multiple of 4)
    char c; // => co-16: 1 byte, offset 5
};

int main(void) {
    printf("sizeof(Mixed)        = %zu\n",
           sizeof(struct Mixed)); // => co-16: ex-14's padded size
    printf("sizeof(MixedPacked)  = %zu\n",
           sizeof(struct MixedPacked));    // => co-16: expected exactly 6 -- no
                                           // padding at all
    printf("raw field sum        = %zu\n", // => co-16: 1 + 4 + 1 -- the
                                           // theoretical minimum
           sizeof(char) + sizeof(int) + sizeof(char));

    // ex-16: the claim -- packing makes sizeof EXACTLY equal the raw field-byte
    // sum, unlike ex-14's padded 8-byte version
    int correct = sizeof(struct MixedPacked) == 6; // => co-16: exact match to the raw field sum
    printf("%s\n",
           correct // => co-16: PASS/FAIL verdict
               ? "PASS: packed struct's sizeof equals the exact 6-byte raw field sum"
               : "FAIL: packed struct size did not equal the raw field sum");

    // ex-16: the REAL cost, stated honestly rather than measured here -- field
    // `b` inside MixedPacked now starts at offset 1, which is NOT a multiple
    // of 4. On this arm64 machine the hardware tolerates misaligned loads (see
    // ex-18), but on strict-alignment ISAs a misaligned 4-byte load either traps
    // (SIGBUS) or requires the compiler to emit multiple single-byte loads plus
    // shifts/ORs to reassemble the value -- packing trades memory footprint for
    // per-access CPU cost.
    printf("note: MixedPacked.b starts at a MISALIGNED offset -- see ex-18 for "
           "the cost\n");

    return correct ? 0 : 1; // => co-16: nonzero exit on assertion failure
}
