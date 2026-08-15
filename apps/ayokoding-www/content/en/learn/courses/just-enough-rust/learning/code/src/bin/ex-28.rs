// Passing String by value moves it into consume.
// The caller cannot use it after that transfer.
fn consume(text: String) {
    println!("{text}");
}
fn main() {
    consume(String::from("owned"));
}
