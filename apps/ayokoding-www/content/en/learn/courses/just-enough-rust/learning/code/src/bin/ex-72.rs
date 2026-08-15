// assert_eq! compares actual and expected values.
// A mismatch makes the test fail clearly.
fn secure(port: u16) -> bool {
    port == 443
}
fn main() {
    println!("{}", secure(443));
}
#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn recognizes_https() {
        assert_eq!(secure(443), true);
    }
}
