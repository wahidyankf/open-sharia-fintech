fn main() {
    let command = std::env::args().nth(1).unwrap_or_default();
    match command.as_str() {
        "check" => println!("ok"),
        "publish" => println!("published"),
        _ => {
            eprintln!("usage: ship <check|publish>");
            std::process::exit(2)
        }
    }
}
