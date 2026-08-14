# Factual Validation — Source Prioritization

## Tier 1: Official Documentation (Highest Authority)

**Examples**:

- Official language documentation (docs.python.org, docs.oracle.com/javase)
- Official package documentation (npmjs.com package pages, PyPI)
- Official CLI references (git-scm.com, docs.npmjs.com)
- Official API documentation (developer.mozilla.org, official SDK docs)

**Characteristics**:

- Maintained by project creators
- Canonical source of truth
- Version-specific
- Updated with releases

**When to use**: For syntax, commands, API signatures, version numbers

## Tier 2: Package Registries (Version Truth)

**Examples**:

- npmjs.com (JavaScript/Node.js packages)
- pypi.org (Python packages)
- crates.io (Rust crates)
- rubygems.org (Ruby gems)
- maven.org (Java packages)

**Characteristics**:

- Authoritative version numbers
- Availability confirmation
- Dependency information
- Release dates

**When to use**: For version verification, package availability, dependency checks

## Tier 3: Official Release Notes (Change Truth)

**Examples**:

- GitHub Releases pages
- CHANGELOG.md files in official repos
- Official blog announcements
- Migration guides

**Characteristics**:

- Documents changes between versions
- Breaking change identification
- Deprecation notices
- Migration paths

**When to use**: For outdated content detection, breaking change verification

## Tier 4: Well-Maintained Community (Supplementary)

**Examples**:

- Stack Overflow accepted answers (with high votes)
- MDN Web Docs (Mozilla Developer Network)
- Official tutorial sites (RustByExample, GoByExample)

**Characteristics**:

- Community-verified
- Practical examples
- Context-dependent correctness
- May lag behind latest versions

**When to use**: For practical patterns, edge cases, when official docs insufficient
