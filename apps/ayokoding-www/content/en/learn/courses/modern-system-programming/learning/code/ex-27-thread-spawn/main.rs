// co-10 threads: join makes the parent wait for the child result.
fn main() {
    let handle = std::thread::spawn(|| 21 * 2);
    assert_eq!(handle.join().unwrap(), 42);
}
