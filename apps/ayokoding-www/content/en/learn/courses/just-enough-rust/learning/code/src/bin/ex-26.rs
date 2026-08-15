// Shadowing introduces a new binding with one name.
// The second type may differ from the first.
fn main() {
    let port = "8080";
    let port: u16 = port.parse().expect("literal port");
    println!("{port}");
}
