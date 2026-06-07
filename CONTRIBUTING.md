# Contributing

Thanks for helping make agent-assisted infrastructure work safer.

Start with the first-PR path if this is your first contribution:

- [Make a safe first PR](docs/contributing/first-pr.md)

## Pick Good First Work

Look for issues labelled `good first issue`. Good first issues should name:

- the expected files or folders to touch
- the validation commands to run
- the proof boundary, usually `repo_only`
- anything that is out of scope

If an issue does not include those details, ask before starting.

## Privacy Boundaries

Keep examples synthetic. Do not include private hostnames, IP addresses,
domains, secrets, logs, runtime state, live config, inventories, or operational
screenshots. Public examples should use names such as `source`, `host`,
`runtime`, `live-config`, and `external-service`.

## Before Opening a Pull Request

Run the smallest relevant gate for your change. For most source and docs work:

```bash
python -m pip install -e ".[dev]"
python -m pytest
homelab-operator doctor --root .
```

For docs-only changes, also run:

```bash
homelab-operator check-privacy --root .
git diff --check
```

PRs should describe what was proven and what was not proven. For source-only
or docs-only changes, use a claim boundary like:

```text
Proof kind: repo_only
Claim proven: docs/source changed in this checkout and the listed local checks passed.
Claim not proven: no host checkout, runtime export, live config, or external service was checked.
Host/runtime/live-config handoff needed: no
```
