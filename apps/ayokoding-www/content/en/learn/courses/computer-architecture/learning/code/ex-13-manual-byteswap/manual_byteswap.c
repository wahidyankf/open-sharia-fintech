// learning/code/ex-13-manual-byteswap/manual_byteswap.c
/* Example 13: Manual Byteswap -- hand-written uint32_t byte swap, cross-checked
 * against htonl. */

#include <arpa/inet.h> // => co-15: htonl -- the trusted reference implementation this example checks against
#include <stdint.h>    // => co-15: uint32_t -- the fixed-width value being swapped
#include <stdio.h>     // => co-15: printf -- reports both swap implementations side by side

// ex-13: hand-written byte swap -- shifts and masks pull out each of the 4
// bytes and reassembles them in REVERSED order, with no library call at all
static uint32_t swap_bytes_manual(uint32_t value) {
    uint32_t byte0 = (value >> 0) & 0xFFu;  // => co-15: least-significant byte (bits 7..0)
    uint32_t byte1 = (value >> 8) & 0xFFu;  // => co-15: next byte (bits 15..8)
    uint32_t byte2 = (value >> 16) & 0xFFu; // => co-15: next byte (bits 23..16)
    uint32_t byte3 = (value >> 24) & 0xFFu; // => co-15: most-significant byte (bits 31..24)
    // ex-13: reassemble with byte0 (was LOWEST) now in the HIGHEST position, and
    // vice versa -- exactly what htonl does on a little-endian host
    return (byte0 << 24) | (byte1 << 16) | (byte2 << 8) | byte3; // => co-15: fully reversed byte order
}

int main(void) {
    uint32_t value = 0x11223344u; // => co-15: same recognizable value used
                                  // throughout this batch

    uint32_t manual_swap = swap_bytes_manual(value); // => co-15: this example's own hand-written implementation
    uint32_t library_swap = htonl(value);            // => co-15: the trusted reference --
                                                     // htonl on THIS little-endian host

    printf("value            = 0x%08x\n", value); // => co-15: the input
    printf("manual swap      = 0x%08x\n",
           manual_swap); // => co-15: expected 0x44332211 -- fully byte-reversed
    printf("htonl(value)     = 0x%08x\n",
           library_swap); // => co-15: htonl on a little-endian host also fully
                          // reverses

    // ex-13: the claim -- the hand-written swap produces the IDENTICAL 32-bit
    // result that htonl produces on this little-endian host (both are pure byte
    // reversals here)
    int correct = (manual_swap == library_swap); // => co-15: direct equality check between
                                                 // both implementations
    printf("%s\n", correct                       // => co-15: PASS/FAIL verdict
                       ? "PASS: hand-written byte swap matches htonl's output on "
                         "this little-endian host"
                       : "FAIL: manual swap diverged from htonl's result");

    return correct ? 0 : 1; // => co-15: nonzero exit on assertion failure
}
