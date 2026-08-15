// co-11: dropping all senders closes the receiving iterator as a shutdown signal.
fn main() {
    let (tx, rx) = std::sync::mpsc::channel::<u8>();
    drop(tx);
    assert_eq!(rx.iter().count(), 0);
}
