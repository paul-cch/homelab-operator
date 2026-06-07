# Add a CLI command for JSON Schema validation

Labels: `good first issue`, `roadmap`, `cli`, `schemas`

## Summary

Expose the bundled JSON Schemas through a simple CLI command so adopters can
validate a PR contract, lane receipt, surface claim, or estate file directly.

## Why

The schemas already exist under `schemas/`, but users currently need to know how
to wire their own validator. A first-party command would make the contract
surface easier to try and easier to document in CI.

## Proposed Scope

- Add a command such as `homelab-operator validate-schema`.
- Support selecting one bundled schema by name.
- Validate one local file path per invocation.
- Return a non-zero exit code and concise error output on failure.
- Add tests with existing synthetic fixtures or new synthetic fixtures.

## Acceptance Criteria

- A valid fixture passes against the selected schema.
- An invalid fixture fails with the failing path or field name in the output.
- The command is documented in the command reference.
- No examples include private topology, logs, secrets, or live config.

## Out Of Scope

- Remote schema fetching.
- Host, runtime, or external-service validation.
- Automatic fixes for invalid files.
