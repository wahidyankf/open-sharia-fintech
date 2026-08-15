// co-19: match requires both success and failure paths to be handled.
fn main() {
    let message = match "x".parse::<u32>() {
        Ok(n) => n.to_string(),
        Err(_) => "invalid".into(),
    };
    assert_eq!(message, "invalid");
}
