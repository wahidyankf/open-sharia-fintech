// co-12 co-13: Arc shares the lock; Mutex serializes each mutation.
fn main() {
    let count = std::sync::Arc::new(std::sync::Mutex::new(0));
    let handles: Vec<_> = (0..4)
        .map(|_| {
            let count = count.clone();
            std::thread::spawn(move || *count.lock().unwrap() += 1)
        })
        .collect();
    for h in handles {
        h.join().unwrap();
    }
    assert_eq!(*count.lock().unwrap(), 4);
}
