// co-28: the 2024 edition requires unsafe(no_mangle) when exporting a C-visible symbol.
#[unsafe(no_mangle)]
pub extern "C" fn exported_answer() -> i32 {
    42
}
fn main() {
    assert_eq!(exported_answer(), 42);
}
