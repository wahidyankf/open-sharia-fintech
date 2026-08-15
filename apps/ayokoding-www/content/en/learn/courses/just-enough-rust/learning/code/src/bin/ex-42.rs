// A trait names shared behavior as a contract.
// Implementations provide its concrete result.
trait Describe {
    fn describe(&self) -> String;
}
struct Service;
impl Describe for Service {
    fn describe(&self) -> String {
        "service".into()
    }
}
fn main() {
    println!("{}", Service.describe());
}
