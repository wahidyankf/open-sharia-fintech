// Derived traits can implement routine value behavior.
// Equality compares the owned field values.
#[derive(Clone, PartialEq, Debug)]
struct Port(u16);
fn main() {
    let first = Port(443);
    let second = first.clone();
    println!("{}", first == second);
}
