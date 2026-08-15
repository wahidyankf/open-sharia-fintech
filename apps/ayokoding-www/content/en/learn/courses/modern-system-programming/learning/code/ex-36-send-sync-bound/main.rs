// co-14 send-sync: this bound documents the type permitted to move to a thread.
fn spawn_value<T: Send + 'static>(value: T) -> T {
    std::thread::spawn(move || value).join().unwrap()
}
fn main() {
    assert_eq!(spawn_value(42), 42);
}
