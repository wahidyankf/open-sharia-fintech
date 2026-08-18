//! `rhino-cli` binary entry point.
#![forbid(unsafe_code)]

fn main() {
    // Git hands hooks whatever descriptor flags it inherited. If stdout
    // arrives non-blocking, a long report (the README-index gate emits ~440
    // finding lines) fills the pipe buffer and the next write returns EAGAIN,
    // which `println!` escalates to a panic — reported to the user as an
    // unexplained gate failure even though the gate found nothing wrong.
    rhino_cli::infrastructure::stdio_blocking::make_std_streams_blocking();

    let exit_code = rhino_cli::cli::run();
    std::process::exit(exit_code);
}
