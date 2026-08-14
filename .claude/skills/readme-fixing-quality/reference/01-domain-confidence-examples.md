# Domain-Specific Confidence Examples for README Content

**HIGH Confidence** (Apply automatically — OBJECTIVE issues):

- Paragraph exceeding 5 lines (count is objective)
- Specific jargon patterns ("vendor lock-in", "utilize", "leverage")
- Acronym without context/expansion
- Passive voice patterns ("is controlled by" vs "you control")
- Missing problem-solution hook structure
- Feature list without benefits transformation

**MEDIUM Confidence** (Manual review — SUBJECTIVE issues):

- Overall tone assessment (welcoming vs corporate)
- Engagement quality (inviting vs dry)
- Sentence length appropriateness (context-dependent)
- Emoji placement effectiveness
- Whether hook is "clear enough"
- Overall scannability quality

**FALSE_POSITIVE** (Report to checker):

- Checker flagged technical term as jargon (actually necessary)
- Checker reported paragraph too long (exactly 5 lines = acceptable)
- Checker misidentified passive voice (actually active)
- Checker flagged explained acronym as unexplained

**CRITICAL**: Many README quality issues are subjective. Apply fixes ONLY for objective,
verifiable issues.
