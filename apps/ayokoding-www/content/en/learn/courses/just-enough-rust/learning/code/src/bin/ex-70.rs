// This generic accepts any Display value.
// Result carries validation failure without a panic.
fn required<T: std::fmt::Display>(value: Option<T>) -> Result<String, String> {
    Ok(value.ok_or("missing")?.to_string())
}
fn main() {
    println!("{:?} {:?}", required(Some(443)), required::<u16>(None));
}
