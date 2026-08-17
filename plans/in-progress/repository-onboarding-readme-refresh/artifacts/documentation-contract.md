# Reader Documentation Contract

## Source of Truth

| Subject                                 | Authority                                                        |
| --------------------------------------- | ---------------------------------------------------------------- |
| Product purpose and audience path       | `prd.md`                                                         |
| Repository topology and technical facts | `tech-docs.md` and the owning repository's tracked configuration |
| Delivery safety and task ownership      | `delivery.md` and the owning execution record                    |
| GitHub About metadata                   | `prd.md` exact metadata table                                    |

## Voice and Reader Path

Start with the product purpose. Write for product people and early-career engineers: explain
unfamiliar terms when first used, use direct active language, and use emojis only where they improve
navigation or recognition. Do not clone one repository opening into another.

| Repository    | First Reader Path                               | First Local Success      |
| ------------- | ----------------------------------------------- | ------------------------ |
| `ose-public`  | Understand the product, then run OSE locally    | `ose-www`                |
| `ose-private` | Understand CoralPolyp, then use a local sandbox | CoralPolyp local sandbox |

`ose-primer` is not covered by this contract — it left the parity set on 2026-08-16 and carries no
sync obligation.

macOS and Ubuntu are supported. WSL2 may work but is not supported or verified. External
contributions are closed: docs may explain the internal AI delivery route but do not invite outside
contribution or promise a response time.

## Safety Boundary

Never read, write, quote, or commit real `.env*` files or values. Public artifacts may not contain
private paths, topology, hostnames, credentials, account details, or raw private command output.
Use only tracked examples, placeholders, variable names, path-free summaries, and opaque digests.
