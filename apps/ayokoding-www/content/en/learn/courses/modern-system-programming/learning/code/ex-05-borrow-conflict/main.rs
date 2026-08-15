// co-05 borrow-rules: end the shared borrow before forming the exclusive borrow.
fn main() {
    let mut value = String::from("a");
    assert_eq!((&value).len(), 1);
    (&mut value).push('b');
    assert_eq!(value, "ab");
}
