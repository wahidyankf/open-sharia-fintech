# Evaluation Methodology — Heuristic Evaluation + Cognitive Walkthrough

Combine the two canonical usability-inspection methods (Nielsen Norman Group). Heuristic evaluation
gives breadth (the whole interface against a guideline set); cognitive walkthrough gives depth on
learnability (specific tasks, step by step, from a new user's seat).

## 1. Heuristic evaluation — Nielsen's 10 usability heuristics

Sweep the interface against each heuristic; record every violation with its heuristic number and a
0-4 severity (see the finding-anatomy reference module).

1. **Visibility of system status** — the design keeps the user informed with timely feedback.
2. **Match between system and the real world** — speaks the user's language; no internal jargon.
3. **User control and freedom** — a clearly marked "emergency exit"; easy undo/cancel.
4. **Consistency and standards** — same words/actions mean the same thing; follows platform and
   industry convention (internal **and** external consistency).
5. **Error prevention** — the design prevents problems before they occur, not just reports them.
6. **Recognition rather than recall** — options are visible; the user needn't remember across
   screens.
7. **Flexibility and efficiency of use** — shortcuts for experts without burdening novices.
8. **Aesthetic and minimalist design** — no irrelevant or rarely-needed content competing for
   attention.
9. **Help users recognize, diagnose, and recover from errors** — plain-language messages that name
   the problem and suggest a fix (no raw error codes).
10. **Help and documentation** — ideally unneeded; when present, easy to search and task-focused.

## 2. Cognitive walkthrough — the four questions, per task step

For each task (given or derived), walk every step as a first-time user and ask:

1. Will the user **try to achieve the right result**? (Do they understand what to do at this step?)
2. Will the user **notice the correct action is available**? (Is it visible and findable?)
3. Will the user **associate the correct action with the result** they want? (Do labels/affordances
   read correctly?)
4. After acting, will the user **see that progress was made** toward the goal? (Does the system
   confirm?)

Any "no" or "uncertain" is a usability finding. Capture the full step transcript in `walkthrough.md`
so the verdict is auditable.

## 3. First-click & information scent

For each key task, identify what the **correct first click** should be, then judge whether the
page's visual hierarchy, labelling, and information scent actually make that the most compelling
target — a correct first click correlates with roughly **3× task success** (Optimal Workshop; Bailey
& Wolfson). Evaluate every nav item and link for **information scent** (Pirolli & Card): could a
user, seeing only the label and its immediate context, correctly predict the destination? Vague
labels ("Click here", "Learn more", unlabelled icons) are weak-scent findings.

## 4. The naive-user stance

Channel Krug's _Don't Make Me Think_: users **scan, they don't read**; they **satisfice** (take the
first reasonable option, not the best); a good page is **self-evident**. For every element ask:
"could a first-time visitor understand what this is and what to do **without thinking**?" If it
needs reasoning to decode, that is the finding.
