// co-03: borrowing lets a function inspect while the caller retains ownership.
fn size(value: &str) -> usize {
    value.len()
}
fn main() {
    let value = String::from("retain");
    assert_eq!(size(&value), 6);
    assert_eq!(value, "retain");
}
