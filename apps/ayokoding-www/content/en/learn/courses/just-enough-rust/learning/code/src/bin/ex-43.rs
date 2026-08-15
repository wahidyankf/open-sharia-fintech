// impl connects a type to a trait contract.
// Calling through the trait uses that implementation.
trait Healthy {
    fn healthy(&self) -> bool;
}
struct Api;
impl Healthy for Api {
    fn healthy(&self) -> bool {
        true
    }
}
fn main() {
    println!("{}", Api.healthy());
}
