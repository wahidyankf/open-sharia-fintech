fn main() {
    match std::env::args().nth(1) {
        Some(file) => println!("checking {file}"),
        None => {
            eprintln!("usage: check FILE");
            std::process::exit(2)
        }
    }
}
