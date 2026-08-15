// A larger unit test checks an ordinary Result-returning function.
// cargo test --bin ex-77 exercises both cases.
fn port(text: &str) -> Result<u16, String> {
    text.parse().map_err(|_| "invalid".into())
}
fn main() {
    println!("{:?}", port("443"));
}
#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn accepts_port() {
        assert_eq!(port("443"), Ok(443));
    }
    #[test]
    fn rejects_text() {
        assert!(port("x").is_err());
    }
}
