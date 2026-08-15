// co-09 rc-refcell: Rc shares ownership only within one thread.
fn main() {
    let first = std::rc::Rc::new(String::from("local"));
    let second = first.clone();
    assert_eq!(std::rc::Rc::strong_count(&first), 2);
    assert_eq!(second.as_str(), "local");
}
