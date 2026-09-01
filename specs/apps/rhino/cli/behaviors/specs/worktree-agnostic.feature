@worktree-agnostic
Feature: worktree-agnostic guardrail execution

  As a developer working in a git worktree
  I want rhino-cli guardrails to resolve paths relative to the worktree toplevel
  So that pre-commit checks work correctly from linked worktrees

  @unit
  Scenario: A regression test locks worktree-safe execution
    Given a synthetic linked worktree in the rhino-cli test suite
    When a guardrail command runs inside it
    Then it resolves to the worktree's own toplevel and exits successfully
