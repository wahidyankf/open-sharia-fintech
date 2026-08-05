fn main() {
    if std::env::args().any(|a| a == "--help" || a == "-h") {
        println!("usage: ship [--dry-run] RELEASE\n\nPublish a release safely.")
    } else {
        println!("run ship --help")
    }
}
