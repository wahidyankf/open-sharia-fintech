// A Vec can own structured values.
// Iteration borrows each element to read it.
struct Service {
    name: &'static str,
}
fn main() {
    let services = vec![Service { name: "api" }, Service { name: "worker" }];
    for service in &services {
        print!("{} ", service.name);
    }
    println!();
}
