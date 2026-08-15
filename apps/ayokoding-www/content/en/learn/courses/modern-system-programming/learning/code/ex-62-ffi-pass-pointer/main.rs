// co-29 co-24: the borrowed slice stays alive and nonempty during the C-ABI read.
mod export {
    #[unsafe(no_mangle)]
    pub extern "C" fn c_first(p: *const u8) -> u8 {
        unsafe { *p }
    }
}
unsafe extern "C" {
    fn c_first(p: *const u8) -> u8;
}
fn first(bytes: &[u8]) -> Option<u8> {
    bytes.first().map(|_| unsafe { c_first(bytes.as_ptr()) })
}
fn main() {
    assert_eq!(first(b"R"), Some(b'R'));
}
