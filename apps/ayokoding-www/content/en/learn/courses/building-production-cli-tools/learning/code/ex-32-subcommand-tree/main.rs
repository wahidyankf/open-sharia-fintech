fn main() {
    let a: Vec<String> = std::env::args().skip(1).collect();
    match a.as_slice() {
        [group, command] if group == "config" && command == "get" => println!("read config"),
        [group, command] if group == "config" && command == "set" => println!("write config"),
        _ => eprintln!("usage: ship config <get|set>"),
    }
}
