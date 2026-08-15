// co-07 drop: destructors run predictably when a scope ends.
struct Guard<'a>(&'a mut bool);
impl Drop for Guard<'_> {
    fn drop(&mut self) {
        *self.0 = true;
    }
}
fn main() {
    let mut dropped = false;
    {
        let _guard = Guard(&mut dropped);
    }
    assert!(dropped);
}
