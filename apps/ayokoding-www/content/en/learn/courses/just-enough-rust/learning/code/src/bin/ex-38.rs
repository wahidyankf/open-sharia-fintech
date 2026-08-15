// parse returns Result because text may not be numeric.
// The caller chooses how to display failure.
fn main() {
    let good = "8080".parse::<u16>();
    let bad = "port".parse::<u16>();
    println!("{:?} {:?}", good, bad);
}
