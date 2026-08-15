// co-08 box: Box owns a heap allocation and dereferences safely.
fn main() {
    let number = Box::new(41);
    assert_eq!(*number + 1, 42);
}
