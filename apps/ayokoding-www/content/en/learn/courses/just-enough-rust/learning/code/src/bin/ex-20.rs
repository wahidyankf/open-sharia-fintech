// Option represents presence or absence without null.
// match forces both cases to be considered.
fn main() {
    for value in [Some("up"), None] {
        println!(
            "{}",
            match value {
                Some(text) => text,
                None => "down",
            }
        );
    }
}
