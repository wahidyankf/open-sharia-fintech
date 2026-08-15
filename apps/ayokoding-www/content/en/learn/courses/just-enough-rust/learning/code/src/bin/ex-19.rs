// while let repeats while a pattern matches.
// pop returns None when the vector is empty.
fn main() {
    let mut values = vec![1, 2];
    while let Some(value) = values.pop() {
        print!("{value}");
    }
    println!();
}
