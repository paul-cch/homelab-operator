# Blocked With Evidence Workflow

Use `BLOCKED_WITH_EVIDENCE` when work cannot continue safely and the blocker is
concrete.

Valid blockers include:

- missing access
- unclear ownership
- dirty worktree collision
- failing validation
- missing dependency
- unsafe live action
- host/runtime authority missing

The receipt must include:

- the exact command, file, or check that exposed the blocker
- the surface where the blocker lives
- the next safe action

Avoid vague blockers like "needs review" unless the receipt names what must be
reviewed and why.
