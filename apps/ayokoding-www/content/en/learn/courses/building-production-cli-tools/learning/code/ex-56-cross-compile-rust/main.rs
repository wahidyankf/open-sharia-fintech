fn main() {
    println!(
        "rustup target add x86_64-unknown-linux-musl\ncargo build --release --target x86_64-unknown-linux-musl"
    );
}
