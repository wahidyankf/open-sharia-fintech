// This combines struct, enum, trait, generic, Result, and match.
// It is still a short language slice, not a systems project.
trait Named {
    fn name(&self) -> &str;
}
struct Service {
    name: String,
}
impl Named for Service {
    fn name(&self) -> &str {
        &self.name
    }
}
enum State {
    Ready,
    Stopped,
}
fn report<T: Named>(service: &T, state: State) -> Result<String, String> {
    Ok(format!(
        "{}:{}",
        service.name(),
        match state {
            State::Ready => "ready",
            State::Stopped => "stopped",
        }
    ))
}
fn main() {
    println!(
        "{:?}",
        report(&Service { name: "api".into() }, State::Ready)
    );
    let _ = State::Stopped;
}
