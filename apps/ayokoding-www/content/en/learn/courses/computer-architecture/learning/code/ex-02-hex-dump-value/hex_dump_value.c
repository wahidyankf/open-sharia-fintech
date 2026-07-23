// learning/code/ex-02-hex-dump-value/hex_dump_value.c
/* Example 2: Hex-Dump Value -- byte-by-byte hex dump cross-checked against
 * printf("%x"). */

#include <stdint.h> // => co-11: uint32_t -- fixed-width, so nibble count is guaranteed to be 8
#include <stdio.h>  // => co-11: printf/snprintf -- builds both the dump and the reference string
#include <string.h> // => co-11: strcmp -- compares the two independently-built hex strings

int main(void) {
    uint32_t value = 0xCAFEBABEu; // => co-11: a value using every hex digit range A-F, 0-9

    unsigned char *bytes = (unsigned char *)&value; // => co-11: same reinterpret-cast technique as ex-01
    char dump[9];                                   // => co-11: 8 hex nibbles + NUL -- built byte-by-byte below
    // ex-02: reconstruct the number's canonical hex text by reading bytes
    // HIGH-to-LOW (bytes[3] is most-significant on this little-endian machine) --
    // proves the dump agrees with printf("%x") only when byte order is accounted
    // for, not read raw
    snprintf(dump, sizeof dump, "%02x%02x%02x%02x", // => co-11: writes 4 pairs of
                                                    // hex digits, MSB byte first
             bytes[3], bytes[2], bytes[1],
             bytes[0]); // => co-15: index order REVERSED vs storage -- undoes
                        // little-endian

    char reference[9]; // => co-11: the "ground truth" string from printf itself
    snprintf(reference, sizeof reference, "%08x",
             value); // => co-11: %x always prints in NUMERIC (big-endian-style) order

    printf("value            = 0x%08x\n",
           value);                                     // => co-11: the number as printf renders it
    printf("byte[3..0]       = %02x %02x %02x %02x\n", // => co-15: raw memory
                                                       // order, most-significant
                                                       // byte first here
           bytes[3], bytes[2], bytes[1], bytes[0]);
    printf("hand-built dump  = %s\n",
           dump); // => co-11: dump built from raw bytes, reordered by hand
    printf("printf(\"%%x\")     = %s\n",
           reference); // => co-11: dump built purely by printf's own formatting

    int match = strcmp(dump, reference) == 0; // => co-11: the assertion this example exists to check
    printf("%s\n",
           match // => co-11: prints PASS/FAIL based on that assertion
               ? "PASS: hand-built hex dump matches printf(\"%x\") exactly"
               : "FAIL: hand-built dump diverges from printf(\"%x\")");

    return match ? 0 : 1; // => co-11: nonzero exit on assertion failure
}
