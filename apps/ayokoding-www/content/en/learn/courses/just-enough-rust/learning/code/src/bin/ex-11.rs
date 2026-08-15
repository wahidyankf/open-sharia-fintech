// A struct groups named fields into one value.
// Field access reads the stored data.
struct Service {
    name: String,
}
fn main() {
    let service = Service { name: "api".into() };
    println!("{}", service.name);
}
