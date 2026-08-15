// &mut gives one caller exclusive mutation access.
// The borrow ends after append returns.
fn append_ok(text: &mut String) {
    text.push_str(" ok");
}
fn main() {
    let mut status = String::from("ready");
    append_ok(&mut status);
    println!("{status}");
}
