# Support configurable privacy scan patterns

Labels: `roadmap`, `privacy`, `configuration`

## Summary

Allow repositories to add privacy scan patterns for their own public-safety
rules while preserving Homelab Operator's default checks.

## Why

The built-in privacy scanner catches common risky material, but public projects
may have organization-specific terms or generated files they want to block.
Configuration would make the scanner more useful without hard-coding local
policy into the package.

## Proposed Scope

- Define a small config file format for additional deny patterns.
- Keep built-in patterns enabled by default.
- Support rule ids and human-readable descriptions.
- Add tests for config loading, matching, and malformed config handling.
- Document a synthetic config example.

## Acceptance Criteria

- Custom patterns can be added without editing Python source.
- Built-in privacy checks still run when a config file is present.
- Invalid config fails with a clear, non-sensitive error.
- Matching output does not print secret-like captured values.

## Out Of Scope

- Allowing config to disable built-in high-risk checks.
- Publishing real organization policy examples.
- Runtime, host, or live-config scanning.
