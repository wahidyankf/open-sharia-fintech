// co-13 mutex: the lock guard releases the lock at scope end.
fn main() {
    let value = std::sync::Mutex::new(1);
    {
        *value.lock().unwrap() += 1;
    }
    assert_eq!(*value.lock().unwrap(), 2);
}
