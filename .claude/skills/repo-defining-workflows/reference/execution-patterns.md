# Execution Patterns

## Sequential Execution

**When**: Steps depend on previous results.

```markdown
1. maker creates content
2. checker validates content (uses maker output)
3. fixer applies fixes (uses checker findings)
```

## Parallel Execution

**When**: Steps are independent and can run simultaneously.

```markdown
Run in parallel:

- checker-1 validates docs
- checker-2 validates code
- checker-3 validates configs

Combine results after all complete.
```

## Conditional Execution

**When**: Different paths based on conditions.

```markdown
If validation passes:

- Deploy to production
  Else:
- Create issue with findings
- Notify team
```

## Mixed Patterns

Combine sequential, parallel, and conditional:

```markdown
1. Run maker (sequential)
2. Run checkers in parallel:
   - checker-1
   - checker-2
3. Wait for all checkers
4. Conditional:
   If critical issues found:
   - STOP
   - Report to user
     Else:
   - Run fixer (sequential)
   - Deploy
```
