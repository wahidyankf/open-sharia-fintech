// co-19 result-error: expected failure is a typed value.
fn parse(text: &str) -> Result<u32, &'static str> {
    text.parse().map_err(|_| "not a number")
}
fn main() {
    assert_eq!(parse("7"), Ok(7));
    assert_eq!(parse("x"), Err("not a number"));
}
