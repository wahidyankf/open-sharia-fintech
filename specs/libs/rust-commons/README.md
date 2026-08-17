# rust-commons Specs

Gherkin behavioral specifications for
[rust-commons](../../../libs/rust-commons/Cargo.toml), the shared Rust utility crate.

## Purpose

These specs define the **observable behavior** of the shared utilities exposed by
`rust-commons`: given a content directory, which internal markdown links are checked, and which
are reported broken.

## Structure

```
specs/libs/rust-commons/
├── README.md
├── product/               # C4 L1 product framing
├── system-context/        # C4 L1 actors and consumers
├── containers/            # C4 L2 deployable units
├── components/            # C4 L3 component catalogue
└── behavior/
    └── gherkin/           # Gherkin feature files
        └── links/
```

## Status

`test:unit` (`cargo test --lib`) exercises the `links` module directly via Rust unit tests; no
Cucumber/Gherkin runner is wired up for this crate yet — `specs:behavior:coverage` is an `echo`
placeholder until that lands.

- [Behavior — rust-commons](./behavior/README.md)
- [Components — rust-commons](./components/README.md)
- [Containers — rust-commons](./containers/README.md)
- [Product — rust-commons](./product/README.md)
- [System Context — rust-commons](./system-context/README.md)
