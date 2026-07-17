// learning/code/ex-01-print-int-bytes/print_int_bytes.c
/* Example 1: Print Int Bytes -- reinterpret an int's storage as raw bytes. */

#include <stdint.h> // => co-11: int32_t -- a FIXED-width int, so "4 bytes" is guaranteed, not assumed
#include <stdio.h>  // => co-11: printf/puts -- the report this program prints

int main(void) {                // => co-11: single-file, no args -- fully self-contained
    int32_t value = 0x11223344; // => co-11: a value with 4 visibly DIFFERENT byte values
    // => co-11: 0x11, 0x22, 0x33, 0x44 -- chosen so byte ORDER is unambiguous in
    // the printed dump

    unsigned char *bytes = (unsigned char *)&value; // => co-11: reinterpret the 4-byte int as 4 raw bytes
    // => co-15: THIS cast is the entire lesson -- it exposes the STORAGE order,
    // not the numeric value

    printf("value        = 0x%08x (%d)\n", (unsigned)value,
           value); // => co-11: the number, as C prints it
    printf("byte[0]      = 0x%02x\n",
           bytes[0]); // => co-15: lowest ADDRESS -- first byte in memory
    printf("byte[1]      = 0x%02x\n",
           bytes[1]);                            // => co-15: second byte in memory
    printf("byte[2]      = 0x%02x\n", bytes[2]); // => co-15: third byte in memory
    printf("byte[3]      = 0x%02x\n",
           bytes[3]); // => co-15: highest ADDRESS -- last byte in memory

    // ex-01: on a LITTLE-endian machine (this one), the LEAST-significant byte
    // (0x44) is stored at the LOWEST address -- byte[0] == 0x44, not 0x11
    int little_endian_order =                       // => co-15: the assertion this program exists to
                                                    // check
        (bytes[0] == 0x44) && (bytes[1] == 0x33) && // => co-15: 0x44 first, 0x33 second (reversed order)
        (bytes[2] == 0x22) && (bytes[3] == 0x11);   // => co-15: 0x22 third, 0x11 last -- fully reversed

    printf("%s\n",
           little_endian_order // => co-15: prints the verdict this whole example
                               // proves
               ? "PASS: byte[0]=0x44 .. byte[3]=0x11 -- little-endian storage "
                 "confirmed"
               : "FAIL: byte order does not match little-endian expectation");

    return little_endian_order ? 0 : 1; // => co-11: nonzero exit signals a failed assertion
}
