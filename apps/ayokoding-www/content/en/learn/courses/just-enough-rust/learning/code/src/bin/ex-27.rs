// String is not Copy, so assignment moves ownership.
// The destination becomes the sole usable owner.
fn main() {
    let request = String::from("GET");
    let moved = request;
    println!("{moved}");
}
