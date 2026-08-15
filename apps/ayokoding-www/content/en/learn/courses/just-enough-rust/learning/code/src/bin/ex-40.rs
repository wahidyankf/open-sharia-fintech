// unwrap_or supplies a local default for None.
// The caller stays explicit about the fallback.
fn main() {
    let host: Option<&str> = None;
    println!("{}", host.unwrap_or("localhost"));
}
