// co-01 co-12 co-16 co-27: ownership, Arc, iterators, and a safe boundary cooperate.
fn main() {
    let values = std::sync::Arc::new(vec![20, 22]);
    let other = values.clone();
    let sum = std::thread::spawn(move || other.iter().sum::<i32>())
        .join()
        .unwrap();
    assert_eq!(sum, 42);
}
