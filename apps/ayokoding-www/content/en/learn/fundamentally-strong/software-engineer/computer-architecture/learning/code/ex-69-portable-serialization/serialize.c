// learning/code/ex-69-portable-serialization/serialize.c
/* Example 69: byte-order-explicit serialization -- portable regardless of host
 * endianness. */
#include <stdint.h> // stdint.h: standard library header
#include <stdio.h>  // stdio.h: standard library header
#include <string.h> // string.h: standard library header

// ex-69: a record with fields a naive `memcpy(&r, buf, sizeof(r))` would get
// WRONG in two independent ways: co-16 struct padding (compiler-inserted bytes
// with unspecified content differ across compilers/hosts) and co-15 endianness
// (the multi-byte fields' byte order depends on the host CPU) -- this example
// serializes field-by-field with explicit shifts instead, sidestepping BOTH.
typedef struct {   // struct layout definition
    uint32_t id;   // => 4-byte field
    int16_t score; // => 2-byte SIGNED field -- byte-packed via its uint16_t bit
                   // pattern
    uint8_t flag;  // => 1-byte field
} Record;          // wire format below is exactly 7 bytes -- no padding, because we
                   // never serialize sizeof(Record) raw bytes, only the fields, one
                   // explicit byte at a time

#define WIRE_BYTES 7 // => 4 + 2 + 1 -- the record's TRUE information content, with zero padding

// ex-69: BIG-ENDIAN (network byte order) wire encoding -- co-15:
// most-significant byte first, written with explicit shifts (`>> 24`, `>> 16`,
// ...) that behave IDENTICALLY no matter what endianness the HOST CPU itself
// uses, because shifting an integer is a value-level operation, not a
// memory-layout operation.
static void serialize_be(Record r,
                         uint8_t *buf) { // defines serialize_be(): helper
                                         // function used by this example
    buf[0] = (uint8_t)(r.id >> 24);      // => co-15: most-significant byte of id, written FIRST
    buf[1] = (uint8_t)(r.id >> 16);      // assigns buf[1]
    buf[2] = (uint8_t)(r.id >> 8);       // assigns buf[2]
    buf[3] = (uint8_t)(r.id);            // => co-15: least-significant byte of id, written LAST
    uint16_t s = (uint16_t)r.score;      // => co-15/co-11: reinterpret the signed value's bit pattern
    buf[4] = (uint8_t)(s >> 8);          // assigns buf[4]
    buf[5] = (uint8_t)(s);               // assigns buf[5]
    buf[6] = r.flag;                     // assigns buf[6]
}

static Record deserialize_be(const uint8_t *buf) { // defines deserialize_be(): helper
                                                   // function used by this example
    Record r;                                      // declares r
    // co-15: reassemble MSB-first -- this is the exact inverse of serialize_be,
    // and it too never depends on the CALLING host's endianness, only on the byte
    // SEQUENCE it is handed.
    r.id = ((uint32_t)buf[0] << 24) | ((uint32_t)buf[1] << 16) | ((uint32_t)buf[2] << 8) | (uint32_t)buf[3]; // assigns r.id
    uint16_t s = (uint16_t)(((uint16_t)buf[4] << 8) | (uint16_t)buf[5]);                                     // declares s
    r.score = (int16_t)s;                                                                                    // assigns r.score
    r.flag = buf[6];                                                                                         // assigns r.flag
    return r;                                                                                                // returns the computed result
}

// ex-69: LITTLE-ENDIAN wire encoding -- the mirror-image convention (x86/ARM's
// native in-register byte order, and many binary file formats). Included to
// prove the round trip holds for BOTH byte orders, not just network byte order
// -- co-15's whole point is that the choice is a CONVENTION.
static void serialize_le(Record r,
                         uint8_t *buf) { // defines serialize_le(): helper
                                         // function used by this example
    buf[0] = (uint8_t)(r.id);            // => co-15: least-significant byte of id, written FIRST
    buf[1] = (uint8_t)(r.id >> 8);       // assigns buf[1]
    buf[2] = (uint8_t)(r.id >> 16);      // assigns buf[2]
    buf[3] = (uint8_t)(r.id >> 24);      // => co-15: most-significant byte of id, written LAST
    uint16_t s = (uint16_t)r.score;      // declares s
    buf[4] = (uint8_t)(s);               // assigns buf[4]
    buf[5] = (uint8_t)(s >> 8);          // assigns buf[5]
    buf[6] = r.flag;                     // assigns buf[6]
}

static Record deserialize_le(const uint8_t *buf) {                                                           // defines deserialize_le(): helper
                                                                                                             // function used by this example
    Record r;                                                                                                // declares r
    r.id = (uint32_t)buf[0] | ((uint32_t)buf[1] << 8) | ((uint32_t)buf[2] << 16) | ((uint32_t)buf[3] << 24); // assigns r.id
    uint16_t s = (uint16_t)((uint16_t)buf[4] | ((uint16_t)buf[5] << 8));                                     // declares s
    r.score = (int16_t)s;                                                                                    // assigns r.score
    r.flag = buf[6];                                                                                         // assigns r.flag
    return r;                                                                                                // returns the computed result
}

static int records_equal(Record a,
                         Record b) {                               // defines records_equal(): helper function used by this example
    return a.id == b.id && a.score == b.score && a.flag == b.flag; // => field-by-field, not memcmp of
} // raw struct bytes (co-16: padding
  // bytes have unspecified content)

int main(void) {                                   // program entry point
    Record original = {0x01020304u, -12345, 0xAB}; // => co-15: id's bytes are all distinct, easy to eyeball

    uint8_t wire_be[WIRE_BYTES];     // declares wire_be
    uint8_t wire_le[WIRE_BYTES];     // declares wire_le
    serialize_be(original, wire_be); // calls serialize_be(...)
    serialize_le(original, wire_le); // calls serialize_le(...)

    printf("original: id=0x%08X score=%d flag=0x%02X\n", original.id, original.score, original.flag);        // prints a report line
    printf("BE wire bytes: %02X %02X %02X %02X %02X %02X %02X  (MSB of id FIRST)\n", wire_be[0], wire_be[1], // prints a report line
           wire_be[2], wire_be[3], wire_be[4], wire_be[5],
           wire_be[6]);                                                                                      // continues the printf(...) call above
    printf("LE wire bytes: %02X %02X %02X %02X %02X %02X %02X  (LSB of id FIRST)\n", wire_le[0], wire_le[1], // prints a report line
           wire_le[2], wire_le[3], wire_le[4], wire_le[5],
           wire_le[6]); // continues the printf(...) call above

    // co-15: the two encodings of the SAME record must byte-for-byte differ in
    // the multi-byte fields (id and score), proving this isn't accidentally
    // producing identical output.
    int be_differs_from_le = memcmp(wire_be, wire_le, WIRE_BYTES) != 0; // declares be_differs_from_le

    Record round_be = deserialize_be(wire_be);               // declares round_be
    Record round_le = deserialize_le(wire_le);               // declares round_le
    int be_roundtrip_ok = records_equal(original, round_be); // declares be_roundtrip_ok
    int le_roundtrip_ok = records_equal(original, round_le); // declares le_roundtrip_ok

    // co-15: the ULTIMATE portability check -- decode BE-encoded bytes with the
    // BE decoder (correct wire-format-to-decoder pairing) and confirm it recovers
    // the record on THIS host, which is little-endian (verified: this Apple
    // Silicon dev machine is little-endian) -- an explicit byte-order decoder
    // gets the right answer on ANY host, unlike a raw `memcpy` reinterpret cast,
    // which would only happen to work when the host's native order matches the
    // wire format's order.
    printf("\nBE round-trip (serialize_be -> deserialize_be): %s\n",
           be_roundtrip_ok ? "OK" : "MISMATCH"); // prints a report line
    printf("LE round-trip (serialize_le -> deserialize_le): %s\n",
           le_roundtrip_ok ? "OK" : "MISMATCH"); // prints a report line
    printf("BE and LE wire encodings differ (as expected): %s\n",
           be_differs_from_le ? "yes" : "NO -- BUG"); // prints a report line

    int pass = be_roundtrip_ok && le_roundtrip_ok && be_differs_from_le; // declares pass
    printf("PASS (round-trip holds on BOTH byte orders, and the two wire formats "
           "are genuinely\n"); // prints a report line
    printf(" different byte sequences): %s\n",
           pass ? "PASS" : "FAIL"); // prints a report line
    return 0;                       // returns the computed result
}
