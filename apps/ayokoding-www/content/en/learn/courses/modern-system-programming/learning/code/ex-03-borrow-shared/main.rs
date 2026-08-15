// co-03 borrow-shared: a shared reference reads without taking ownership.
fn main() {
    let value = String::from("read");
    let view = &value;
    assert_eq!(view.len(), 4);
    assert_eq!(value, "read");
}
