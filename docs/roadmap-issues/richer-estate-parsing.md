# Expand synthetic estate parsing

Labels: `roadmap`, `parser`, `examples`

## Summary

Extend `check-estate` beyond the current simple YAML subset while keeping the
minimal synthetic example valid and easy to understand.

## Why

Richer estate shapes would let public examples show more realistic contract
structure without revealing any real topology. This can help users model
services, owners, proof surfaces, and handoff notes in a consistent way.

## Proposed Scope

- Define the next supported synthetic estate fields.
- Add parser validation for nested services or surface metadata.
- Keep clear errors for unsupported fields.
- Add fixtures for both valid and invalid synthetic estates.
- Update docs to explain the supported shape.

## Acceptance Criteria

- The existing minimal estate still passes.
- New synthetic fixtures cover richer estate structure.
- Invalid estate files fail with precise field-level messages.
- No fixture includes real hostnames, IP addresses, domains, logs, or live config.

## Out Of Scope

- Importing real inventory formats.
- Probing hosts, runtimes, or external services.
- Supporting every YAML feature or arbitrary custom schemas.
