// co-24: creating a raw pointer is safe; dereferencing it is not.
fn main() {
    let n = 7;
    let p: *const i32 = &n;
    assert!(!p.is_null());
}
