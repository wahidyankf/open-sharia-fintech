// co-19: a system boundary returns an error rather than indexing invalid input.
fn read(bytes: &[u8], index: usize) -> Result<u8, &'static str> {
    bytes.get(index).copied().ok_or("out of range")
}
fn main() {
    assert_eq!(read(&[], 0), Err("out of range"));
}
