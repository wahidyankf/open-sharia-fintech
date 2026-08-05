fn normalize(name: &str) -> String {
    name.trim().to_ascii_lowercase()
}
fn main() {
    let raw = std::env::args().nth(1).unwrap_or_else(|| " Ship ".into());
    println!("{}", normalize(&raw));
}
