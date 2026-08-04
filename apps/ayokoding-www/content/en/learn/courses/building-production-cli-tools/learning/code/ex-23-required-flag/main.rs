fn main() {
    let args: Vec<String> = std::env::args().collect();
    match args
        .windows(2)
        .find(|p| p[0] == "--release")
        .map(|p| p[1].as_str())
    {
        Some(value) => println!("publishing {value}"),
        None => {
            eprintln!("--release is required");
            std::process::exit(2)
        }
    }
}
