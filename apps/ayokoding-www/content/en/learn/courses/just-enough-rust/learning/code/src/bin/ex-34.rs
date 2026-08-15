// Returning a reference to a local value is rejected.
// Returning owned data is the safe repair.
fn message() -> String {
    String::from("owned, not dangling")
}
fn main() {
    println!("{}", message());
}
