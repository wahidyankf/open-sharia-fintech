// ? returns an Err early from this function.
// A successful value continues to the next expression.
fn doubled(text: &str) -> Result<u16, String> {
    Ok(text.parse::<u16>().map_err(|_| "bad".to_string())? * 2)
}
fn main() {
    println!("{:?} {:?}", doubled("21"), doubled("x"));
}
