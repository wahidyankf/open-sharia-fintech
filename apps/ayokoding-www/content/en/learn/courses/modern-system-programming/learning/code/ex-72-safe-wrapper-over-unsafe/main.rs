// co-25 co-29: safe callers cannot supply a null pointer; the wrapper owns the invariant.
fn byte_at(bytes: &[u8], index: usize) -> Option<u8> {
    bytes
        .get(index)
        .map(|value| unsafe { *(value as *const u8) })
}
fn main() {
    assert_eq!(byte_at(b"ok", 1), Some(b'k'));
}
