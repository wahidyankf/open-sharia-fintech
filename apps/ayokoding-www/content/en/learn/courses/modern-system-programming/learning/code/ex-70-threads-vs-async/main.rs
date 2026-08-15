// co-10 co-30: threads run OS stacks; async tasks need an executor and cooperate at await points.
fn main() {
    assert_eq!(std::thread::spawn(|| 42).join().unwrap(), 42);
}
