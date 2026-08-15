//! Step 4: C ABI boundary. The wrapper has no pointer ownership to transfer.

unsafe extern "C" {
    fn c_double(value: i32) -> i32;
}

/// Doubles a copied i32 through the C ABI.
///
/// Safety: `i32` is passed by value, `c_double` has the declared C ABI, and the linked C function
/// has no side effects or ownership transfer. This is the sole audited unsafe operation.
pub fn double(value: i32) -> i32 {
    unsafe { c_double(value) }
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn safely_calls_c() {
        assert_eq!(double(21), 42);
    }
}
