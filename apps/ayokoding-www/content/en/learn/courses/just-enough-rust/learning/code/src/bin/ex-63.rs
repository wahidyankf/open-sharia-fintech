// derive(Debug) supplies diagnostic formatting.
// {:?} asks for that Debug representation.
#[derive(Debug)]
struct Endpoint {
    port: u16,
}
fn main() {
    let endpoint = Endpoint { port: 443 };
    println!("{endpoint:?} {}", endpoint.port);
}
