// ? composes multiple fallible parsing steps.
// The first Err skips the remaining work.
fn sum(left: &str, right: &str) -> Result<u16, String> {
    Ok(left.parse::<u16>().map_err(|_| "left".to_string())?
        + right.parse::<u16>().map_err(|_| "right".to_string())?)
}
fn main() {
    println!("{:?} {:?}", sum("1", "2"), sum("x", "2"));
}
