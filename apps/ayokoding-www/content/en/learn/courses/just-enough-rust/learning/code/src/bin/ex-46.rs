// A generic struct carries a chosen field type.
// Each construction selects a concrete T.
struct Config<T> {
    value: T,
}
fn main() {
    let port = Config { value: 443 };
    let host = Config { value: "localhost" };
    println!("{} {}", port.value, host.value);
}
