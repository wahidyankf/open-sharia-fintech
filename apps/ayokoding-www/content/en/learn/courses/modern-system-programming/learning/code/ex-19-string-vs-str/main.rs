// co-03: String owns bytes; &str borrows a UTF-8 view of them.
fn main() {
    let owned = String::from("Rust");
    let borrowed: &str = &owned;
    assert_eq!(borrowed, "Rust");
}
