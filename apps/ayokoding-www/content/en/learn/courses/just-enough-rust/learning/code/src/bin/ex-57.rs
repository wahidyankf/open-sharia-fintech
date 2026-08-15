// Enums can also own methods through impl.
// match keeps every state handling explicit.
enum Connection {
    Open,
    Closed,
}
impl Connection {
    fn label(&self) -> &str {
        match self {
            Self::Open => "open",
            Self::Closed => "closed",
        }
    }
}
fn main() {
    println!("{}", Connection::Open.label());
    let _ = Connection::Closed;
}
