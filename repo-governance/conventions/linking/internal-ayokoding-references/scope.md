---
description: What this convention covers (docs/ to apps/ayokoding-www/ relative linking) and what it explicitly excludes.
when_to_use: Use when checking whether a specific linking scenario falls inside or outside this convention's coverage.
---

# Scope

## What This Convention Covers

- **docs/ → apps/ayokoding-www/** - Linking from documentation to AyoKoding educational content
- **Relative path calculation** - How to determine correct `../` depth
- **URL pattern recognition** - Identifying when to use relative paths vs external URLs
- **Path examples by location** - Common linking scenarios and correct paths
- **Enforcement mechanisms** - Manual review and automated validation

## What This Convention Does NOT Cover

- **General markdown linking** - Covered by [Linking Convention](../../formatting/linking.md)
- **ayokoding-www internal navigation** - Covered by [Programming Language Content Standard](../../tutorials/programming-language-content.md)
- **External web resources** - Public URLs to third-party sites (Stack Overflow, GitHub, etc.)
- **Cross-repository references** - Links to content in separate git repositories
- **apps/ayokoding-www/ → docs/** - Reverse direction (educational content linking to docs)
