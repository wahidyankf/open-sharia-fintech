---
description: "Defines the cookbook directory structure, recipe file naming pattern, and category organization rules."
when_to_use: "Read when creating or naming a new recipe file or a new cookbook category."
---

# Recipe Organization and Naming

## Directory Structure

```
cookbook/
├── _index.md                          # Cookbook overview and navigation
├── setup/                             # Setup and configuration recipes
│   ├── recipe-01-install-dependencies.md
│   ├── recipe-02-configure-environment.md
│   └── ...
├── data/                              # Data manipulation recipes
│   ├── recipe-01-parse-csv.md
│   ├── recipe-02-parse-json.md
│   └── ...
├── network/                           # Network and HTTP recipes
├── concurrency/                       # Concurrency recipes
├── testing/                           # Testing recipes
├── performance/                       # Performance recipes
├── errors/                            # Error handling recipes
├── security/                          # Security recipes
└── database/                          # Database recipes
```

## Recipe Naming Convention

**Pattern**: `recipe-[NN]-[problem-identifier].md`

**Examples**:

- `recipe-01-read-csv-with-headers.md`
- `recipe-02-retry-failed-api-calls.md`
- `recipe-03-parse-json-unknown-schema.md`

**Requirements**:

- Sequential numbering within category (01, 02, 03...)
- Kebab-case problem identifier
- Descriptive enough to search
- No difficulty indicators in name

## Category Organization

**Each category should have**:

- 3-5 recipes minimum
- Clear category scope
- `_index.md` with category overview
- Logical grouping by problem domain

**Category selection criteria**:

- Common enough to warrant 3+ recipes
- Distinct from other categories
- Aligned with production problem domains
- Searchable/discoverable
