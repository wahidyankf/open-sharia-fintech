// co-23 co-24: p originates from a valid reference and n lives through the read.
fn main() {
    let n = 9;
    let p = &n as *const i32;
    assert_eq!(unsafe { *p }, 9);
}
