// co-06: returning `&local` would dangle, so return ownership instead.
fn created() -> String {
    String::from("owned result")
}
fn main() {
    assert_eq!(created(), "owned result");
}
