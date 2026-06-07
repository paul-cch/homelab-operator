# Emit SARIF output for contract and privacy checks

Labels: `roadmap`, `ci`, `privacy`, `developer-experience`

## Summary

Add optional SARIF output for checks that produce actionable findings, starting
with privacy scanning and contract validation.

## Why

SARIF lets GitHub and other CI systems display scanner findings in a structured
way. This would make Homelab Operator easier to adopt in repositories that want
machine-readable proof without parsing plain text.

## Proposed Scope

- Add an output flag such as `--format sarif` or `--sarif-file`.
- Map each finding to a stable rule id.
- Include file path, line, message, severity, and remediation text when known.
- Add tests that assert the output is valid JSON and includes expected rules.

## Acceptance Criteria

- Existing text output remains the default.
- SARIF output is deterministic for the same synthetic fixture.
- Privacy findings never echo secret values or private operational snippets.
- Documentation shows a synthetic CI invocation.

## Out Of Scope

- Uploading results to GitHub.
- Scanning real estates, live logs, or runtime exports.
- Adding a new security scanner beyond existing contract checks.
