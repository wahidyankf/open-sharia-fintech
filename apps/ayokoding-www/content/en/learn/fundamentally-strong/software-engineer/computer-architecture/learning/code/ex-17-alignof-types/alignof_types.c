// learning/code/ex-17-alignof-types/alignof_types.c
/* Example 17: Alignof Types -- _Alignof grows (non-decreasing) as type size
 * grows. */

#include <stdio.h> // => co-16: printf -- reports each type's size and required alignment

// ex-17: a small struct is included so "alignment of a struct" (its LARGEST
// member's alignment, by the C standard's rules) has a concrete example
// alongside the scalars
struct Pair { // => co-16: two doubles -- the struct's own alignment mirrors
              // double's
    double x; // => co-16: 8-byte aligned member
    double y; // => co-16: 8-byte aligned member
};

int main(void) {
    printf("%-16s size=%zu  alignof=%zu\n", "char", sizeof(char),
           _Alignof(char)); // => co-16: 1-byte type
    printf("%-16s size=%zu  alignof=%zu\n", "short", sizeof(short),
           _Alignof(short)); // => co-16: 2-byte type
    printf("%-16s size=%zu  alignof=%zu\n", "int", sizeof(int),
           _Alignof(int)); // => co-16: 4-byte type
    printf("%-16s size=%zu  alignof=%zu\n", "double", sizeof(double),
           _Alignof(double)); // => co-16: 8-byte type
    printf("%-16s size=%zu  alignof=%zu\n", "struct Pair", sizeof(struct Pair),
           _Alignof(struct Pair)); // => co-16: struct case

    // ex-17: the claim -- alignment is NON-DECREASING as these types grow: char
    // <= short <= int <= double, and struct Pair's alignment matches double's
    // (its largest member) rather than exceeding it
    int correct = _Alignof(char) <= _Alignof(short) &&       // => co-16: 1 <= 2
                  _Alignof(short) <= _Alignof(int) &&        // => co-16: 2 <= 4
                  _Alignof(int) <= _Alignof(double) &&       // => co-16: 4 <= 8
                  _Alignof(struct Pair) == _Alignof(double); // => co-16: struct inherits its largest
                                                             // member's alignment

    printf("%s\n",
           correct // => co-16: PASS/FAIL verdict
               ? "PASS: alignment is non-decreasing char <= short <= int <= double"
               : "FAIL: alignment ordering did not hold as expected");

    return correct ? 0 : 1; // => co-16: nonzero exit on assertion failure
}
