// co-09 co-14: Rc cannot cross threads; Arc is the thread-safe alternative.
fn main() {
    let value = std::sync::Arc::new(7);
    let moved = value.clone();
    assert_eq!(std::thread::spawn(move || *moved).join().unwrap(), 7);
}
