// co-16: adapters fuse into a direct loop after optimization, without an iterator allocation.
fn main() {
    let total: i32 = (1..=5).filter(|n| n % 2 == 1).map(|n| n * n).sum();
    assert_eq!(total, 35);
}
