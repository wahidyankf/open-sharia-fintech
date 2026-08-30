# Learning-Bearing Syllabus-Record Scaffolding Fixes (Step 5n Findings)

For a missing syllabus artefact on a learning-bearing plan, scaffold the missing sections — never
invent corpus content. Re-validate first; re-read after editing. Artefact shape:
[Learning-Plan `syllabus/` Folder Convention](../../../../repo-governance/conventions/structure/learning-plan-syllabus.md).

**Confidence**: **HIGH** — folder layout completely absent (scaffold `syllabus/README.md`,
`syllabus/courses/README.md`, `syllabus/paths/README.md` with stubs), or the `## Corpus Disposition`/
`## Corpus Custody`/Custodian line is absent (scaffold with a placeholder for the author to choose).
**MEDIUM** — a course file exists but missing a REQUIRED template section — add the header with a
placeholder, never fabricate concepts/prose. **FALSE_POSITIVE** — the plan only reads/links/lightly
corrects an existing corpus — exempt.

**How to scaffold**: insert stubs directly under the plan's `syllabus/` folder.

`syllabus/README.md`:

```markdown
# <Corpus Name> — Syllabus

> _Scaffolded by plan-fixer — fill each placeholder. See the Learning-Plan `syllabus/` Folder
> Convention._

**Custodian**: `<plan-id>` <!-- author: name the owning plan -->

<one-paragraph corpus overview — author to fill>
```

Chosen technical form — Corpus Disposition (owning/custodian plan only; directory README maps the
owning companion):

```markdown
## Corpus Disposition

`<archive-with-plan|promote-to:<path>>` <!-- author: choose exactly one -->
```

Chosen technical form — Corpus Custody echo (consumer plan only; a plan carries exactly one of the
two, and a directory README maps the owning companion):

```markdown
## Corpus Custody

`custodied-by:<plan-id>` <!-- author: name the corpus's owning plan -->
```

For a missing course file's REQUIRED skeleton, point the author at the copy-paste template in
[Learning-Plan `syllabus/` Folder Convention §Copy-Paste Course Template](../../../../repo-governance/conventions/structure/learning-plan-syllabus/copy-paste-course-template.md#copy-paste-course-template)
rather than reproducing it inline.
