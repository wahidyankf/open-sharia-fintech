// co-30: async fn creates a future; a runtime is required to poll it to completion.
async fn answer() -> i32 {
    42
}
fn main() {
    let _future = answer();
}
