// Multiple bounds state each operation a generic needs.
// Display renders while Clone preserves the value.
fn duplicate_label<T: Clone + std::fmt::Display>(value: T) -> String {
    format!("{value}, {}", value.clone())
}
fn main() {
    println!("{}", duplicate_label("api"));
}
