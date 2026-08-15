// dyn Trait stores behavior behind a trait object.
// Dynamic dispatch selects the concrete implementation.
trait Render {
    fn render(&self) -> String;
}
struct Text;
impl Render for Text {
    fn render(&self) -> String {
        "text".into()
    }
}
fn main() {
    let item: &dyn Render = &Text;
    println!("{}", item.render());
}
