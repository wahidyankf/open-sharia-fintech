fn main() {
    let a: Vec<String> = std::env::args().collect();
    let verbose = a.iter().any(|x| x == "--verbose");
    let command = a.last().map(String::as_str).unwrap_or("help");
    if verbose {
        eprintln!("debug: dispatching {command}")
    };
    println!("{command}")
}
