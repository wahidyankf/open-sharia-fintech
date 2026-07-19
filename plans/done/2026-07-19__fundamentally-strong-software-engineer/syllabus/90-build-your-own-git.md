# 90 · Build Your Own Git (By Example, Python †)

**prd row**: Pass 5 · Internals & Lead at Altitude · By Example · Python † · Learn 190 / Drill 290 ·
Nvim-ready Yes · VSCode-ready Yes. ([prd canonical table](../prd.md#the-94-topics--canonical-table-spiral-order-identical-in-both-tracks))

**Scope note**: demystify Git by rebuilding its core — the content-addressed object store
(blobs/trees/commits), refs, the index/staging area, and the everyday commands `commit`/`log`/`checkout`
— written against a real `.git` directory so your reimplementation and the real `git` binary can read
each other's output. This is the build-your-own tier of [`06-version-control-and-git`](./06-version-control-and-git.md):
that topic taught the object-model intuition and the CLI; here you make it concrete by implementing it.
`†`: Python, fully type-annotated (DD-39), verified with `pytest`.

## Why this exists · the big idea

- **The problem before the solution**: Git feels like magic — a fast, distributed, tamper-evident history
  — and that mystery makes it scary to use fully and easy to misuse; the "solution" is to stop treating it
  as a black box and rebuild the handful of ideas underneath, at which point the whole tool becomes obvious.
- **Keep-this-if-you-forget-everything**: Git is a content-addressed key-value store with a thin porcelain
  on top — every object is named by the hash of its content, commits point to trees point to blobs, and
  refs are just named pointers into that graph. Once you see that, branches, merges, and history stop being
  mysterious.
- **Big ideas touched**: `abstraction-and-its-cost` (Git's porcelain hides the object model; rebuilding the
  plumbing shows what the leverage costs and where it leaks — detached HEAD, dangling objects),
  `layering-and-leaks` (blobs → trees → commits → refs is a clean layered stack, and the index is the layer
  that most surprises people until you build it).

## Prerequisites

- **Prior topics**: [topic 6 Version Control & Git](./06-version-control-and-git.md) (the object-model
  intuition — commits/trees/blobs/refs — and everyday CLI fluency this topic makes concrete) and
  [topic 4 Just Enough Python](./04-just-enough-python.md) (the implementation language).
- **Tools & environment**: a macOS/Linux terminal; **Python 3.x** with type hints (pyright-clean spirit, DD-39);
  `pytest`; the real **`git`** binary installed so you can cross-check your objects against genuine ones;
  Neovim/VSCode with the Python LSP (DD-17).
- **Assumed knowledge**: Git's object model and the porcelain commands (topic 06); Python classes, files,
  and bytes handling (topic 04); hashing intuition (topic 07/17).

## Accuracy notes (web-verified)

> Verified in the pre-authoring `web-researcher` sweep (#48, DD-28).

- 2026-07-12 — verified: Git's on-disk model — zlib-compressed, SHA-named loose objects under
  `.git/objects`, the `blob`/`tree`/`commit` object headers, refs as files under `.git/refs`, and the
  index format — is stable and correctly left version-unpinned. The reimplementation targets loose objects
  and the index; packfiles are an optional stretch, not required for a readable clone.
- 2026-07-12 — verified (GAP for plan owner): Git is mid-transition from SHA-1 to SHA-256 object naming.
  Build against the repository's default hash (SHA-1 for compatibility with a stock `git init`) and note
  SHA-256 as the forward direction — keep the hash algorithm a named parameter rather than hard-coded.
  (git-scm.com/docs, hash-function-transition)

### DD-35 primary-source citations (fetched-and-read)

Every format, version, and behaviour claim below traces to a primary source fetched and read during
grounding. Unverifiable specifics are marked `[Needs Verification]` and never shipped as fact.

- **Four object types** — `blob`, `tree`, `commit`, `tag` — each stored as a loose object: the payload is
  prefixed with a header `"<type> <size>\0"`, then the whole thing is **zlib-deflated** and written to
  `.git/objects/<first-2-hex>/<remaining-38-hex>`. (git-scm.com/book/en/v2/Git-Internals-Git-Objects, git-scm.com/docs/gitformat-loose)
- **Object name** = the hash of the _uncompressed_ `header + payload`. Default is **SHA-1** for a stock
  `git init`; **SHA-256** is the forward transition. Keep the hash algorithm a **named parameter**, never
  hard-coded. (git-scm.com/docs/hash-function-transition)
- **Tree entries** are `"<mode> <name>\0" + <raw-20-byte-hash>` (SHA-1); modes `100644` (file), `100755`
  (executable), `040000` (subtree), `120000` (symlink), `160000` (gitlink). (git-scm.com/docs/gitformat-loose, Pro Git Git-Objects)
- **Commit object** payload lists `tree <hash>`, zero-or-more `parent <hash>`, `author`/`committer` lines
  (name, email, epoch seconds, timezone), a blank line, then the message. (git-scm.com/book Git-Objects)
- **Refs** are files under `.git/refs/` holding a 40-hex object name; **`HEAD`** is a **symbolic ref**
  (`ref: refs/heads/<branch>`), or a raw hash when **detached**. (git-scm.com/docs/gitrepository-layout)
- **The index** is `.git/index` — a binary file with the `DIRC` ("dircache") signature, a version, and a
  sorted list of staged entries; it sits between the working tree and the next commit.
  (git-scm.com/docs/gitformat-index)
- **Git 2.55.0** is the current stable release used to cross-check objects; treat the exact patch as
  `[Needs Verification]` at authoring — the on-disk formats above are stable regardless. (github.com/git/git/tags)
- **Implementation language** — Python **fully type-annotated** (DD-39), tested with **pytest**; every
  object written is cross-checked against the real `git` binary (`git cat-file`, `git ls-tree`, `git log`).

## Concepts

<!-- co-01 · concept enumeration (DD-34): every concept this topic teaches, 1:1-mirrored to a delivery.md checkbox. Floor ≥ 10 (subject). Each example below cites the co-NN it exercises. -->

- **co-01 · content-addressing** — every object is named by the hash of its content; identical content dedups.
- **co-02 · sha-hashing** — the object name is a SHA hash (SHA-1 default, SHA-256 forward transition).
- **co-03 · blob-object** — a `blob` stores raw file content with a `"blob <size>\0"` header.
- **co-04 · tree-object** — a `tree` stores a directory snapshot: mode + name + child hash per entry.
- **co-05 · commit-object** — a `commit` binds a tree, parents, author/committer, and a message.
- **co-06 · tag-object** — an annotated `tag` is the fourth object type, pointing at another object.
- **co-07 · object-header** — every loose object is prefixed with `"<type> <size>\0"` before hashing.
- **co-08 · zlib-compression** — loose objects are zlib-deflated on disk.
- **co-09 · loose-object-path** — the object lives at `.git/objects/<first-2>/<remaining-38>` hex.
- **co-10 · hash-object** — the plumbing that writes an object and returns its hash.
- **co-11 · cat-file** — the plumbing that reads an object's type, size, and content back.
- **co-12 · tree-serialization** — encoding tree entries as `"<mode> <name>\0" + raw-hash`.
- **co-13 · tree-parse** — decoding a tree object's bytes back into entries.
- **co-14 · commit-serialization** — encoding the tree/parent/author/committer/message lines.
- **co-15 · commit-parent** — parent pointers form the history DAG (one parent, or many for a merge).
- **co-16 · refs** — refs are files under `.git/refs` holding an object name.
- **co-17 · head** — `HEAD` names the current commit/branch.
- **co-18 · symbolic-ref** — `HEAD` is a symbolic ref (`ref: refs/heads/<branch>`).
- **co-19 · branch** — a branch is a ref under `refs/heads/` that moves as you commit.
- **co-20 · index-format** — `.git/index` (`DIRC`) stores the sorted list of staged entries.
- **co-21 · staging** — adding a file writes a blob and records an index entry.
- **co-22 · index-to-tree** — `write-tree` turns the index into a tree object.
- **co-23 · commit-porcelain** — `commit` snapshots the index into a commit and advances the branch.
- **co-24 · log-walk** — `log` walks the parent chain from `HEAD` backward.
- **co-25 · checkout** — `checkout` materializes a tree into the working directory and moves `HEAD`.
- **co-26 · git-interop** — objects are byte-compatible: real `git` reads yours and you read its.
- **co-27 · detached-head** — `HEAD` can point straight at a commit, off any branch.
- **co-28 · dangling-objects** — objects reachable from no ref are dangling (candidates for gc).
- **co-29 · hash-algo-parameter** — the hash algorithm (SHA-1/SHA-256) is a parameter, not hard-coded.
- **co-30 · pytest-stages** — `pytest` covers each stage (objects, refs, index, porcelain, interop).

## Tensions & trade-offs — when NOT to reach for this

- **Building the plumbing vs trusting the porcelain**: reimplementing Git's object store teaches exactly
  what sits under `commit`/`log`/`checkout`, but a working engineer should still use the real `git` binary
  day to day — this topic is understanding-for-judgment, not a recommendation to replace Git with a
  hand-rolled reimplementation.
- **SHA-1 vs SHA-256 object naming**: building against the default SHA-1 keeps the implementation
  compatible with a stock `git init` and every existing repository, but SHA-1 is the outgoing algorithm —
  treating the hash algorithm as a named parameter (co-29) rather than hard-coding it is what keeps the
  reimplementation honest about that transition instead of silently locking in a deprecated choice.
- **When NOT to use it**: don't over-invest in packfile/delta-compression internals here — loose objects
  and the index are enough to demystify the object model and interoperate with real `git`; packfiles are
  explicitly a stretch, not the done bar, because chasing them trades the topic's actual payoff
  (understanding) for reimplementing an optimization.

## Lineage — why it beat the alternative

- Before Git, version control (CVS, then Subversion) tracked file-by-file deltas against a central
  server, so history was a series of diffs and most operations needed a network round-trip. Git's
  content-addressed object model — every blob/tree/commit named by the hash of its content, with commits
  forming a DAG of pointers rather than a linear diff chain — won because it makes the entire history
  locally available, tamper-evident (any change to a past object changes its hash and every hash after
  it), and trivially distributable (two repositories with the same object graph are the same history, no
  server required). Rebuilding that model here is what turns
  [`06-version-control-and-git`](./06-version-control-and-git.md)'s porcelain commands from memorized
  incantations into a graph you can reason about directly.

## Worked examples

Colocated under `build-your-own-git/learning/code/`; Python (fully type-annotated, DD-39) + `pytest`
(DD-20/DD-30/DD-39). Every object your code writes is cross-checked against the real `git` binary. Contiguous
`ex-01..ex-78`. Every example cites the `co-NN` it exercises. Concepts come before examples.

### Beginner

- **ex-01 · init-git-dir** — create a minimal `.git/` (objects, refs, HEAD) — verify a stock `git status` accepts it. (co-09)
- **ex-02 · blob-header-format** — build `b"blob " + size + b"\0" + content` — verify the header bytes. (co-07, co-03)
- **ex-03 · sha1-of-blob** — compute the SHA-1 of the headered blob — verify it matches `git hash-object`. (co-02, co-01)
- **ex-04 · zlib-compress-object** — zlib-deflate the object — verify it round-trips through inflate. (co-08)
- **ex-05 · write-loose-object** — write to `.git/objects/<ab>/<cdef...>` — verify the file lands at the right path. (co-09, co-10)
- **ex-06 · hash-object-cmd** — a `hash-object` equivalent returning the hash — verify the hash. (co-10)
- **ex-07 · cross-check-real-git** — compare your hash to `git hash-object` on the same input — verify they match. (co-26)
- **ex-08 · read-loose-object** — inflate and strip the header — verify the payload. (co-11, co-08)
- **ex-09 · cat-file-p** — a `cat-file -p` equivalent — verify it prints the content. (co-11)
- **ex-10 · cat-file-t** — print the object type — verify `blob`. (co-11, co-07)
- **ex-11 · cat-file-s** — print the object size — verify the byte count. (co-11)
- **ex-12 · real-git-cat-file** — `git cat-file -p <your-hash>` — verify real git reads your object. (co-26)
- **ex-13 · content-address-dedup** — hash two identical contents — verify the same hash results. (co-01)
- **ex-14 · blob-roundtrip** — write then read a blob — verify content survives. (co-03, co-10, co-11)
- **ex-15 · object-path-split** — split a hash into `<2>/<38>` — verify the directory sharding. (co-09)
- **ex-16 · hash-algo-param-sha1** — pass SHA-1 as the algorithm parameter — verify default behaviour. (co-29, co-02)
- **ex-17 · hash-algo-param-sha256** — pass SHA-256 — verify a 64-hex object name. (co-29, co-02)
- **ex-18 · empty-blob** — hash an empty file — verify it equals git's empty-blob hash. (co-03)
- **ex-19 · pytest-blob** — a `pytest` over blob write/read — verify it passes. (co-30)
- **ex-20 · pytest-hash-match** — a `pytest` asserting your hash equals git's — verify it passes. (co-30, co-26)
- **ex-21 · tree-entry-format** — encode `"100644 name\0" + raw-hash` — verify the entry bytes. (co-12)
- **ex-22 · tree-object-header** — prefix a tree with `"tree <size>\0"` — verify the header. (co-07, co-04)
- **ex-23 · write-tree-single** — a tree of one blob — verify it writes and hashes. (co-04, co-12)
- **ex-24 · tree-sha** — hash the tree — verify it matches `git write-tree`. (co-02, co-04)
- **ex-25 · real-git-ls-tree** — `git ls-tree <your-tree>` — verify real git lists your entries. (co-26, co-04)
- **ex-26 · typed-object-model** — a fully type-annotated object dataclass — verify `pyright`-clean typing. (co-03)

### Intermediate

- **ex-27 · tree-multiple-blobs** — a tree with several files — verify all entries present and sorted. (co-04, co-12)
- **ex-28 · nested-tree** — a subdirectory as a sub-tree entry — verify the nested hash resolves. (co-04)
- **ex-29 · parse-tree-bytes** — decode a tree object back to entries — verify the parse. (co-13)
- **ex-30 · tree-mode-file** — a `100644` entry — verify the mode. (co-12)
- **ex-31 · tree-mode-dir** — a `040000` subtree entry — verify the mode. (co-12)
- **ex-32 · tree-mode-exec** — a `100755` executable entry — verify the mode. (co-12)
- **ex-33 · commit-object-format** — encode `tree`/`author`/`committer`/message — verify the bytes. (co-14, co-05)
- **ex-34 · write-commit-no-parent** — a root commit (no parent) — verify it writes. (co-05, co-14)
- **ex-35 · commit-with-parent** — add a `parent <hash>` line — verify the parent linkage. (co-15)
- **ex-36 · commit-sha** — hash the commit — verify it matches `git commit-tree`. (co-02, co-05)
- **ex-37 · real-git-log-shows-commit** — point a ref at your commit and run `git log` — verify it appears. (co-26, co-05)
- **ex-38 · commit-multi-parent** — a merge commit with two parents — verify both parent lines. (co-15)
- **ex-39 · ref-write** — write `refs/heads/main` — verify the file holds the object name. (co-16)
- **ex-40 · ref-read** — read a ref back — verify the hash. (co-16)
- **ex-41 · head-symbolic** — `HEAD` as `ref: refs/heads/main` — verify it resolves through. (co-17, co-18)
- **ex-42 · head-update-on-commit** — committing moves the branch ref — verify the ref advanced. (co-16, co-19)
- **ex-43 · branch-create** — create a new `refs/heads/<name>` — verify the branch. (co-19)
- **ex-44 · resolve-ref** — resolve `HEAD` → branch → commit — verify the chain. (co-17, co-16)
- **ex-45 · detached-head** — set `HEAD` to a raw commit hash — verify detached state. (co-27)
- **ex-46 · commit-author-timestamp** — author/committer with epoch + timezone — verify the format. (co-14)
- **ex-47 · tag-object-format** — an annotated tag object — verify it points at a commit. (co-06)
- **ex-48 · lightweight-tag** — a ref-only tag under `refs/tags` — verify it resolves. (co-16, co-06)
- **ex-49 · dangling-object** — write an object referenced by nothing — verify `git fsck` reports it dangling. (co-28)
- **ex-50 · pytest-commit** — a `pytest` over commit write — verify it passes. (co-30, co-05)
- **ex-51 · pytest-ref** — a `pytest` over a ref update — verify it passes. (co-30, co-16)
- **ex-52 · pytest-tree-parse** — a `pytest` over tree parsing — verify it passes. (co-30, co-13)

### Advanced

- **ex-53 · index-format-header** — write the `DIRC` signature + version — verify the header. (co-20)
- **ex-54 · index-entry** — encode one staged index entry — verify the entry fields. (co-20, co-21)
- **ex-55 · add-file-to-index** — stage a file (blob + index entry) — verify it appears staged. (co-21)
- **ex-56 · index-read** — parse `.git/index` — verify the entry list. (co-20)
- **ex-57 · index-write** — serialize the index back — verify byte round-trip. (co-20)
- **ex-58 · real-git-status-reads-index** — run `git status` on your index — verify it shows your staged file. (co-26, co-20)
- **ex-59 · write-tree-from-index** — turn the index into a tree — verify it matches `git write-tree`. (co-22)
- **ex-60 · staged-multiple** — stage several files — verify all are in the index. (co-21)
- **ex-61 · update-staged-file** — restage a modified file — verify the index entry updates. (co-21)
- **ex-62 · commit-porcelain** — `commit` from the index — verify a commit object is produced. (co-23)
- **ex-63 · commit-updates-head** — commit advances `HEAD`'s branch — verify the ref moved. (co-23, co-17)
- **ex-64 · log-walk-linear** — walk a single-parent chain — verify order newest-first. (co-24)
- **ex-65 · log-walk-merge** — walk history with a merge — verify both ancestries reached. (co-24, co-15)
- **ex-66 · log-format** — print `<sha> <message>` per commit — verify the output. (co-24)
- **ex-67 · checkout-tree** — materialize a tree to the working dir — verify files written. (co-25)
- **ex-68 · checkout-updates-working** — checkout replaces working files — verify contents match the tree. (co-25)
- **ex-69 · checkout-updates-head** — checkout moves `HEAD` — verify `HEAD` points at the target. (co-25, co-17)
- **ex-70 · full-cycle-add-commit-checkout** — add → commit → checkout — verify the round-trip. (co-21, co-23, co-25)
- **ex-71 · interop-git-reads-full-history** — `git log` over your full history — verify identical history. (co-26, co-24)
- **ex-72 · interop-you-read-git-commit** — parse a commit written by real `git` — verify your parser agrees. (co-26, co-14)
- **ex-73 · sha256-repo** — build against a `--object-format=sha256` repo — verify 64-hex names interop. (co-29, co-02)
- **ex-74 · gc-find-dangling** — enumerate objects reachable from no ref — verify the dangling set. (co-28)
- **ex-75 · detached-head-commit** — commit while `HEAD` is detached — verify `HEAD` (not a branch) advanced. (co-27, co-23)
- **ex-76 · pytest-full-cycle** — a `pytest` over add → commit → checkout — verify it passes. (co-30)
- **ex-77 · pytest-interop** — a `pytest` cross-checking objects with real `git` — verify it passes. (co-30, co-26)
- **ex-78 · capstone-mini-git** — the capstone: an interoperable mini-Git (objects + refs + index + porcelain) — verify end-to-end + real-git interop + green tests. (co-01, co-05, co-20, co-25, co-26)

## Capstone spec — intra-topic (subject → full runnable)

- **Goal**: build a minimal but interoperable Git — a content-addressed object store (blobs/trees/commits),
  refs and `HEAD`, an index, and the `commit`/`log`/`checkout` porcelain — that reads and writes a real
  `.git` directory, so your implementation and the stock `git` binary can consume each other's objects,
  fully covered by `pytest`.
- **Concepts exercised**: [ ] hash-object + cat-file plumbing (co-10, co-11) [ ] blob/tree serialization
  (co-03, co-04, co-12) [ ] commit objects with parents (co-05, co-14, co-15) [ ] refs + `HEAD` (co-16,
  co-17, co-18) [ ] an index/staging area (co-20, co-21, co-22) [ ] `commit`/`log`/`checkout` porcelain
  (co-23, co-24, co-25) [ ] cross-interop with the real `git` (co-26) [ ] `pytest` coverage of each stage
  (co-30).
- **Ordered steps**:
  1. `.../learning/capstone/code/objects.py` — hash, write, and read `blob`/`tree`/`commit` objects to
     `.git/objects`. Verify the real `git cat-file -p` prints your objects correctly (tests).
  2. `refs.py` + `index.py` — refs/`HEAD` as pointers and an index that stages blobs. Verify staging a file
     records it in the index and a ref update moves `HEAD` (tests).
  3. `porcelain.py` — `commit`, `log` (walk parents), and `checkout` (materialize a tree). Verify an
     add → commit → checkout cycle round-trips and `git log` on the same repo shows the identical history.
- **Acceptance criteria**: objects are byte-compatible with the real `git` (it can read yours, you can read
  its); refs/`HEAD`/index behave; the commit graph walks correctly; checkout materializes the right tree;
  `pytest` covers each stage.
- **Done bar**: runnable end-to-end + interoperates with the real `git` + tests green + web-verified.

## Read more

**Books**

- **Pro Git** — Scott Chacon, Ben Straub (2nd ed., 2014). The official, comprehensive Git book, whose
  internals chapters (objects, refs, packfiles) are exactly what you reimplement here; freely licensed.
  <https://git-scm.com/book/en/v2>

**Papers & articles**

- **Write Yourself a Git!** — Thibault Polge. Free, widely cited tutorial that walks through implementing
  Git's core plumbing commands from scratch. <https://wyag.thb.lt/>
- **Git from the Bottom Up** — John Wiegley (2009). Early, influential free explainer of Git's object model
  and internals. <https://jwiegley.github.io/git-from-the-bottom-up/>

---

← Previous: [89 · Compilers, Parsers & Transpilers](./89-compilers-parsers-and-transpilers.md) · Next: [91 · Build Your Own Database](./91-build-your-own-database.md) →
