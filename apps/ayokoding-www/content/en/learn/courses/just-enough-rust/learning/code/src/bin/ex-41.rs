// match exposes both Result branches.
// The error branch remains ordinary control flow.
fn main() {
    let parsed = "x".parse::<u16>();
    println!(
        "{}",
        match parsed {
            Ok(port) => port.to_string(),
            Err(_) => "invalid".into(),
        }
    );
}
