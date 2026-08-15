// co-16: fold and sum make the accumulation policy explicit.
fn main() {
    let total: i32 = [1, 2, 3, 4].into_iter().sum();
    assert_eq!(total, 10);
}
