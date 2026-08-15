// co-30: Tokio is one possible executor; this standard-library example remains runnable without pinning it.
async fn work() -> &'static str {
    "task"
}
fn main() {
    let _future = work();
}
