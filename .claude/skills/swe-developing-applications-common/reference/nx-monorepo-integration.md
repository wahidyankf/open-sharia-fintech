# Common Development Workflow — Nx Monorepo Integration

## Repository Structure

This platform uses **Nx** for monorepo management with clear separation of concerns:

**Apps** (`apps/[app-name]`):

- Deployable applications
- Import libraries but never export
- Each independently deployable
- Never import other apps

**Libraries** (`libs/[lib-name]`):

- Reusable code modules
- Flat structure (no nesting)
- Can import other libraries (no circular dependencies)
- Naming convention: `[language]-[name]` (e.g., `ts-env-loader`, `rust-commons`, `fsharp-env-loader`)

## Common Nx Commands

All target names follow [Nx Target Standards](../../../../repo-governance/development/infra/nx-targets.md). Use canonical names: `dev` (not `serve`), `test:quick` (not `test`), `start` (not `serve` for production).

**Development**:

```bash
nx dev [project-name]       # Start development server (use 'dev', not 'serve')
nx start [project-name]     # Start production server (use 'start', not 'serve')
```

**Building**:

```bash
nx build [project-name]     # Build specific project
nx affected -t build        # Build only affected projects
```

**Testing**:

```bash
nx run [project-name]:test:quick        # Fast pre-push quality gate (mandatory for all projects)
nx run [project-name]:test:unit         # Isolated unit tests
nx run [project-name]:test:integration  # Tests requiring external services
nx run [project-name]:test:e2e          # End-to-end tests (run via scheduled cron, not pre-push)
nx affected -t test:quick               # Run quality gate for affected projects
```

**Analysis**:

```bash
nx graph                   # Visualize dependencies
nx affected:graph          # Show affected dependency graph
```

**Affected Commands Philosophy**:

- After making changes, use `nx affected:*` commands
- Only builds/tests projects impacted by your changes
- Efficient in large monorepo (don't rebuild everything)

## Monorepo Best Practices

1. **Keep libraries focused**: Each library should have single responsibility
2. **Avoid circular dependencies**: Libraries form directed acyclic graph (DAG)
3. **Use affected commands**: Leverage Nx's smart rebuilding
4. **Apps never depend on apps**: Only libraries are shared
5. **Test at library level**: Unit test libraries, integration test apps
