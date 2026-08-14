# Common Mistakes

## Mistake 1: Missing acceptance criteria

**Wrong**: Plan without Gherkin scenarios
**Right**: Every plan has concrete acceptance criteria

## Mistake 2: Vague requirements

**Wrong**: "Improve system performance"
**Right**: "Reduce API response time to <200ms for 95th percentile"

## Mistake 3: No progress tracking

**Wrong**: Never updating delivery checklist
**Right**: Mark items complete with implementation notes

## Mistake 4: Wrong folder placement

**Wrong**: Active work in backlog/
**Right**: Move to in-progress/ when starting work

## Mistake 5: Code delivery items without TDD shape

**Wrong**: Combining implementation and test into one checkbox

```markdown
- [ ] Implement email validation with tests
```

**Right**: Separate RED, GREEN, REFACTOR phases as independent checkboxes

```markdown
- [ ] **RED**: Write failing test for email validation in `libs/ts-utils/src/validation.test.ts`
      — command: `nx run ts-utils:test:unit`
      — acceptance: test fails with "validateEmail is not defined"
- [ ] **GREEN**: Implement `validateEmail` in `libs/ts-utils/src/validation.ts`
      — command: `nx run ts-utils:test:unit`
      — acceptance: test passes, no other tests broken
- [ ] **REFACTOR**: Extract regex constant, improve naming
      — command: `nx run ts-utils:test:unit`
      — acceptance: all tests still pass
```

`plan-checker` flags combined TDD items as HIGH severity findings.
