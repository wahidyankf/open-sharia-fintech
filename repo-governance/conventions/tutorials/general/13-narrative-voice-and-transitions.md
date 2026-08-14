---
title: "Narrative Requirements: Voice, Perspective, and Transitions"
description: "Defines the required teacher voice and perspective, plus the transition patterns used to connect tutorial sections."
when_to_use: "Read when writing tutorial prose and choosing voice, perspective, or a transition between two sections."
category: explanation
subcategory: conventions
tags:
  - tutorials
  - diataxis
  - learning
  - pedagogy
  - documentation
  - teaching
created: 2025-12-03
---

# Narrative Requirements: Voice, Perspective, and Transitions

## Voice and Perspective

**Teacher Voice** (Not Neutral Documentation Voice)

**Good Examples**:

```markdown
PASS: "Let's start with a simple example to build your intuition."
PASS: "You might be wondering why we multiply by (1-T). Here's the reasoning..."
PASS: "Great! You've now mastered the basics. Let's add some complexity."
PASS: "This is where many people get confused. Take your time with this step."
```

**Bad Examples** (Too Neutral):

```markdown
FAIL: "NPV is calculated using the following formula."
FAIL: "The components are equity and debt."
FAIL: "This formula is used in finance."
```

**Characteristics of Teacher Voice**: - **Personal**: Use "you" and "we" (not "one" or passive voice) - **Encouraging**: Positive, supportive tone - **Anticipatory**: Address common confusions preemptively - **Conversational**: Natural language (not academic jargon) - **Empathetic**: Acknowledges difficulty, provides reassurance

**Perspective Consistency**: - Maintain same voice throughout - Use "we" for joint exploration: "Let's explore..." - Use "you" for learner actions: "Now you try..." - Avoid switching between formal and informal tone

## Transitions Between Sections

**Purpose of Transitions**: - Connect concepts logically - Show how new material builds on previous - Maintain narrative flow - Prevent cognitive jarring

**Transition Patterns**:

**Building Pattern**:

```markdown
Now that you understand [previous concept], we can build on this to explore [new concept].
```

**Connecting Pattern**:

```markdown
[Previous concept] and [new concept] work together to [achieve something].
```

**Contrasting Pattern**:

```markdown
We've seen how [previous concept] works. [New concept] takes a different approach by [contrast].
```

**Problem-Solution Pattern**:

```markdown
[Previous concept] helps us understand the basics, but what about [complication]? That's where [new concept] comes in.
```

**Example**:

```markdown
## 3. Present Value

[Content about PV...]

---

Now you can calculate what future money is worth today. But what if you have multiple cash flows over many years? That's where **Net Present Value (NPV)** comes in. NPV extends the PV concept to handle complex cash flow streams.

## 4. Net Present Value (NPV)

[Content about NPV...]
```
