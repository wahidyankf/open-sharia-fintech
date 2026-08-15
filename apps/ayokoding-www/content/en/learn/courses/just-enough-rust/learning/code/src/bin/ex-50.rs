// collect uses the target type to choose a collection.
// Vec owns the collected iterator values.
fn main() {
    let names: Vec<String> = ["api", "worker"].into_iter().map(String::from).collect();
    println!("{names:?}");
}
