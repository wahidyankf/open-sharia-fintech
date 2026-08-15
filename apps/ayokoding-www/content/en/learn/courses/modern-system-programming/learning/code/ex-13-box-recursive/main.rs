// co-08: Box gives a recursive enum a known, pointer-sized variant.
enum List {
    End,
    Node(i32, Box<List>),
}
fn sum(list: &List) -> i32 {
    match list {
        List::End => 0,
        List::Node(value, next) => value + sum(next),
    }
}
fn length(list: &List) -> usize {
    match list {
        List::End => 0,
        List::Node(_, next) => 1 + length(next),
    }
}
fn main() {
    let list = List::Node(1, Box::new(List::End));
    assert_eq!((length(&list), sum(&list)), (1, 1));
}
