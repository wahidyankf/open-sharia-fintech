// Traits may provide a default method body.
// An implementor receives it without repeating code.
trait Named {
    fn name(&self) -> &str;
    fn label(&self) -> String {
        format!("service:{}", self.name())
    }
}
struct Api;
impl Named for Api {
    fn name(&self) -> &str {
        "api"
    }
}
fn main() {
    println!("{}", Api.label());
}
