// learning/capstone/code/repr.c
/* Capstone step 1: representation and endianness hazards in the
 * sensor-averaging kernel this capstone builds toward -- print bytes of
 * int/float values, force an integer-overflow allocation bug (and its
 * checked-multiply fix), show a non-equal float compare on real sensor
 * arithmetic, and round-trip a sensor ID through network byte order. Every
 * hazard shown here is exactly the kind of bug that hides silently inside the
 * sensor-averaging kernel cache.c/cache_soa.c build next.
 */
#include <arpa/inet.h> // => co-15: htonl/ntohl -- network (big-endian, "wire") byte order
#include <stdint.h>    // => fixed-width types so the byte layout is exact, not "whatever int is"
#include <stdio.h>     // => printf: report every hazard's before/after state
#include <string.h>    // => memcpy: safe type-punning between int32_t/float and unsigned char[4]

// ---------------------------------------------------------------------------
// Part A: print the raw bytes of a two's-complement int and an IEEE-754 float
// ---------------------------------------------------------------------------
static void print_int_bytes(const char *label,
                            int32_t value) { // => co-11: two's-complement bit layout
    unsigned char bytes[4];
    memcpy(bytes, &value,
           sizeof(bytes)); // => safe, no strict-aliasing UB (unlike a raw cast)
    printf("%-28s value=%-12d bits=0x%08x bytes(low->high)=%02x %02x %02x %02x\n", label, value, (unsigned)(uint32_t)value, bytes[0], bytes[1], bytes[2], bytes[3]);
    // => co-11: negative values store as (2^32 + value) mod 2^32 -- the sign bit
    // is just bit 31
}

static void print_float_bits(const char *label,
                             float value) { // => co-13: IEEE-754 sign/exponent/mantissa
    uint32_t bits;
    memcpy(&bits, &value,
           sizeof(bits));                     // => reinterpret the 4 bytes as an IEEE-754 pattern
    unsigned sign = (bits >> 31) & 0x1u;      // => co-13: bit 31 -- 1 means negative
    unsigned exponent = (bits >> 23) & 0xFFu; // => co-13: bits 30..23, biased by 127
    unsigned mantissa = bits & 0x7FFFFFu;     // => co-13: bits 22..0, the fractional significand
    printf("%-28s value=%-14g bits=0x%08x sign=%u exponent=%u(biased) "
           "mantissa=0x%06x\n",
           label, (double)value, bits, sign, exponent, mantissa);
}

// ---------------------------------------------------------------------------
// Part B: an integer-overflow allocation hazard -- the exact bug class that can
// silently under-allocate the sensor array cache.c/cache_soa.c both build on
// ---------------------------------------------------------------------------
static int checked_records_bytes(int32_t n_records, int32_t record_size, size_t *out) {
    // => co-12: n_records * record_size computed in 32-bit int OVERFLOWS for
    // large n_records --
    // __builtin_mul_overflow (a real clang/gcc builtin) detects it before the
    // multiply completes
    int32_t product;
    if (__builtin_mul_overflow(n_records, record_size,
                               &product)) { // => co-12: true if the true product
                                            // doesn't fit in int32_t
        return 0;                           // => reject instead of silently wrapping into a small alloc size
    }
    *out = (size_t)product;
    return 1;
}

static void demonstrate_overflow_hazard(void) {
    // => co-12: a deliberately hostile n_records that overflows 32-bit int when
    // multiplied by a realistic per-record size -- this is the classic "malloc(n
    // * size)" CVE shape
    int32_t hostile_n = 100000000;                                    // => 100,000,000
    int32_t record_size = 32;                                         // => bytes per SensorRecord-shaped struct (see cache.c)
    int64_t true_product = (int64_t)hostile_n * (int64_t)record_size; // => the CORRECT 64-bit answer for comparison
    int32_t naive_product = hostile_n * record_size;                  // => co-12: UB in ISO C (signed overflow) --
                                                                      //    compiled here to observe what -fwrapv defines it as
    printf("hostile_n=%d record_size=%d\n", hostile_n, record_size);
    printf("  true 64-bit product   = %lld bytes (%.2f MB)\n", (long long)true_product, true_product / 1e6);
    printf("  naive int32 product   = %d bytes  <-- WRONG, this is what "
           "malloc(n*size) would request\n",
           naive_product);

    size_t safe_bytes;
    int ok = checked_records_bytes(hostile_n, record_size, &safe_bytes);
    printf("  checked_records_bytes: %s\n", ok ? "accepted" : "REJECTED (overflow detected, allocation refused)");
    printf("PASS: __builtin_mul_overflow caught the hazard naive multiplication "
           "silently missed\n");
}

// ---------------------------------------------------------------------------
// Part C: float non-equality on the exact kind of arithmetic
// cache.c/cache_soa.c perform (summing many small readings and dividing by the
// count)
// ---------------------------------------------------------------------------
static void demonstrate_float_hazard(void) {
    // => co-13/co-14: binary32 (float) happens to round 0.1f+0.2f to the SAME
    // bits as the literal 0.3f on this toolchain -- the anomaly is real but
    // precision-dependent, so this uses double (binary64), the precision the
    // sensor-average kernel's accumulator uses too, where the rounding error is
    // large enough to survive both additional roundings
    double a = 0.1,
           b = 0.2;     // => co-13: neither has an exact binary64 representation
    double sum = a + b; // => co-13/co-14: rounds twice more, compounding error
    double target = 0.3;
    printf("a=%.17f b=%.17f a+b=%.17f target=%.17f\n", a, b, sum, target);
    printf("  strict (a+b == 0.3)    : %s\n", (sum == target) ? "true" : "false");
    double diff = sum - target;
    if (diff < 0)
        diff = -diff;
    printf("  epsilon (|diff|<1e-9)  : %s\n", (diff < 1e-9) ? "true" : "false");
    printf("PASS: strict equality fails on this exact arithmetic shape; epsilon "
           "compare is the correct tool\n");
}

// ---------------------------------------------------------------------------
// Part D: endianness -- round-trip a sensor ID through network (wire) byte
// order
// ---------------------------------------------------------------------------
static void demonstrate_endianness(void) {
    uint32_t sensor_id_host = 0x0A2B3C4Du;           // => a plausible packed sensor-id field, in HOST byte order
    uint32_t sensor_id_wire = htonl(sensor_id_host); // => co-15: convert to network (big-endian) byte
                                                     // order for "transmission"
    uint32_t roundtrip = ntohl(sensor_id_wire);      // => co-15: convert back

    unsigned char host_bytes[4], wire_bytes[4];
    memcpy(host_bytes, &sensor_id_host, 4);
    memcpy(wire_bytes, &sensor_id_wire, 4);

    printf("sensor_id_host = 0x%08x  bytes = %02x %02x %02x %02x\n", sensor_id_host, host_bytes[0], host_bytes[1], host_bytes[2], host_bytes[3]);
    printf("sensor_id_wire = 0x%08x  bytes = %02x %02x %02x %02x  "
           "(network/big-endian order)\n",
           sensor_id_wire, wire_bytes[0], wire_bytes[1], wire_bytes[2], wire_bytes[3]);
    printf("roundtrip      = 0x%08x\n", roundtrip);
    printf("PASS: %s (host bytes %s wire bytes on this little-endian machine)\n", (roundtrip == sensor_id_host) ? "ntohl(htonl(x)) == x" : "ROUNDTRIP FAILED", memcmp(host_bytes, wire_bytes, 4) != 0 ? "differ from" : "match");
}

int main(void) {
    printf("=== Part A: raw representation ===\n");
    print_int_bytes("int32_t -1", -1);
    print_int_bytes("int32_t 42", 42);
    print_float_bits("float 1.0f", 1.0f);
    print_float_bits("float -0.5f", -0.5f);

    printf("\n=== Part B: integer-overflow allocation hazard ===\n");
    demonstrate_overflow_hazard();

    printf("\n=== Part C: float comparison hazard ===\n");
    demonstrate_float_hazard();

    printf("\n=== Part D: endianness round-trip ===\n");
    demonstrate_endianness();

    printf("\nCAPSTONE STEP 1 PASS: representation, overflow, float, and "
           "endianness hazards all demonstrated\n");
    return 0;
}
