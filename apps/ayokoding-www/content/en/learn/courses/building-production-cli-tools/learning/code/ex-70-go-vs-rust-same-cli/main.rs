fn main() {
    let region = std::env::args().nth(1).unwrap_or_else(|| "local".into());
    println!("{{\"region\":\"{region}\",\"status\":\"ready\"}}");
}
