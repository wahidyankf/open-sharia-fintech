fn main() {
    let region = std::fs::read_to_string("ship.conf")
        .ok()
        .map(|s| s.trim().to_owned())
        .filter(|s| !s.is_empty())
        .unwrap_or_else(|| "local".into());
    println!("region={region}")
}
