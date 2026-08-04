fn main() {
    let a: Vec<String> = std::env::args().collect();
    let quiet = a.contains(&"--quiet".into());
    let verbose = a.contains(&"--verbose".into());
    if verbose && !quiet {
        eprintln!("debug: resolving configuration")
    };
    if !quiet {
        println!("done")
    }
}
