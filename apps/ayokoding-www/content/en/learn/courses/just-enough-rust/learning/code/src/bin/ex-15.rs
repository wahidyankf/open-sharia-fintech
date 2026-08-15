// match handles every enum variant.
// Exhaustiveness protects future states.
enum State {
    Ready,
    Stopped,
}
fn main() {
    for state in [State::Ready, State::Stopped] {
        println!(
            "{}",
            match state {
                State::Ready => "ready",
                State::Stopped => "stopped",
            }
        );
    }
}
