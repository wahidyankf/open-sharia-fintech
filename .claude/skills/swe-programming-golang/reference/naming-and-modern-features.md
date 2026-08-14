# Go Quick Standards — Naming and Modern Features (Go 1.18+)

## Naming Conventions

**Packages**: lowercase, single word

- `http`, `json`, `user`, `payment`
- Avoid underscores

**Types and Functions**: MixedCaps

- Exported: `UserAccount`, `CalculateTotal()`
- Unexported: `userAccount`, `calculateTotal()`

**Variables**: Short names in limited scope

- `i`, `j` for loop counters
- `r` for reader, `w` for writer
- Descriptive names for package-level: `defaultTimeout`

**Constants**: MixedCaps (not UPPER_CASE)

- `MaxRetries`, `DefaultTimeout`

## Modern Go Features (Go 1.18+)

**Generics**: Use for type-safe data structures

```go
func Map[T, U any](slice []T, f func(T) U) []U {
    result := make([]U, len(slice))
    for i, v := range slice {
        result[i] = f(v)
    }
    return result
}
```

**Error Wrapping**: Always `%w` for error args in `fmt.Errorf` — `errorlint` linter enforces:

```go
if err != nil {
    return fmt.Errorf("failed to process user: %w", err) // %w preserves chain
}
// Never: fmt.Errorf("...%v", err) — errorlint violation
```

**Error Comparison**: Always `errors.Is`/`errors.As` — `errorlint` linter enforces:

```go
if errors.Is(err, io.EOF) { ... }   // NOT: err == io.EOF

var exitErr *exec.ExitError
if errors.As(err, &exitErr) { ... } // NOT: err.(*exec.ExitError)
```

**Sealed-Interface Sum Types**: Use `//sumtype:decl` + `gochecksumtype` for exhaustive type switches:

```go
//sumtype:decl
type MyStatus interface {
    isMyStatus()
    Code() string
    String() string
}
type StatusA struct{}
func (StatusA) isMyStatus()   {}
func (StatusA) Code() string  { return "a" }
func (StatusA) String() string { return "a" }

// gochecksumtype enforces exhaustive coverage:
switch s.(type) {
case StatusA:
    // ...
}
```

**Const-Block Hygiene**: `iotamixing` forbids mixing `iota` constants with literal constants in the
same `const` block — split them into separate blocks.

**Doc Comments** — `godot` + `revive exported` + `revive package-comments` enforce:

```go
// Package doctor checks required development tools are installed.
package doctor

// Execute runs the root cobra command, writing errors to stderr and exiting on failure.
func Execute() { ... }

// DefaultMaxSize is the maximum allowed file size for env backup inclusion (1 MB).
const DefaultMaxSize = 1024 * 1024

// Code implements ToolStatus.
func (StatusOK) Code() string { return "ok" }
```

Rules:

- First line = identifier name + verb + object + period (`godot`)
- Imperative mood for functions: "Execute runs…" not "This runs…"
- Interface implementations: `// Code implements [InterfaceName].`
- `String()` (fmt.Stringer): optional — recognized as stdlib interface
- Unexported identifiers: no linter, code-review only
- Package main: `// Package main is the entry point for [tool name].`

**Struct Embedding**: Use for composition

```go
type User struct {
    BaseModel
    Name string
}
```
