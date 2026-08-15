// co-01 co-12 co-16 co-27 co-25: full runnable safety slice; the detailed version is the capstone.
fn main() {
    let values = std::sync::Arc::new(vec![20, 22]);
    let other = values.clone();
    let total = std::thread::spawn(move || other.iter().sum::<i32>())
        .join()
        .unwrap();
    assert_eq!(total, 42);
}
