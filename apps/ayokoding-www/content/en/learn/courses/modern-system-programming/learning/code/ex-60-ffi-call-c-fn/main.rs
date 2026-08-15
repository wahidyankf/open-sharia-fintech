// co-27: the ABI declaration isolates the unchecked call site.
mod export {
    #[unsafe(no_mangle)]
    pub extern "C" fn c_double(n: i32) -> i32 {
        n * 2
    }
}
unsafe extern "C" {
    fn c_double(n: i32) -> i32;
}
fn double(n: i32) -> i32 {
    unsafe { c_double(n) }
}
fn main() {
    assert_eq!(double(21), 42);
}
