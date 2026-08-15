// co-06 lifetimes: the input reference lifetime is elided in this common shape.
fn first(text: &str) -> &str {
    &text[..1]
}
fn main() {
    assert_eq!(first("rust"), "r");
}
