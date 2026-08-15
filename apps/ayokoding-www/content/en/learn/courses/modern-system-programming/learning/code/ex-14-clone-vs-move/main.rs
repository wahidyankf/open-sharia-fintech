// co-02: clone explicitly pays to retain two independently owned values.
fn main() {
    let original = String::from("copy me");
    let copy = original.clone();
    assert_eq!(original, "copy me");
    assert_eq!(copy, "copy me");
}
