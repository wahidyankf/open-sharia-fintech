---
description: "Defines the recommended tutorial length range and how to split an overlong tutorial into a progressive series."
when_to_use: "Read when a tutorial is growing too long and you need to decide whether and how to split it into a series."
---

# Tutorial Length and Splitting

**Recommended Length**: 500-1,500 lines (15-45 minutes reading time)

**Why length matters**: - Too short: May lack sufficient depth or practice opportunities - Too long: Overwhelms learners, violates single-focus principle

**Length Guidelines**:

**< 300 lines (Too Short)**: - May indicate insufficient depth - Consider: - Combining with related tutorial - Adding more examples and practice exercises - Expanding explanations with visual aids - Exception: "Initial Setup" tutorials can be shorter (200-300 lines)

**500-1,500 lines (Ideal)**: - Focused on single topic or skill - Sufficient depth and practice - Maintains learner engagement - Completable in one sitting

**1,500-5,000 lines (Upper Limit)**: - Still manageable but approaching threshold - Consider if content can be split - Ensure strong narrative flow to maintain engagement

**> 5,000 lines (Too Long - Must Split)**: - Risk overwhelming learners - Violates single-focus principle - Action required: Split into tutorial series

**How to Split Long Tutorials**:

**1. Identify Natural Break Points**: - Basic vs. Advanced concepts (beginner/intermediate split) - Core features vs. Optional extensions - Local development vs. Production deployment - Theory vs. Practice (conceptual/hands-on split)

**2. Create Progressive Series**:

```
Part 1: Basic Setup (rag-basics.md)
Part 2: Advanced Features (rag-advanced.md)
Part 3: Production Deployment (rag-production.md)
```

**3. Link Tutorials Together**: - **Part 1 "Next Steps"**: Link to Part 2 - **Part 2 "Prerequisites"**: Link back to Part 1 - **Part 2 "Next Steps"**: Link to Part 3 - Each part should be self-contained but reference the series

**4. Optional: Create Series Index**:

Create a series overview tutorial (e.g., `rag-series.md`):

```markdown
# RAG Tutorial Series

Complete guide to building Retrieval-Augmented Generation systems.

## Tutorial Sequence

**Part 1: RAG Basics** (Beginner)

- [Link to Part 1](../rag-basics.md)
- Build your first RAG system
- Coverage: 0-40% of RAG concepts

**Part 2: Advanced RAG** (Intermediate)

- [Link to Part 2](../rag-advanced.md)
- Hybrid search, reranking, and optimization
- Coverage: 40-75% of RAG concepts
- Prerequisites: Part 1

**Part 3: Production RAG** (Advanced)

- [Link to Part 3](../rag-production.md)
- Deploy RAG to production with monitoring
- Coverage: 75-100% of RAG concepts
- Prerequisites: Parts 1 & 2
```

**Example Split**:

FAIL: **Bad**: Single 3,000-line tutorial covering basic RAG, advanced techniques, and production deployment

PASS: **Good**: Three focused tutorials:

1. "Build Your First RAG System" (800 lines) - Core concepts, simple implementation
2. "Advanced RAG Techniques" (700 lines) - Hybrid search, reranking, optimization
3. "Deploy RAG to Production" (600 lines) - Scalability, monitoring, best practices

**Each part**: - Has clear prerequisites - Focuses on specific skill level - Is completable in one session - Links to previous/next parts
