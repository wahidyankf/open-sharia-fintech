// Returning String transfers ownership to the caller.
// The caller becomes responsible for the result.
fn request() -> String {
    String::from("GET /health")
}
fn main() {
    let line = request();
    println!("{line}");
}
