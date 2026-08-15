// co-01 ownership-memory: a function may become the owner of its parameter.
fn consume(value: String) -> usize {
    value.len()
}
fn main() {
    assert_eq!(consume(String::from("transfer")), 8);
}
