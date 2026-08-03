use std::io::IsTerminal;
fn main() {
    let tty = std::io::stderr().is_terminal();
    if tty {
        eprint!("\r\x1b[36muploading\x1b[0m")
    };
    println!("{{\"status\":\"done\"}}");
}
