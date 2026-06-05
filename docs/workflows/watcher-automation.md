# Watcher Automation Workflow

Watcher automations should reduce noise. If nothing materially changed, they
should leave a compact receipt instead of creating duplicate comments or issues.

Use `CLEAN_NO_OP` when:

- the queue is empty
- the existing issue or PR already covers the current state
- a previous receipt still matches the current evidence
- the only available action would create noise

The receipt should say:

- what was checked
- why no edit, branch, issue, or PR was created
- what future change would make the lane actionable

This makes automation useful without making maintainers sort through repeated
"still fine" messages.
