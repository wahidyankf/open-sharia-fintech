//! Clears the `O_NONBLOCK` flag inherited on the process's standard streams.
//!
//! Git runs `pre-push`/`pre-commit` hooks with whatever descriptor flags it
//! inherited. When stdout arrives carrying `O_NONBLOCK`, a large enough burst
//! of output fills the pipe buffer, the next `write(2)` returns `EAGAIN`, and
//! Rust's `print!`/`println!` turn that into
//!
//! ```text
//! failed printing to stdout: Resource temporarily unavailable (os error 35)
//! ```
//!
//! — a panic, mid-line, that the gate runner reports as a plain gate failure.
//! The gate itself has found nothing wrong; it simply had too much to say. The
//! `governance-readme-index` gate hit this reproducibly at ~440 finding lines
//! while exiting 0 whenever it was run outside a hook.
//!
//! Clearing the flag once at startup fixes every print site in the binary at
//! once, which is the only tractable fix: there are 160+ of them, and any new
//! one would otherwise reintroduce the same crash.

/// Clears `O_NONBLOCK` on the standard streams, if set.
///
/// Best-effort and infallible by design: a descriptor that cannot be queried
/// or updated (closed, or not a file descriptor at all) leaves the process
/// exactly as it was. Never fails a command over a stream-flag adjustment.
pub fn make_std_streams_blocking() {
    #[cfg(unix)]
    {
        use std::os::fd::AsFd;
        clear_nonblock(std::io::stdout().as_fd());
        clear_nonblock(std::io::stderr().as_fd());
    }
}

/// Clears `O_NONBLOCK` on one borrowed descriptor, leaving every other flag
/// untouched. Returns `true` when the flag was set and has been cleared.
#[cfg(unix)]
pub fn clear_nonblock(fd: std::os::fd::BorrowedFd<'_>) -> bool {
    use rustix::fs::{OFlags, fcntl_getfl, fcntl_setfl};
    let Ok(flags) = fcntl_getfl(fd) else {
        return false;
    };
    if !flags.contains(OFlags::NONBLOCK) {
        return false;
    }
    fcntl_setfl(fd, flags - OFlags::NONBLOCK).is_ok()
}

#[cfg(all(test, unix))]
#[allow(clippy::unwrap_used, clippy::panic)]
mod tests {
    use super::*;
    use rustix::fs::{OFlags, fcntl_getfl, fcntl_setfl};
    use std::os::fd::AsFd;

    #[test]
    fn clears_the_nonblock_flag_a_hook_leaves_on_the_descriptor() {
        let (reader, _writer) = std::io::pipe().unwrap();
        let fd = reader.as_fd();
        let flags = fcntl_getfl(fd).unwrap();
        fcntl_setfl(fd, flags | OFlags::NONBLOCK).unwrap();
        assert!(
            fcntl_getfl(fd).unwrap().contains(OFlags::NONBLOCK),
            "precondition: the fixture must actually be non-blocking, or this \
             test passes without exercising anything"
        );

        assert!(clear_nonblock(fd), "must report that it cleared the flag");
        assert!(
            !fcntl_getfl(fd).unwrap().contains(OFlags::NONBLOCK),
            "O_NONBLOCK must be gone — this is the flag that makes a large \
             report panic with EAGAIN under a git hook"
        );
    }

    #[test]
    fn leaves_an_already_blocking_descriptor_alone_and_says_so() {
        let (reader, _writer) = std::io::pipe().unwrap();
        let fd = reader.as_fd();
        let before = fcntl_getfl(fd).unwrap();
        assert!(!clear_nonblock(fd), "nothing to clear must report false");
        assert_eq!(
            fcntl_getfl(fd).unwrap(),
            before,
            "no other descriptor flag may be disturbed"
        );
    }
}
