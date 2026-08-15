// Vec owns a growable sequence of values.
// push changes the vector deliberately.
fn main() {
    let mut ports = vec![80];
    ports.push(443);
    println!("{}", ports[1]);
}
