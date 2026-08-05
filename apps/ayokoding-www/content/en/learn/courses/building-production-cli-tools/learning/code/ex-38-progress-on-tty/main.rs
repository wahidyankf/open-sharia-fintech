use std::io::{self, IsTerminal, Write};
fn main() {
    if io::stderr().is_terminal() {
        eprint!("\rUploading 100%");
        io::stderr().flush().unwrap();
    }
    println!("uploaded")
}
