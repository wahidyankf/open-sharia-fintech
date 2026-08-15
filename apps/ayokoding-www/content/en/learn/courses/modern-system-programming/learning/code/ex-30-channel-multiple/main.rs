// co-11: cloned senders allow multiple producers with one receiver.
fn main() {
    let (tx, rx) = std::sync::mpsc::channel();
    for n in 1..=2 {
        let tx = tx.clone();
        std::thread::spawn(move || tx.send(n).unwrap());
    }
    drop(tx);
    let mut got: Vec<_> = rx.iter().collect();
    got.sort();
    assert_eq!(got, [1, 2]);
}
