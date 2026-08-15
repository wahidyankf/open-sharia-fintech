// A trait bound tells the compiler required behavior.
// Display allows format! to render every T.
fn label<T: std::fmt::Display>(value: T) -> String {
    format!("value={value}")
}
fn main() {
    println!("{} {}", label(443), label("api"));
}
