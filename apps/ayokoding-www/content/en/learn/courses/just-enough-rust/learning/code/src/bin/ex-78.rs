// The final slice previews every capstone requirement together.
// Run and test the dedicated capstone crate for the full check.
trait Named {
    fn name(&self) -> &str;
}
struct Job {
    name: String,
    port: Option<u16>,
}
impl Named for Job {
    fn name(&self) -> &str {
        &self.name
    }
}
enum Outcome {
    Ready,
    MissingPort,
}
fn render<T: Named>(job: &T, outcome: Outcome) -> Result<String, String> {
    Ok(format!(
        "{}:{}",
        job.name(),
        match outcome {
            Outcome::Ready => "ready",
            Outcome::MissingPort => "missing",
        }
    ))
}
fn main() {
    let job = Job {
        name: "api".into(),
        port: Some(443),
    };
    let outcome = if job.port.is_some() {
        Outcome::Ready
    } else {
        Outcome::MissingPort
    };
    println!("{:?}", render(&job, outcome));
}
