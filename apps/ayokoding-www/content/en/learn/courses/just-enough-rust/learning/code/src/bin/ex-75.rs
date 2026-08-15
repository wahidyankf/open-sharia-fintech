// Passing &String borrows; passing String transfers ownership.
// These functions make their requirements explicit.
fn inspect(value: &str) {
    println!("borrowed:{value}");
}
fn consume(value: String) {
    println!("moved:{value}");
}
fn main() {
    let value = String::from("api");
    inspect(&value);
    consume(value);
}
