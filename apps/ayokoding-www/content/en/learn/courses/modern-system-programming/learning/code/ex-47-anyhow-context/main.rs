// co-22 anyhow: applications can add context; this dependency-free version keeps the message explicit.
fn load(text: &str) -> Result<u32, String> {
    text.parse()
        .map_err(|_| format!("config port `{text}` is invalid"))
}
fn main() {
    assert_eq!(load("bad"), Err("config port `bad` is invalid".into()));
}
