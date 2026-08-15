// An error enum identifies known failure classes.
// Result makes that enum part of the API.
#[derive(Debug)]
enum ConfigError {
    Missing,
    Invalid,
}
fn port(text: Option<&str>) -> Result<u16, ConfigError> {
    text.ok_or(ConfigError::Missing)?
        .parse()
        .map_err(|_| ConfigError::Invalid)
}
fn main() {
    println!("{:?} {:?}", port(Some("443")), port(None));
}
