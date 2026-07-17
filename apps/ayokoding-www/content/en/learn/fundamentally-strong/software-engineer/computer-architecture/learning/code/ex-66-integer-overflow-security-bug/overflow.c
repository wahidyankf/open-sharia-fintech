// learning/code/ex-66-integer-overflow-security-bug/overflow.c
/* Example 66: an allocation-size integer overflow, then the checked-multiply
 * fix. */
#include <stdint.h> // => uint32_t: the exact 32-bit width real CVE-class allocation bugs use
#include <stdio.h>  // stdio.h: standard library header
#include <stdlib.h> // stdlib.h: standard library header

// ex-66: a "record" a real system might allocate N of, from an
// attacker/user-controlled count (e.g., a length field parsed off the network
// or a file header).
typedef struct {
    unsigned char payload[64];
} Record; // sizeof(Record) == 64 bytes

// ex-66: THE VULNERABLE PATTERN -- `n` and `elem_size` are both `uint32_t` (the
// classic shape: a 32-bit "count" field read straight from an untrusted
// format), multiplied in `uint32_t` BEFORE ever reaching `malloc`. co-12:
// unsigned multiplication overflow is STANDARDS-DEFINED wraparound modulo 2^32
// (not UB) -- so this function's bug is fully reproducible, not undefined
// behavior; the danger is not the wraparound arithmetic itself but trusting its
// result as an allocation size.
static void *alloc_records_vulnerable(uint32_t n, uint32_t elem_size,
                                      uint32_t *out_total) { // defines alloc_records_vulnerable(): helper
                                                             // function used by this example
    uint32_t total = n * elem_size;                          // => co-12: DEFINED wraparound mod 2^32 --
                                                             // computed here, not UB
    *out_total = total;                                      // => hand the (possibly wrapped) size back so main() can
                                                             // inspect it
    return malloc(total);                                    // => co-12: malloc receives a size_t WIDENED FROM the
                                                             // already-wrapped total --
} // widening happens too late to recover the bits that were already lost

// ex-66: THE FIX -- `__builtin_mul_overflow` (a real clang/GCC builtin,
// verified compiling here) does the SAME `uint32_t * uint32_t` multiply but
// reports whether it wrapped, so the caller can REJECT the allocation instead
// of silently under-allocating and letting a later write walk off the buffer.
static void *alloc_records_checked(uint32_t n, uint32_t elem_size, uint32_t *out_total,
                                   int *overflowed) { // defines alloc_records_checked():
                                                      // helper function used by this example
    uint32_t total;                                   // declares total
    *overflowed = __builtin_mul_overflow(n, elem_size,
                                         &total); // => co-12: returns nonzero iff n*elem_size wrapped
    *out_total = total;                           // => report the (possibly meaningless, if overflowed)
                                                  // 32-bit product too
    if (*overflowed) {                            // declares function pointer overflowed
        return NULL;                              // => co-12: REFUSE the allocation -- no under-sized buffer is
                                                  // ever handed back
    }
    return malloc(total); // => co-12: only reached when the multiply is PROVEN
                          // not to have wrapped
}

int main(void) { // program entry point
    // ex-66: chosen so n * elem_size crosses 2^32 by exactly 64 -- 67108865 * 64
    // = 4294967360 = 2^32 + 64, so the 32-bit product wraps down to just 64 -- a
    // dramatic, exactly-reproducible case.
    uint32_t n_evil = 67108865u;                   // => attacker-controlled "record count"
    uint32_t elem_size = (uint32_t)sizeof(Record); // => 64, a fixed, trusted constant
    // co-12: the CORRECT byte count, computed in 64-bit size_t arithmetic where
    // it does NOT overflow -- this is the number of bytes the vulnerable path
    // SHOULD have allocated to be safe.
    size_t correct_bytes = (size_t)n_evil * (size_t)elem_size; // declares correct_bytes

    printf("scenario: n=%u records of %u bytes each (attacker-controlled n)\n", n_evil, elem_size); // prints a report line
    printf("correct byte count (64-bit size_t, no overflow): %zu bytes (%.2f MB)\n",
           correct_bytes,                              // prints a report line
           (double)correct_bytes / (1024.0 * 1024.0)); // continues the printf(...) call above

    uint32_t vuln_total = 0; // declares vuln_total
    void *vuln_buf = alloc_records_vulnerable(n_evil, elem_size,
                                              &vuln_total);                                                 // declares vuln_buf
    printf("\nvulnerable path: uint32_t total = %u bytes (WRAPPED from %zu)\n", vuln_total, correct_bytes); // prints a report line
    printf("  malloc(%u) %s -- caller BELIEVES it can write %u records of %u "
           "bytes into this buffer,\n", // prints a report line
           vuln_total, vuln_buf ? "succeeded" : "failed", n_evil,
           elem_size); // continues the printf(...) call above
    printf("  but the buffer is only %u bytes -- every write past record 1 is a "
           "heap buffer overflow\n", // prints a report line
           vuln_total);              // continues the printf(...) call above

    int overflowed = 0;                                                                        // declares overflowed
    uint32_t checked_total = 0;                                                                // declares checked_total
    void *checked_buf = alloc_records_checked(n_evil, elem_size, &checked_total, &overflowed); // declares checked_buf
    printf("\nchecked path (__builtin_mul_overflow): overflow detected=%s, "
           "allocation=%s\n", // prints a report line
           overflowed ? "yes" : "no",
           checked_buf ? "proceeded" : "REFUSED"); // continues the printf(...) call above

    // ex-66: a second, NON-overflowing call proves the checked path is not just
    // "always refuse" -- it allocates normally whenever the multiply genuinely
    // does not wrap.
    uint32_t n_ok = 1000u; // declares n_ok
    int overflowed_ok = 0; // declares overflowed_ok
    uint32_t ok_total = 0; // declares ok_total
    void *ok_buf = alloc_records_checked(n_ok, elem_size, &ok_total,
                                         &overflowed_ok); // declares ok_buf
    printf("\nsanity case: n=%u (no overflow) -> checked total=%u bytes, "
           "overflow=%s, allocation=%s\n", // prints a report line
           n_ok, ok_total, overflowed_ok ? "yes" : "no",
           ok_buf ? "proceeded" : "REFUSED"); // continues the printf(...) call above

    int pass = (vuln_total == 64) &&                                                       // the exact predicted wrapped value (see comment above)
               (overflowed == 1) && (checked_buf == NULL) &&                               // checked path correctly REJECTED the bad case
               (overflowed_ok == 0) && (ok_buf != NULL) && (ok_total == n_ok * elem_size); // and allowed the good one
    printf("\nPASS (vulnerable path under-allocated to exactly %u bytes; checked "
           "path rejected the\n", // prints a report line
           vuln_total);           // continues the printf(...) call above
    printf(" overflowing request and still allocated normally for the "
           "non-overflowing one): %s\n", // prints a report line
           pass ? "PASS" : "FAIL");      // continues the printf(...) call above

    free(vuln_buf);    // releases vuln_buf's heap memory
    free(checked_buf); // => NULL here -- free(NULL) is a well-defined no-op
    free(ok_buf);      // releases ok_buf's heap memory
    return 0;          // returns the computed result
}
