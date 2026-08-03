fn main() {
    let mut flags = Vec::new();
    for arg in std::env::args().skip(1) {
        if arg.starts_with('-') && !arg.starts_with("--") {
            flags.extend(arg[1..].chars());
        }
    }
    println!("flags={}", flags.into_iter().collect::<String>());
}
