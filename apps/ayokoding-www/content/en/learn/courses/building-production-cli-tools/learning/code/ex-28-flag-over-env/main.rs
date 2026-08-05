fn main() {
    let args: Vec<String> = std::env::args().collect();
    let region = args
        .windows(2)
        .find(|p| p[0] == "--region")
        .map(|p| p[1].clone())
        .or_else(|| std::env::var("SHIP_REGION").ok())
        .unwrap_or_else(|| "local".into());
    println!("region={region}")
}
