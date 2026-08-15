// co-25 co-23: do not mutate process environment in a multithreaded program; read it safely instead.
fn main() {
    let path = std::env::var_os("PATH");
    assert!(path.is_some());
}
