// co-17 traits-generics: one generic definition is specialized for its concrete callers.
fn largest<T: Ord + Copy>(items: &[T]) -> T {
    *items.iter().max().unwrap()
}
fn main() {
    assert_eq!(largest(&[3, 1, 4]), 4);
}
