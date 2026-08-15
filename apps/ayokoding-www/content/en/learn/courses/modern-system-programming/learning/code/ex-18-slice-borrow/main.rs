// co-03: a slice borrows a contiguous view of Vec-owned elements.
fn main() {
    let values = vec![2, 3, 5];
    let view = &values[1..];
    assert_eq!(view, [3, 5]);
    assert_eq!(values[0], 2);
}
