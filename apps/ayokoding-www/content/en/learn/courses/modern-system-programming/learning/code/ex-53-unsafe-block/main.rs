// co-23 co-24: dereferencing a raw pointer needs an explicit unsafe proof boundary.
fn main() {
    let n = 42;
    let p = &n as *const i32;
    let read = unsafe { *p };
    assert_eq!(read, 42);
}
