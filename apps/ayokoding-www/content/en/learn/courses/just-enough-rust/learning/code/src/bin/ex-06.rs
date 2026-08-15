// `let count = 1; count = 2;` is rejected.
// This valid repair names mutation with mut.
fn main() {
    let mut count = 1;
    println!("{count}");
    count = 2;
    println!("{count}");
}
