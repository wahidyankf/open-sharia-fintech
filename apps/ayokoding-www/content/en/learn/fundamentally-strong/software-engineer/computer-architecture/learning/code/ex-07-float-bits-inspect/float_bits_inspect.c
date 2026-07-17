// learning/code/ex-07-float-bits-inspect/float_bits_inspect.c
/* Example 7: Float Bits Inspect -- decode 1.0f's IEEE-754
 * sign/exponent/mantissa. */

#include <stdio.h>  // => co-13: printf -- reports the decoded fields
#include <string.h> // => co-13: memcpy -- the STANDARD, no-UB way to reinterpret float bits as an integer

int main(void) {
    float value = 1.0f;                 // => co-13: the simplest nontrivial IEEE-754 value to decode
    unsigned int bits;                  // => co-13: destination for value's raw 32-bit representation
    memcpy(&bits, &value, sizeof bits); // => co-13: memcpy avoids strict-aliasing
                                        // UB that a union/cast risks

    unsigned int sign = (bits >> 31) & 0x1u;      // => co-13: bit 31 -- 0 means positive
    unsigned int exponent = (bits >> 23) & 0xFFu; // => co-13: bits 30..23, 8 bits, BIASED by +127
    unsigned int mantissa = bits & 0x7FFFFFu;     // => co-13: bits 22..0, 23 bits, the fractional significand

    printf("value        = %g\n",
           (double)value);                   // => co-13: the number as C prints it
    printf("bits         = 0x%08x\n", bits); // => co-13: the raw 32-bit pattern
    printf("sign         = %u\n",
           sign);                                         // => co-13: expected 0 -- 1.0 is positive
    printf("exponent     = %u (biased), %d (unbiased)\n", // => co-13: unbiased =
                                                          // stored - 127, IEEE-754's
                                                          // exponent bias
           exponent, (int)exponent - 127);
    printf("mantissa     = 0x%06x\n",
           mantissa); // => co-13: expected 0 -- 1.0's significand is exactly 1.0
                      // x 2^0

    // ex-07: 1.0f's KNOWN IEEE-754 single-precision encoding is sign=0, biased
    // exponent=127 (unbiased 0), mantissa=0 -- the implicit leading 1 bit
    // supplies the "1." and the stored fraction is all zero, giving exactly 1.0 x
    // 2^0
    int correct = sign == 0 && exponent == 127 && mantissa == 0; // => co-13: the exact known encoding, checked directly
    printf("%s\n", correct                                       // => co-13: PASS/FAIL verdict
                       ? "PASS: 1.0f decodes to sign=0, exponent=127 (unbiased "
                         "0), mantissa=0"
                       : "FAIL: decoded fields do not match the known IEEE-754 "
                         "encoding of 1.0");

    return correct ? 0 : 1; // => co-13: nonzero exit on assertion failure
}
