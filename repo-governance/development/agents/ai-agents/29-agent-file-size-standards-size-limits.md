---
title: "Agent File Size Standards — Size Limits by Agent Complexity"
description: "Defines the three agent complexity tiers and their target file-size limits."
category: explanation
subcategory: development
tags:
  - ai-agents
  - conventions
  - development
  - standards
created: 2025-11-23
when_to_use: Use when checking whether an agent definition file's size fits its complexity tier.
---

# Agent File Size Standards — Size Limits by Agent Complexity

## Size Limits by Agent Complexity

Agent files are organized into **three complexity tiers** with corresponding size guidelines. These limits balance agent capability with performance, maintainability, and clarity.

**Rationale**: Research shows LLMs follow ~150-200 instructions reliably, with quality degrading as count increases. While agents are only loaded when spawned (unlike AGENTS.md which is universally included), keeping them focused improves effectiveness.

### Tier 1: Simple Agents (Deployers, Specialized Operations)

**Target**: < 500 lines / < 15KB
**Warning**: 600 lines / 18KB
**Hard Limit**: 800 lines / 25KB

**Characteristics**:

- Single, straightforward responsibility
- Minimal decision logic
- Limited tool usage (typically Bash only for deployers)
- Few edge cases to handle
- Direct, linear workflows

**Examples**:

- apps-ayokoding-www-deployer (deployment automation)
- apps-ose-www-deployer (deployment automation)
- apps-organiclever-app-web-deployer (deployment automation)
- social-linkedin-post-maker (single-purpose content generation)
- repo-workflow-maker (workflow document creation)

**When to use this tier**:

- Agent performs one specific operation repeatedly
- Minimal validation or error handling needed
- Clear success/failure conditions
- No complex orchestration

### Tier 2: Standard Agents (Makers, Checkers, Validators)

**Target**: < 800 lines / < 25KB
**Warning**: 1,000 lines / 30KB
**Hard Limit**: 1,200 lines / 35KB

**Characteristics**:

- Moderate complexity with clear domain
- Multiple related responsibilities
- Comprehensive validation or creation logic
- Moderate edge case handling
- Structured workflows with phases

**Examples**:

- docs-maker (documentation creation)
- docs-checker (factual verification)
- docs-tutorial-checker (tutorial quality validation)
- docs-file-manager (file organization, relative path calculation, link updates)
- agent-maker (agent creation automation)
- apps-ayokoding-www-general-maker (general Next.js content creation for ayokoding-www)
- apps-ayokoding-www-by-example-maker (by-example tutorial creation)
- apps-ose-www-content-maker (Next.js content creation for ose-www)

**When to use this tier**:

- Agent creates or validates content
- Requires moderate decision-making
- Follows established patterns
- Handles multiple related tasks within a domain

### Tier 3: Complex Agents (Planners, Orchestrators, Comprehensive Validators)

**Target**: < 1,200 lines / < 35KB
**Warning**: 1,500 lines / 40KB
**Hard Limit**: 1,800 lines / 50KB

**Characteristics**:

- High complexity with multiple interconnected concerns
- Advanced reasoning and pattern recognition
- Multi-step orchestration
- Extensive edge case handling
- Complex validation or planning logic
- Cross-cutting concerns

**Examples**:

- plan-maker (comprehensive project planning)
- plan-checker (pre-implementation validation)
- repo-rules-maker (cascading updates across files)
- repo-rules-checker (comprehensive consistency validation)
- docs-link-checker (external/internal link validation with caching)

**When to use this tier**:

- Agent orchestrates multiple phases or agents
- Requires advanced reasoning
- Handles complex dependencies
- Manages cascading impacts
- Performs comprehensive validation
