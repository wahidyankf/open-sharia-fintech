// Option::map transforms only a present value.
// None passes through unchanged.
fn main() {
    let port = Some(443);
    println!("{:?}", port.map(|value| value + 1));
}
