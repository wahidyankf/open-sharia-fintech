fn main() {
    let format = std::env::args().nth(1).unwrap_or_else(|| "text".into());
    println!("format={format}")
}
