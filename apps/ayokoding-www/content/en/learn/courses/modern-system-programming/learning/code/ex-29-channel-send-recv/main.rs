// co-11 channels: send transfers message ownership to the receiver.
fn main() {
    let (tx, rx) = std::sync::mpsc::channel();
    tx.send(String::from("done")).unwrap();
    assert_eq!(rx.recv().unwrap(), "done");
}
