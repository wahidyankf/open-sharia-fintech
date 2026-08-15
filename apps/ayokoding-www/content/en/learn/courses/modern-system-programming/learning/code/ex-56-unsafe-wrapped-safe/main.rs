// co-25: the safe API establishes the pointer validity contract before the tiny unsafe block.
fn first(values: &[i32]) -> Option<i32> {
    values.first().map(|v| unsafe { *(v as *const i32) })
}
fn main() {
    assert_eq!(first(&[42]), Some(42));
}
