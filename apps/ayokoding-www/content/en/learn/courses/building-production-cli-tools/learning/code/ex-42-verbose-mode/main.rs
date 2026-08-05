fn main() {
    let verbose = std::env::args().any(|a| a == "--verbose");
    if verbose {
        eprintln!("debug: reading release manifest")
    };
    println!("ready")
}
