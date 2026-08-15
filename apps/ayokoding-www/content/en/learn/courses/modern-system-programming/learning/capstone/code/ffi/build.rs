use std::{env, process::Command};

fn main() {
    println!("cargo:rerun-if-changed=c/double.c");
    let out = env::var("OUT_DIR").expect("Cargo provides OUT_DIR");
    let object = format!("{out}/double.o");
    let archive = format!("{out}/libdouble.a");
    assert!(
        Command::new("cc")
            .args(["-c", "c/double.c", "-o", &object])
            .status()
            .expect("C compiler available")
            .success()
    );
    assert!(
        Command::new("ar")
            .args(["rcs", &archive, &object])
            .status()
            .expect("archive tool available")
            .success()
    );
    println!("cargo:rustc-link-search=native={out}");
    println!("cargo:rustc-link-lib=static=double");
}
