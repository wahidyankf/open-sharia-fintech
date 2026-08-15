// HashMap owns key/value associations.
// get returns Option for an absent key.
use std::collections::HashMap;
fn main() {
    let mut ports = HashMap::new();
    ports.insert("https", 443);
    println!("{:?}", ports.get("https"));
}
