// co-17: generic trait calls use static dispatch for each concrete T.
trait Magnitude {
    fn magnitude(&self) -> i32;
}
impl Magnitude for i32 {
    fn magnitude(&self) -> i32 {
        self.abs()
    }
}
fn absolute<T: Magnitude>(value: T) -> i32 {
    value.magnitude()
}
fn main() {
    assert_eq!(absolute(-8_i32), 8);
}
