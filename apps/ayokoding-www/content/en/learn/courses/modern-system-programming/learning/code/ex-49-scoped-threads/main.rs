// co-10: scoped threads may borrow stack data because scope joins them.
fn main() {
    let values = [20, 22];
    std::thread::scope(|scope| {
        let handle = scope.spawn(|| values.iter().sum::<i32>());
        assert_eq!(handle.join().unwrap(), 42);
    });
}
