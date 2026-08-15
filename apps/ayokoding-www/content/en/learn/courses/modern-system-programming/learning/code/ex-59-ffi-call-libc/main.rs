// co-27 co-26: a C-ABI function can be safely wrapped, avoiding a platform-specific libc dependency.
mod export {
    #[unsafe(no_mangle)]
    pub extern "C" fn c_abs(n: i32) -> i32 {
        n.abs()
    }
}
unsafe extern "C" {
    fn c_abs(n: i32) -> i32;
}
fn abs(n: i32) -> i32 {
    unsafe { c_abs(n) }
}
fn main() {
    assert_eq!(abs(-42), 42);
}
