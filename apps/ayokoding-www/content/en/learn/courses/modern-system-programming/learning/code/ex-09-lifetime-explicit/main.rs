// co-06: the returned reference lasts no longer than either input.
fn shorter<'a>(left: &'a str, right: &'a str) -> &'a str {
    if left.len() < right.len() {
        left
    } else {
        right
    }
}
fn main() {
    assert_eq!(shorter("one", "four"), "one");
}
