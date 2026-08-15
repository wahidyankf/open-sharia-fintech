// co-30 co-11: async channels have the same ownership-transfer idea as mpsc channels.
async fn send_then_receive() -> i32 {
    42
}
fn main() {
    let _future = send_then_receive();
}
