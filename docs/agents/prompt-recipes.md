# Prompt Recipes

These prompts are copy-paste starting points for AI-assisted infrastructure
work. Replace bracketed text with public, repo-safe details.

## Source-only change

```text
Work only in [owned paths]. Make the requested source or docs change, then
validate it locally.

Your PR or receipt must use proof kind repo_only. State what passed, what was
not checked, and the next safe handoff. Do not claim host, runtime, live config,
or external-service proof unless a matching public check exists.

Keep examples synthetic and privacy-safe.
```

## Deploy handoff

```text
Prepare the source change for deploy handoff. Do not deploy, restart services,
edit live config, or claim runtime success.

Return a receipt that names the source validation performed, the host/runtime
checks still required, blockers if any, and the exact next safe handoff command
or reviewer action.
```

## Watcher no-op

```text
Check the watcher inputs and local repo state for [scope]. If nothing materially
changed, leave a clean no-op receipt instead of opening GitHub noise.

The receipt must say what was checked, why no change is needed, what was not
proven, and what the next run should watch.
```

## Blocked with evidence

```text
If the task cannot proceed safely, stop and write a blocked receipt.

Name the blocker, include the command or file evidence that proves the blocker,
state what was already verified, and avoid speculative host/runtime/live claims.
```

## PR review

```text
Review this AI-authored infrastructure PR for claim-boundary correctness.

Check whether the validation section proves only repo source, GitHub
coordination, host checkout, runtime export, live config, or external service.
Flag any overclaim where local tests are used as deployment proof.
```

## Validation commands

```bash
homelab-operator check-pr --body-file PR.md
homelab-operator receipt-template --state MERGE_READY
homelab-operator check-receipt --file receipt.md
homelab-operator doctor --root .
```
