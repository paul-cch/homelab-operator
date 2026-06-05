# Deploy Handoff Workflow

Use this workflow when repo source is ready, but live success requires a host,
runtime, live-config, or external-service check.

1. Complete the source change in a branch.
2. Run the source gate.
3. Open the pull request with `HOST_RUNTIME_HANDOFF` as the exit state if live
   proof is still needed.
4. Name the exact downstream surface to check.
5. State the exact claim that remains unverified.

Example:

```text
Claim proven: source tests pass for the runtime exporter.
Claim not proven: target host has not pulled this commit and runtime export has
not been checked.
Next safe command: run the host deploy gate on the target host.
```

Do not turn a handoff into an end-to-end claim until the downstream evidence
exists.
