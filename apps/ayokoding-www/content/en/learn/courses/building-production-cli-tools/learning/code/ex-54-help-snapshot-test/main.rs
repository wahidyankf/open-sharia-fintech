fn help() -> &'static str {
    "usage: ship [--json] RELEASE\n"
}
fn main() {
    assert_eq!(help(), "usage: ship [--json] RELEASE\n");
    print!("{}", help());
}
