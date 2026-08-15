// co-15: repeated runs use message ownership instead of aliased mutable state.
fn main() {
    for _ in 0..10 {
        let (tx, rx) = std::sync::mpsc::channel();
        std::thread::spawn(move || tx.send(42).unwrap())
            .join()
            .unwrap();
        assert_eq!(rx.recv().unwrap(), 42);
    }
}
