// co-26: this definition has the C ABI and can be called through an extern declaration.
mod export {
    #[unsafe(no_mangle)]
    pub extern "C" fn rust_add(a: i32, b: i32) -> i32 {
        a + b
    }
}
unsafe extern "C" {
    fn rust_add(a: i32, b: i32) -> i32;
}
fn main() {
    assert_eq!(unsafe { rust_add(20, 22) }, 42);
}
