// clone makes a deliberate second owned String.
// Both owners can then be used independently.
fn main() {
    let original = String::from("config");
    let copy = original.clone();
    println!("{original} {copy}");
}
