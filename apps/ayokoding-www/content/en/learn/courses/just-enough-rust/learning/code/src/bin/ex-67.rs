// Nested matches distinguish absence from a parse failure.
// Each branch chooses an explicit outcome.
fn main() {
    let input = Some("x");
    println!(
        "{}",
        match input.map(str::parse::<u16>) {
            Some(Ok(port)) => port.to_string(),
            Some(Err(_)) => "invalid".into(),
            None => "missing".into(),
        }
    );
}
