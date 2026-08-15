// T lets one function accept many concrete types.
// Clone states the operation the body needs.
fn twice<T: Clone>(value: T) -> (T, T) {
    (value.clone(), value)
}
fn main() {
    println!("{:?} {:?}", twice(3), twice("api"));
}
