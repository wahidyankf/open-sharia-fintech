// co-12 arc: atomic reference counting gives threads shared immutable ownership.
fn main() {
    let value = std::sync::Arc::new(String::from("shared"));
    let other = value.clone();
    let handle = std::thread::spawn(move || other.len());
    assert_eq!(handle.join().unwrap(), value.len());
}
