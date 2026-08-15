// co-10 co-11: workers transform owned messages and hand results onward.
fn main() {
    let (input_tx, input_rx) = std::sync::mpsc::channel();
    let (out_tx, out_rx) = std::sync::mpsc::channel();
    let worker = std::thread::spawn(move || {
        for n in input_rx {
            out_tx.send(n * n).unwrap();
        }
    });
    input_tx.send(6).unwrap();
    drop(input_tx);
    worker.join().unwrap();
    assert_eq!(out_rx.recv().unwrap(), 36);
}
