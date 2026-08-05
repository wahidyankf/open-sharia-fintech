fn main() {
    let args: Vec<String> = std::env::args().skip(1).collect();
    let i = args.iter().position(|a| a == "--");
    println!(
        "child args: {}",
        i.map(|n| args[n + 1..].join(" ")).unwrap_or_default()
    )
}
