// &String creates a shared borrow instead of a move.
// The owner remains available after the call.
fn length(text: &str) -> usize {
    text.len()
}
fn main() {
    let path = String::from("/health");
    println!("{} {path}", length(&path));
}
