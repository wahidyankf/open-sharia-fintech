// co-09: RefCell checks mutable borrowing at runtime in a single-threaded context.
fn main() {
    let value = std::cell::RefCell::new(1);
    *value.borrow_mut() += 1;
    assert_eq!(*value.borrow(), 2);
}
