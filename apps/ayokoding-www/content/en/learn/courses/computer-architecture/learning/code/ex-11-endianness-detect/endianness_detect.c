// learning/code/ex-11-endianness-detect/endianness_detect.c
/* Example 11: Endianness Detect -- discover byte order at RUNTIME, not by
 * assumption. */

#include <stdint.h> // => co-15: uint32_t/uint8_t -- fixed-width types make the detection portable
#include <stdio.h>  // => co-15: printf -- reports the runtime-detected byte order

int main(void) {
    // ex-11: a UNION lets one piece of storage be read as either a 32-bit int or
    // 4 separate bytes -- reading `.bytes[0]` inspects whichever byte the
    // hardware placed FIRST in memory, which is exactly what "endianness" means
    union {
        uint32_t as_int;     // => co-15: written once, below
        uint8_t as_bytes[4]; // => co-15: read to inspect memory order
    } probe;

    probe.as_int = 0x00000001u; // => co-15: the number 1 -- its least-significant
                                // byte is 0x01

    int is_little_endian = (probe.as_bytes[0] == 0x01); // => co-15: true only if byte[0] (lowest address) holds the LSB
    int is_big_endian = (probe.as_bytes[0] == 0x00);    // => co-15: true only if byte[0] holds the MOST-significant byte

    printf("probe.as_int     = %u\n",
           probe.as_int); // => co-15: the value written into the union
    printf("byte[0]          = 0x%02x\n",
           probe.as_bytes[0]);                          // => co-15: the byte this whole detection hinges on
    printf("byte[1..3]       = 0x%02x 0x%02x 0x%02x\n", // => co-15: the remaining
                                                        // 3 bytes, all zero for
                                                        // value 1
           probe.as_bytes[1], probe.as_bytes[2], probe.as_bytes[3]);
    printf("detected order   = %s\n", // => co-15: the human-readable verdict
           is_little_endian ? "little-endian" : (is_big_endian ? "big-endian" : "unknown"));

    // ex-11: this machine is arm64 Apple Silicon running macOS -- Apple's arm64
    // platforms run little-endian by default (ARM is BI-endian in hardware, but
    // the OS/ABI fixes it to little-endian), so byte[0] must hold the value's LSB
    // (0x01)
    int correct = is_little_endian; // => co-15: the expected verdict on THIS machine
    printf("%s\n",
           correct // => co-15: PASS/FAIL verdict
               ? "PASS: this machine is little-endian, detected at runtime (not "
                 "assumed)"
               : "FAIL: expected little-endian on this arm64 Apple Silicon machine");

    return correct ? 0 : 1; // => co-15: nonzero exit on assertion failure
}
