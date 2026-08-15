// String owns mutable UTF-8 text.
// push_str appends borrowed text.
fn main() {
    let mut endpoint = String::from("/api");
    endpoint.push_str("/health");
    println!("{endpoint}");
}
