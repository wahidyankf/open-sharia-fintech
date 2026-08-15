// The signature states the input and output contract.
// main observes a typed function call.
fn double(value: i32) -> i32 {
    value * 2
}
fn main() {
    println!("{}", double(21));
}
