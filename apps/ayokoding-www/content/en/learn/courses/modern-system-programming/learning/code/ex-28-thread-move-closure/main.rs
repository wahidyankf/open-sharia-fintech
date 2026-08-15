// co-10 co-02: move transfers captured ownership into the spawned closure.
fn main() {
    let word = String::from("worker");
    let handle = std::thread::spawn(move || word.len());
    assert_eq!(handle.join().unwrap(), 6);
}
