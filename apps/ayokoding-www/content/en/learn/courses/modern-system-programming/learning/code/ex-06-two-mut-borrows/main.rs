// co-05: sequential, non-overlapping mutable borrows are accepted; simultaneous ones are not.
fn main() {
    let mut value = 0;
    *(&mut value) += 1;
    *(&mut value) += 1;
    assert_eq!(value, 2);
}
