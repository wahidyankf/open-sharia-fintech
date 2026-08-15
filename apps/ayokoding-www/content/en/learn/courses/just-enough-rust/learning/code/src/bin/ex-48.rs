// map lazily transforms every iterator item.
// collect materializes the final vector.
fn main() {
    let doubled: Vec<_> = [1, 2, 3].into_iter().map(|value| value * 2).collect();
    println!("{doubled:?}");
}
