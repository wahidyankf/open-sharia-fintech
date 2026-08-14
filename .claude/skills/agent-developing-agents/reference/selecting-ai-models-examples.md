# Developing AI Agents — Selecting AI Models: Matrix and Examples

## Model Selection Matrix

| Task Type          | Complexity  | Reasoning Required          | Recommended Model |
| ------------------ | ----------- | --------------------------- | ----------------- |
| Content creation   | High        | Yes (narrative, structure)  | **Sonnet**        |
| Factual validation | High        | Yes (source evaluation)     | **Sonnet**        |
| Quality assessment | High        | Yes (subjective judgment)   | **Sonnet**        |
| Fix application    | Medium-High | Yes (confidence assessment) | **Sonnet**        |
| Link checking      | Low         | No (exists/accessible)      | **Haiku**         |
| File operations    | Low         | No (read/write/move)        | **Haiku**         |
| Pattern extraction | Low         | No (regex matching)         | **Haiku**         |
| Cache management   | Low         | No (read/write/compare)     | **Haiku**         |

## Agent-Specific Examples

### Sonnet Examples

**docs-checker** (Complex validation):

```yaml
model: sonnet
```

**Reasoning**:

- Analyzes technical claims for contradictions
- Deep web research for fact verification
- Pattern recognition across multiple files
- Complex decision-making for criticality levels
- Multi-step validation orchestration

**docs-fixer** (Sophisticated analysis):

```yaml
model: sonnet
```

**Reasoning**:

- Re-validates findings to detect false positives
- Distinguishes objective errors from subjective improvements
- Assesses confidence levels (HIGH/MEDIUM/FALSE_POSITIVE)
- Complex decision-making for fix safety
- Trust model analysis (when to trust checker)

**docs-tutorial-checker** (Pedagogical analysis):

```yaml
model: sonnet
```

**Reasoning**:

- Evaluates narrative flow and learning progression
- Assesses hands-on element quality
- Analyzes visual completeness
- Determines tutorial type compliance
- Sophisticated quality judgment

### Haiku Examples

**docs-link-checker** (Straightforward validation):

```yaml
model: haiku
```

**Reasoning**:

- Pattern matching to extract URLs
- Sequential URL validation via requests
- File existence checks for internal references
- Cache management (read/write YAML, compare dates)
- Simple status reporting (working/broken/redirected)
- No complex reasoning required

**docs-file-manager** (File operations):

```yaml
model: haiku
```

**Reasoning**:

- Straightforward file operations (move, rename, delete)
- Simple path manipulation
- Git history preservation (scripted commands)
- No complex decision-making
- Deterministic outcomes
