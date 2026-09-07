---
description: "Three writing guidelines: short scannable paragraphs, eliminating jargon, and explaining acronyms with context"
when_to_use: Read this when a README paragraph reads as dense, jargon-heavy, or has an unexplained acronym.
---

# Guidelines: Scannability, Jargon, and Acronyms

## 2. Make It Scannable

**Short Paragraphs**: Maximum 4-5 lines per paragraph. Break longer content into multiple paragraphs or bullet points.

**FAIL: Bad** (6+ line dense paragraph):

```markdown
This project aims to make Sharia-compliant enterprise solutions accessible to organizations worldwide. By creating an open-source platform that puts Sharia-compliance at its core, we enable enterprises to build trust-worthy business systems (fintech, ERP, and beyond) that serve communities with specific religious and ethical requirements. We're starting with ERP to establish a solid enterprise foundation that can support diverse business operations, with plans to expand into fintech and other domains.
```

**PASS: Good** (scannable structure):

```markdown
We're building an open-source platform with Sharia-compliance at its core. Starting with ERP foundations, we'll expand to fintech and beyond.

Our goal: Make trustworthy business systems accessible to any organization—regardless of size, region, or industry.
```

**Visual Breaks**: Use headings, bullet points, code blocks, and emojis strategically to create visual hierarchy.

## 3. Eliminate Jargon

**Plain Language First**: Write like you're explaining to a smart friend, not a technical committee.

**FAIL: Bad** (jargony, corporate):

```markdown
We prioritize open-source and vendor-neutral technologies to avoid lock-in while maintaining project quality and long-term sustainability. We value avoiding vendor lock-in over strict OSS-only requirements.
```

**PASS: Good** (plain language):

```markdown
We choose technologies that keep you free. Your data stays yours, in open formats you can take anywhere. No vendor traps, no proprietary formats, no forced dependencies.
```

**Jargon to Avoid**:

- "vendor lock-in" → "no vendor traps" or "keep you free"
- "vendor-neutral" → "you control your choices"
- "OSS" → "open-source" (spell it out)
- "utilize" → "use"
- "leverage" → "use"
- "solutions" → "software" or "tools"
- "utilize synergies" → just... no

## 4. Explain Acronyms with Context

**First Mention**: Always explain acronyms on first use, and provide context for what they mean.

**FAIL: Bad** (no context):

```markdown
- International Islamic finance standards (AAOIFI, IFSB)
- OJK (Otoritas Jasa Keuangan) Sharia banking regulations
```

**PASS: Good** (context provided):

```markdown
- International Islamic finance standards - Accounting (AAOIFI) and prudential (IFSB) standards
- Indonesian Banking Authority (OJK) - Sharia banking regulations
```

**English-First Naming**: For non-English terms, lead with English translation, then provide original name.

**PASS: Good**:

- **Indonesian Banking Authority (OJK)** - not "OJK (Otoritas Jasa Keuangan)"
- **National Sharia Board (DSN-MUI)** - not "DSN-MUI (Dewan Syariah Nasional...)"
