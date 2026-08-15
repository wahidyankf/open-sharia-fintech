// End the shared borrow before requesting &mut access.
// Non-lexical lifetimes permit this clear sequence.
fn main() {
    let mut status = String::from("ready");
    let size = status.len();
    println!("{size}");
    status.push_str(" ok");
    println!("{status}");
}
