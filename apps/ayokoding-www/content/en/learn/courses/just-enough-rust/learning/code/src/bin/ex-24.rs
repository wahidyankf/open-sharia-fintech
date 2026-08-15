// A tuple groups positional values.
// Destructuring gives each part a name.
fn main() {
    let response = (200, "ok");
    let (code, text) = response;
    println!("{code} {text}");
}
