# Add CI annotations for contract failures

Labels: `roadmap`, `ci`, `developer-experience`

## Summary

Emit GitHub Actions annotation lines for contract and privacy failures so CI can
point directly to the failing file and section.

## Why

Plain text failures are readable, but annotations make pull request feedback
faster to act on. Contributors should be able to jump from CI output to the
missing claim boundary, empty validation section, or privacy finding.

## Proposed Scope

- Add an annotation output mode or CI-aware flag.
- Include file, line, rule id, and concise message when available.
- Keep normal text output unchanged by default.
- Add tests for annotation formatting with synthetic fixtures.

## Acceptance Criteria

- CI annotation output follows GitHub Actions syntax.
- Rule messages are stable and easy to search.
- Privacy annotations avoid echoing sensitive matched content.
- Documentation shows a source-only workflow example.

## Out Of Scope

- Uploading SARIF results.
- Creating or closing GitHub issues.
- Claiming host, runtime, live-config, or external-service proof.
