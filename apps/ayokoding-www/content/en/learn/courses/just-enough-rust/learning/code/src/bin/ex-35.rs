// This lifetime says the result borrows one input.
// The returned slice cannot outlive both inputs.
fn longest<'a>(left: &'a str, right: &'a str) -> &'a str {
    if left.len() >= right.len() {
        left
    } else {
        right
    }
}
fn main() {
    println!("{}", longest("api", "worker"));
}
