// A closure can read a surrounding binding.
// Calling it uses that captured environment.
fn main() {
    let prefix = "service";
    let label = |name: &str| format!("{prefix}:{name}");
    println!("{}", label("api"));
}
