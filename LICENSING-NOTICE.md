# Licensing Notice

This repository is licensed under the **MIT License**. All code, documentation, governance
materials, AI agent configuration, specifications, and tests in this repository are MIT-licensed
unless a subdirectory `LICENSE` file states otherwise.

## License Structure

The root [LICENSE](./LICENSE) is MIT. Selected product app directories and `specs/` carry
their own MIT `LICENSE` file — these override the root for files in that subtree. All
per-directory LICENSE files currently contain identical MIT text; the override mechanism is
preserved so future maintainers can relicense specific subdirectories independently if needed.
E2E test suites (`apps/*-e2e/`) do not carry per-directory LICENSE files and fall back to the
root LICENSE. See
[Licensing Convention](./repo-governance/conventions/structure/licensing.md) for the complete
exemption list.

## What This Means

Under the MIT License, you are free to:

- Use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the software
- Use the code for any purpose — commercial, educational, research, personal, or otherwise
- Fork and build competing products without restriction

The only requirement is that the copyright notice and permission notice be included in all copies
or substantial portions of the software.

## Third-Party Code

No third-party or forked code is currently vendored in this repository — all code is first-party
and MIT-licensed. If third-party code is vendored in the future, it retains its original license
(not this repository's MIT license), and the applicable terms are recorded in a `LICENSE` file
within the relevant subdirectory.

The root [`hippo`](./hippo) release bootstrap and its hermetic consumer test were adapted from the
MIT-licensed BeaverNest repository at commit
[`584ab5a`](https://github.com/wahidyankf/beaver-nest/commit/584ab5af21b272eea6e09fa329f8a5d53e10603c).
Copyright remains `2026 wahidyankf` under that repository's MIT license. OSE changes only its
consumer mappings and integration checks. The HIPPO executable is downloaded from checksum-pinned
[upstream releases](https://github.com/wahidyankf/hippo/releases) into an external cache; neither
the executable nor HIPPO source is vendored here.

## More Information

- [Root license text](./LICENSE)
- [MIT License — Open Source Initiative](https://opensource.org/licenses/MIT)
- [Why MIT? — docs/explanation/software-engineering/licensing/mit-license-rationale.md](./docs/explanation/software-engineering/licensing/mit-license-rationale.md)
