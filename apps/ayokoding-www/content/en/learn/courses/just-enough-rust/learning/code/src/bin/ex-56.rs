// fold carries an accumulator through the iterator.
// The closure returns each next accumulator.
fn main() {
    let total = [80, 443].into_iter().fold(0, |sum, port| sum + port);
    println!("{total}");
}
