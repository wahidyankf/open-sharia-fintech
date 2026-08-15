// filter retains items matching its predicate.
// The closure borrows each candidate.
fn main() {
    let secure: Vec<_> = [80, 443, 8080]
        .into_iter()
        .filter(|port| *port >= 443)
        .collect();
    println!("{secure:?}");
}
