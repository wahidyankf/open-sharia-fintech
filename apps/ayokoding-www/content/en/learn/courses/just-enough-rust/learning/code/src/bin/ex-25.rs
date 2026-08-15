// An array has a fixed length; a slice borrows part.
// The slice does not own a new collection.
fn main() {
    let ports = [80, 443, 8080];
    let secure = &ports[..2];
    println!("{}", secure.len());
}
