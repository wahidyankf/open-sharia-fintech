// co-21: third-party derives are optional; a small error can implement Display directly.
#[derive(Debug)]
struct InputError;
impl std::fmt::Display for InputError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "invalid input")
    }
}
fn main() {
    assert_eq!(InputError.to_string(), "invalid input");
}
