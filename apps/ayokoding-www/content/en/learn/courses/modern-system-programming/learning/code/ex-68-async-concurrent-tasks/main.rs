// co-30: futures describe concurrent work; an executor determines when each is polled.
async fn job(n: i32) -> i32 {
    n * 2
}
fn main() {
    let (_left, _right) = (job(1), job(2));
}
