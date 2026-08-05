use std::io::IsTerminal;
fn main() {
    if std::io::stdout().is_terminal() {
        println!("\x1b[32mready\x1b[0m")
    } else {
        println!("ready")
    }
}
