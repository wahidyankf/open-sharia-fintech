// A function can borrow only the data it reads.
// The caller keeps ownership of the String.
fn starts_api(path: &str) -> bool {
    path.starts_with("/api")
}
fn main() {
    let path = String::from("/api/health");
    println!("{} {path}", starts_api(&path));
}
