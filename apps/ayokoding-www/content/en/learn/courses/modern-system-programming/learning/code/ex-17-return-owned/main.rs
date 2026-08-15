// co-01: returning a value transfers ownership to the caller.
fn decorate(value: String) -> String {
    format!("[{value}]")
}
fn main() {
    assert_eq!(decorate(String::from("ok")), "[ok]");
}
