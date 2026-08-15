// co-13: AtomicUsize provides a lock-free counter with an explicit ordering.
fn main() {
    let count = std::sync::Arc::new(std::sync::atomic::AtomicUsize::new(0));
    let other = count.clone();
    std::thread::spawn(move || {
        other.fetch_add(1, std::sync::atomic::Ordering::SeqCst);
    })
    .join()
    .unwrap();
    assert_eq!(count.load(std::sync::atomic::Ordering::SeqCst), 1);
}
