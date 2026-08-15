// co-21 custom-errors: an enum preserves machine-readable failure cases.
#[derive(Debug, PartialEq)]
enum ReadError {
    Empty,
}
fn read(text: &str) -> Result<&str, ReadError> {
    if text.is_empty() {
        Err(ReadError::Empty)
    } else {
        Ok(text)
    }
}
fn main() {
    assert_eq!(read(""), Err(ReadError::Empty));
}
