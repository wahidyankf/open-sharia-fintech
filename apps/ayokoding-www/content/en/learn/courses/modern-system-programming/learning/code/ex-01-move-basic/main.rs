// co-02 move-semantics: assigning a String transfers its single owner.
fn main() {
    let source = String::from("owned");
    let destination = source;
    assert_eq!(destination, "owned");
}
