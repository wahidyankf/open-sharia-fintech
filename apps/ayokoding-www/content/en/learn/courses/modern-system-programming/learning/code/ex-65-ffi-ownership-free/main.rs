// co-29: the side that creates a CString retains and drops it after the call.
fn main() {
    let owned = std::ffi::CString::new("owned").unwrap();
    let pointer = owned.as_ptr();
    assert!(!pointer.is_null());
    drop(owned);
}
