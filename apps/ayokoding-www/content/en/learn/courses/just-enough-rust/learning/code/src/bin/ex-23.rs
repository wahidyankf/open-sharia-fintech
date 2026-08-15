// for borrows each vector item in turn.
// The vector remains available after the loop.
fn main() {
    let ports = vec![80, 443];
    for port in &ports {
        print!("{port} ");
    }
    println!("{}", ports.len());
}
