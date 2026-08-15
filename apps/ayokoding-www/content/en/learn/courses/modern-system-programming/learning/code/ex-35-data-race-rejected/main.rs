// co-15 co-14: use Arc<Mutex<_>>; sharing `&mut` into two threads is rejected.
fn main() {
    let value = std::sync::Arc::new(std::sync::Mutex::new(0));
    let other = value.clone();
    std::thread::spawn(move || *other.lock().unwrap() += 1)
        .join()
        .unwrap();
    assert_eq!(*value.lock().unwrap(), 1);
}
