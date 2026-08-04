fn main() {
    match std::env::args().nth(1).as_deref() {
        Some("bash") => println!("complete -W 'check publish' ship"),
        Some("zsh") => println!("compadd check publish"),
        _ => eprintln!("usage: ship completion <bash|zsh>"),
    }
}
