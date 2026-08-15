// co-19: Cargo tests check behavior separately; `cargo test --bin ex-75-cargo-test-suite` is valid.
fn square(n: i32) -> i32 {
    n * n
}
fn main() {
    assert_eq!(square(6), 36);
}
#[cfg(test)]
mod tests {
    use super::square;
    #[test]
    fn squares() {
        assert_eq!(square(6), 36);
    }
}
