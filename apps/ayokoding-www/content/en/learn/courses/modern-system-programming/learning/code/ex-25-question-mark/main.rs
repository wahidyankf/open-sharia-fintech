// co-19 co-20: ? returns early on Err and unwraps Ok locally.
fn doubled(text: &str) -> Result<u32, std::num::ParseIntError> {
    Ok(text.parse::<u32>()? * 2)
}
fn main() {
    assert_eq!(doubled("21"), Ok(42));
}
