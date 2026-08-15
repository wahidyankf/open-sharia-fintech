// Iterator adapters compose without intermediate vectors.
// collect performs the final allocation.
fn main() {
    let ports: Vec<_> = [80, 443, 8080]
        .into_iter()
        .filter(|port| *port >= 443)
        .map(|port| port + 1)
        .collect();
    println!("{ports:?}");
}
