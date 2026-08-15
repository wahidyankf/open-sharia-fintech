// A guard adds a condition to a pattern arm.
// The fallback keeps the match exhaustive.
fn main() {
    let code = 503;
    println!(
        "{}",
        match code {
            n if n >= 500 => "server",
            _ => "other",
        }
    );
}
