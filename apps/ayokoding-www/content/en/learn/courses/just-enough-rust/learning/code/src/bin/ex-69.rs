// Borrow a string to compute a separate owned result.
// The return value does not borrow the input.
fn label(path: &str) -> String {
    format!("endpoint:{path}")
}
fn main() {
    let path = String::from("/health");
    println!("{} {path}", label(&path));
}
