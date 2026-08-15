// co-20 co-21: ? preserves the typed error through a call chain.
fn leaf(text: &str) -> Result<u8, std::num::ParseIntError> {
    Ok(text.parse()?)
}
fn middle(text: &str) -> Result<u8, std::num::ParseIntError> {
    Ok(leaf(text)? + 1)
}
fn main() {
    assert_eq!(middle("41"), Ok(42));
}
