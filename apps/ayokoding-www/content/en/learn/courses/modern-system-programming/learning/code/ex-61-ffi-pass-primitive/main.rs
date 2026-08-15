// co-27 co-29: integer ABI values are copied, so no allocation ownership crosses.
mod export {
    #[unsafe(no_mangle)]
    pub extern "C" fn c_increment(n: u32) -> u32 {
        n + 1
    }
}
unsafe extern "C" {
    fn c_increment(n: u32) -> u32;
}
fn increment(n: u32) -> u32 {
    unsafe { c_increment(n) }
}
fn main() {
    assert_eq!(increment(41), 42);
}
