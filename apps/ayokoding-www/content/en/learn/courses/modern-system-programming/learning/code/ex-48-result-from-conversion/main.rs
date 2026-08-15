// co-20 co-21: From supplies the conversion that ? uses on an error path.
#[derive(Debug, PartialEq)]
struct AppError;
impl From<std::num::ParseIntError> for AppError {
    fn from(_: std::num::ParseIntError) -> Self {
        Self
    }
}
fn parse(text: &str) -> Result<u8, AppError> {
    Ok(text.parse()?)
}
fn main() {
    assert_eq!(parse("x"), Err(AppError));
}
