// An enum chooses one named variant.
// Match observes which variant exists.
enum State {
    Ready,
    Stopped,
}
fn main() {
    let state = State::Ready;
    println!("{}", matches!(state, State::Ready));
    let _ = State::Stopped;
}
