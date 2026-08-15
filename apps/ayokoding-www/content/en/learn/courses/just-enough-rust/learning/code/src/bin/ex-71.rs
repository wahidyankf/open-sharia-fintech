// A unit test checks behavior beside executable code.
// cargo test discovers functions marked #[test].
fn double(value: u16) -> u16 {
    value * 2
}
fn main() {
    println!("{}", double(21));
}
#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn doubles() {
        assert_eq!(double(21), 42);
    }
}
