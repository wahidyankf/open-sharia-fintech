// impl attaches behavior to a struct.
// The method borrows self to read it.
struct Port(u16);
impl Port {
    fn number(&self) -> u16 {
        self.0
    }
}
fn main() {
    println!("{}", Port(8080).number());
}
