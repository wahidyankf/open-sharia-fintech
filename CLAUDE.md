# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the **open-sharia-fintech** project - a fintech application built with Node.js. The project is in early stages with basic initialization completed.

## Environment Setup

The project uses **Volta** for Node.js and npm version management:

- **Node.js**: 24.11.1 (LTS)
- **npm**: 11.6.2

These versions are pinned in `package.json` under the `volta` field. When you run `npm` commands, Volta automatically ensures the correct versions are used.

## Project Structure

```
open-sharia-fintech/
├── docs/                 # Documentation (Diátaxis framework)
│   ├── tutorials/       # Learning-oriented guides
│   ├── how-to/          # Problem-oriented guides
│   ├── reference/       # Technical reference
│   └── explanation/     # Conceptual documentation
├── .husky/              # Git hooks (pre-commit, commit-msg)
├── package.json         # Node.js project manifest with Volta pinning
├── commitlint.config.js # Commitlint configuration
├── .gitignore          # Git ignore rules (Node.js and fintech)
└── README.md           # Project README
```

## Code Quality & Git Hooks

The project enforces code quality through automated git hooks managed by **Husky** and **lint-staged**:

### Pre-commit Hook (`.husky/pre-commit`)

Runs automatically before a commit is created:

1. **Lint-staged** selects staged files
2. **Prettier** formats matching files:
   - `*.{js,jsx,ts,tsx,mjs,cjs}` - JavaScript/TypeScript
   - `*.json` - JSON files
   - `*.md` - Markdown
   - `*.{yml,yaml}` - YAML
   - `*.{css,scss}` - Styles
   - `*.html` - HTML
3. Formatted files are automatically staged
4. Commit blocked if any issues found

### Commit-msg Hook (`.husky/commit-msg`)

Runs after pre-commit hook, before commit is finalized:

1. **Commitlint** validates the commit message
2. Checks against **@commitlint/config-conventional** rules
3. Rejects commit if format is invalid
4. Provides helpful error message

### Conventional Commits Rules

**Format:**

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

**Validation Rules:**

- `type` is REQUIRED and must be lowercase
- `scope` is OPTIONAL (recommended)
- `description` is REQUIRED (imperative mood, no period)
- First line (header) ≤ 50 characters
- Body lines (if present) ≤ 100 characters
- Blank line between header and body

**Valid types:** `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `chore`, `ci`, `revert`

**Valid examples:**

- `feat(auth): add login functionality`
- `fix: prevent race condition`
- `docs: update API documentation`
- `refactor(parser): extract common logic`

**Common errors:**

- Missing type: `⧗ type may not be empty`
- Empty description: `⧗ subject may not be empty`
- Line too long: `⧗ body's lines must not be longer than 100 characters`

## Common Development Commands

As the project develops, typical commands will include:

- `npm install` - Install dependencies
- `npm run build` - Build the project (to be configured)
- `npm test` - Run tests (to be configured)
- `npm run lint` - Lint code (to be configured)
- `npm run dev` - Start development server (to be configured)

## Documentation Organization

Documentation uses the [Diátaxis framework](https://diataxis.fr/):

- **Tutorials** (`docs/tutorials/`) - Learning-oriented guides
- **How-to Guides** (`docs/how-to/`) - Problem-solving guides
- **Reference** (`docs/reference/`) - Technical documentation
- **Explanation** (`docs/explanation/`) - Conceptual material

## Important Notes

- Do not stage or commit changes unless explicitly instructed. Per-request commits are one-time only
- The project license is MIT
- Claude Code settings files (`.claude/settings.local.json*`) are gitignored
- All commits must follow Conventional Commits format (enforced by commitlint)
