// co-16: filter lazily selects items before collection.
fn main() {
    let evens: Vec<_> = (1..=6).filter(|n| n % 2 == 0).collect();
    assert_eq!(evens, [2, 4, 6]);
}
