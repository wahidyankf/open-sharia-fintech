// Variants can carry data with their state.
// A pattern extracts the carried port.
enum Event {
    Connected(u16),
}
fn main() {
    let Event::Connected(port) = Event::Connected(443);
    println!("{port}");
}
