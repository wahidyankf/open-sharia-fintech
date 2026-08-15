// co-16 zero-cost-iterators: map expresses the same work as an explicit loop.
fn main() {
    let mapped: Vec<_> = [1, 2, 3].into_iter().map(|n| n * 2).collect();
    assert_eq!(mapped, [2, 4, 6]);
}
