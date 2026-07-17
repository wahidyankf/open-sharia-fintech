// learning/code/ex-12-htonl-roundtrip/htonl_roundtrip.c
/* Example 12: htonl Roundtrip -- host<->network byte order, and the on-wire
 * bytes differ. */

#include <arpa/inet.h> // => co-15: htonl/ntohl -- POSIX host<->network (big-endian) byte-order conversion
#include <stdint.h>    // => co-15: uint32_t -- the fixed-width value being converted
#include <stdio.h>     // => co-15: printf -- reports host value, wire bytes, and the round-tripped result

int main(void) {                       // program entry point
    uint32_t host_value = 0x11223344u; // => co-15: same recognizable value used
                                       // in ex-01, for continuity

    uint32_t wire_value = htonl(host_value); // => co-15: converts to NETWORK byte
                                             // order (always big-endian)
    uint32_t roundtrip = ntohl(wire_value);  // => co-15: converts back -- should
                                             // exactly restore host_value

    unsigned char *host_bytes = (unsigned char *)&host_value; // => co-15: raw storage bytes of the HOST-order value
    unsigned char *wire_bytes = (unsigned char *)&wire_value; // => co-15: raw storage bytes of the WIRE-order value

    printf("host_value       = 0x%08x\n",
           host_value);                                // => co-15: the original value
    printf("host bytes       = %02x %02x %02x %02x\n", // => co-15: little-endian
                                                       // storage on THIS host
           host_bytes[0], host_bytes[1], host_bytes[2],
           host_bytes[3]); // supporting statement for this example
    printf("wire_value       = 0x%08x (as a host-order int)\n",
           wire_value);                                // => co-15: htonl's raw 32-bit result
    printf("wire bytes       = %02x %02x %02x %02x\n", // => co-15: the bytes that
                                                       // would actually go ON THE
                                                       // WIRE
           wire_bytes[0], wire_bytes[1], wire_bytes[2],
           wire_bytes[3]); // supporting statement for this example
    printf("roundtrip        = 0x%08x\n",
           roundtrip); // => co-15: ntohl(htonl(x)) -- should equal host_value

    // ex-12: two independent claims -- (1) the roundtrip is lossless, and (2) the
    // WIRE bytes genuinely differ from the HOST bytes on this little-endian
    // machine (network byte order is always big-endian, per RFC 1700 and every
    // BSD sockets API)
    int roundtrip_ok = (roundtrip == host_value);                           // => co-15: identity claim
    int bytes_differ =                                                      // => co-15: the wire representation is NOT the host one
        host_bytes[0] != wire_bytes[0] || host_bytes[1] != wire_bytes[1] || // supporting statement for this example
        host_bytes[2] != wire_bytes[2] || host_bytes[3] != wire_bytes[3];   // supporting statement for this example
    int correct = roundtrip_ok && bytes_differ;                             // => co-15: both halves of the claim must hold
    printf("%s\n",
           correct // => co-15: PASS/FAIL verdict
               ? "PASS: ntohl(htonl(x)) == x, and wire bytes differ from host "
                 "bytes"                                                 // supporting statement for this example
               : "FAIL: roundtrip or byte-difference assertion failed"); // supporting
                                                                         // statement
                                                                         // for
                                                                         // this
                                                                         // example

    return correct ? 0 : 1; // => co-15: nonzero exit on assertion failure
}
