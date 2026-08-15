// Many shared borrows may coexist.
// This runnable form avoids a conflicting mutable borrow.
fn main() {
    let message = String::from("stable");
    let first = &message;
    let second = &message;
    println!("{first} {second}");
}
