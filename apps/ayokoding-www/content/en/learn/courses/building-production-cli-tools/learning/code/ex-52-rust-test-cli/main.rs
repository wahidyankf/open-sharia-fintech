fn render(name: &str) -> String {
    format!("ok: {name}")
}
fn main() {
    assert_eq!(render("ship"), "ok: ship");
    println!("{}", render("ship"));
}
