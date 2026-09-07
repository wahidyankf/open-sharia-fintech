---
description: "The required sections a CONTRIBUTING.md must have and the writing principles for contributor-facing process docs"
when_to_use: "Read this when drafting or reviewing a CONTRIBUTING.md file's required content and tone."
---

# CONTRIBUTING.md: Essential Components and Writing Principles

## Essential Components

All CONTRIBUTING.md files must include:

1. **Welcome Message**
   - Thank contributors for their interest
   - Make them feel valued and encouraged
   - Set a positive, inclusive tone

2. **Table of Contents**
   - For files > 200 lines
   - Links to major sections
   - Improves navigation

3. **Development Environment Setup**
   - Prerequisites (Node.js, Volta, etc.)
   - Installation steps
   - Running locally
   - Common troubleshooting

4. **Code Conventions**
   - Coding style (link to style guide if detailed)
   - Commit message format (link to [Commit Message Convention](../../../development/workflow/commit-messages.md))
   - Branch naming (link to [Trunk Based Development](../../../development/workflow/trunk-based-development.md))
   - Testing requirements

5. **Contribution Process**
   - How to find issues to work on
   - How to propose new features
   - Pull request submission process
   - Code review expectations
   - Expected response time

6. **Bug Reports**
   - Where to report (GitHub Issues, email, etc.)
   - What information to include
   - Issue template (if available)

7. **Feature Requests**
   - How to propose enhancements
   - What information to include
   - Discussion process

8. **Testing Requirements**
   - How to run tests
   - Coverage expectations
   - Test writing guidelines

9. **Code of Conduct**
   - Link to CODE_OF_CONDUCT.md
   - Or embed if brief

10. **Getting Help**
    - Where to ask questions
    - Community channels
    - Maintainer contact

## Writing Principles

**Be Explicit:**

- Don't assume contributors know your process
- List specific steps, not general guidance
- Provide examples for complex processes

**Anticipate Challenges:**

- Address common setup issues
- Provide troubleshooting sections
- Link to solutions for known problems

**One PR Per Change:**

- Explicitly state: "Submit one pull request per bug fix or feature"
- Explain why (easier review, simpler rollback)
- Provide examples of good vs. bad PR scope

**Set Expectations:**

- Typical review time
- Merge requirements (approvals, tests passing)
- What happens after merge
