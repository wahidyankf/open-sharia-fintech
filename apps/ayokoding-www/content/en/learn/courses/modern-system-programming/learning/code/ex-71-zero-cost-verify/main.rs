// co-16: iterator and hand-loop forms produce the same observable result.
fn main() {
    let iter: i32 = (0..10).filter(|n| n % 2 == 0).sum();
    let mut looped = 0;
    for n in 0..10 {
        if n % 2 == 0 {
            looped += n;
        }
    }
    assert_eq!(iter, looped);
}
