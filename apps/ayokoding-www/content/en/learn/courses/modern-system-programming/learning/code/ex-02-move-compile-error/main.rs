// co-02: `let again = source;` after the move below is rejected; use destination instead.
fn main() {
    let source = String::from("moved");
    let destination = source;
    assert_eq!(destination, "moved");
}
