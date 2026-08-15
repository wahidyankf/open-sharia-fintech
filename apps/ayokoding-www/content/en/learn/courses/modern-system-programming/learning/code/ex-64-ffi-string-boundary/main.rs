// co-29: CString owns the terminator; CStr only borrows the C representation.
fn main() {
    let owned = std::ffi::CString::new("rust").unwrap();
    let view = owned.as_c_str();
    assert_eq!(view.to_str().unwrap(), "rust");
}
