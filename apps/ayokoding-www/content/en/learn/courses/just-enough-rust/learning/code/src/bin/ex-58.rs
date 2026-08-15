// Option fields state data may be unavailable.
// as_deref borrows the contained String as str.
struct Config {
    host: Option<String>,
}
fn main() {
    let config = Config { host: None };
    println!("{}", config.host.as_deref().unwrap_or("localhost"));
}
