// entry combines lookup and insert-or-update.
// or_insert returns a mutable value reference.
use std::collections::HashMap;
fn main() {
    let mut counts = HashMap::new();
    *counts.entry("api").or_insert(0) += 1;
    println!("{:?}", counts);
}
