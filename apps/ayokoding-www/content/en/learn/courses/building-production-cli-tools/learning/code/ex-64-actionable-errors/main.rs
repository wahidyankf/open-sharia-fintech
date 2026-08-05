fn main() {
    let path = ".ship/token";
    if std::fs::metadata(path).is_err() {
        eprintln!("error: {path} is missing; run `ship login`");
        std::process::exit(1)
    }
}
