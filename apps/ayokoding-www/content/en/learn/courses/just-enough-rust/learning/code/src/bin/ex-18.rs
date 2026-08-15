// if let focuses on one useful pattern.
// The else branch handles absence.
fn main() {
    let port = Some(443);
    if let Some(number) = port {
        println!("{number}");
    } else {
        println!("none");
    }
}
