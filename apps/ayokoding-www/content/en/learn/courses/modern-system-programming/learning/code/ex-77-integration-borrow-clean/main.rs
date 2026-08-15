// co-05 co-15 co-29: borrow-clean message passing avoids a shared mutable race.
fn main() {
    let input = vec![40, 2];
    let (tx, rx) = std::sync::mpsc::channel();
    std::thread::spawn(move || tx.send(input.iter().sum::<i32>()).unwrap())
        .join()
        .unwrap();
    assert_eq!(rx.recv().unwrap(), 42);
}
