fn main() {
    let a: Vec<String> = std::env::args().collect();
    if a.get(1).map(String::as_str) != Some("status") || a.iter().any(|x| x == "--help") {
        println!("usage: ship status [--region REGION]");
        return;
    };
    let flag_region = a
        .windows(2)
        .find(|p| p[0] == "--region")
        .map(|p| p[1].clone());
    let config = std::fs::read_to_string("ship.conf")
        .ok()
        .map(|s| s.trim().to_owned())
        .filter(|s| !s.is_empty());
    let region = flag_region
        .or_else(|| std::env::var("SHIP_REGION").ok())
        .or(config)
        .unwrap_or_else(|| "local".into());
    println!("status region={region}")
}
