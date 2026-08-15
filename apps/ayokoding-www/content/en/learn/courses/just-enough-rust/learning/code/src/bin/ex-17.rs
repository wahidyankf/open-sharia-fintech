// A match arm binds the variant payload.
// The binding becomes local to that arm.
enum Event {
    Bytes(usize),
    Closed,
}
fn main() {
    let event = Event::Bytes(8);
    println!(
        "{}",
        match event {
            Event::Bytes(count) => count,
            Event::Closed => 0,
        }
    );
    let _ = Event::Closed;
}
