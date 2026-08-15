// co-11 co-12 co-13: message transfer plus Arc<Mutex<_>> produces a checked shared result.
fn main() {
    let state = std::sync::Arc::new(std::sync::Mutex::new(Vec::new()));
    let (tx, rx) = std::sync::mpsc::channel();
    let worker_state = state.clone();
    let worker = std::thread::spawn(move || {
        for n in rx {
            worker_state.lock().unwrap().push(n);
        }
    });
    tx.send(42).unwrap();
    drop(tx);
    worker.join().unwrap();
    assert_eq!(*state.lock().unwrap(), [42]);
}
