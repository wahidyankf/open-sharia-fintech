// Result makes success and failure explicit in the type.
// match handles both outcomes.
fn port(text: &str) -> Result<u16, String> {
    text.parse().map_err(|_| "invalid port".into())
}
fn main() {
    for text in ["443", "no"] {
        println!("{:?}", port(text));
    }
}
