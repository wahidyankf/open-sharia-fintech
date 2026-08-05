fn main() {
    let endpoint =
        std::env::var("SHIP_ENDPOINT").unwrap_or_else(|_| "https://api.example.test".into());
    println!("endpoint={endpoint}")
}
