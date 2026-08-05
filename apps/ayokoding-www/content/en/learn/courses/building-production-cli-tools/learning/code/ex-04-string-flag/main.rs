fn main() {
    let args: Vec<String> = std::env::args().collect();
    let name = if args.len() == 3 && args[1] == "--name" {
        &args[2]
    } else {
        "world"
    };
    println!("hello, {name}");
}
