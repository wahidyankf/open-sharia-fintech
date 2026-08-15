// co-01 co-07: Vec owns each String and drops them with the Vec.
fn main() {
    let values = vec![String::from("a"), String::from("b")];
    assert_eq!(values.join(""), "ab");
}
