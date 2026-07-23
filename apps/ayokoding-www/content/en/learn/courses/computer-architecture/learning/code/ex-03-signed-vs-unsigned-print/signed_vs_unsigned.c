// learning/code/ex-03-signed-vs-unsigned-print/signed_vs_unsigned.c
/* Example 3: Signed vs Unsigned Print -- the SAME bit pattern read two ways. */

#include <stdio.h> // => co-11: printf -- %d and %u format the SAME bits with opposite meanings

int main(void) {
    int signed_value = -1; // => co-11: -1 in two's complement is ALL-ONES bits
    // => co-11: 32 ones: 0xFFFFFFFF -- no other bit pattern means -1 under two's
    // complement

    unsigned int reinterpreted = (unsigned int)signed_value; // => co-12: SAME bits, unsigned TYPE -- no bits change
    // => co-12: reinterpreting, not converting a VALUE -- the storage is
    // untouched

    printf("signed_value    (%%d) = %d\n",
           signed_value); // => co-11: prints -1, the signed reading
    printf("reinterpreted   (%%u) = %u\n",
           reinterpreted); // => co-12: prints 4294967295, the unsigned reading
    printf("signed_value    (%%u) = %u\n",
           (unsigned)signed_value); // => co-12: same bits, cast inline, same result

    // ex-03: 4294967295 is UINT_MAX == 2^32 - 1 -- the only unsigned value whose
    // bit pattern is all-ones, which is exactly what -1's two's-complement
    // encoding is
    int correct = reinterpreted == 4294967295u; // => co-12: the literal from the syllabus, checked directly
    printf("%s\n",
           correct // => co-12: PASS/FAIL verdict this example exists to print
               ? "PASS: -1 printed as %u shows 4294967295 (UINT_MAX)"
               : "FAIL: unexpected unsigned reinterpretation of -1");

    return correct ? 0 : 1; // => co-11: nonzero exit on assertion failure
}
