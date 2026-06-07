# Source Tests Are Not Runtime Proof

AI agents are good at doing source work quickly. They can edit a workflow,
update documentation, add tests, run the suite, and produce a confident receipt.
That is useful. It is also where a subtle failure starts: a green source check
can be described as if it proved a running system changed.

It did not.

Source tests prove something narrower: the checkout in front of the agent is
internally coherent. They do not prove that a host pulled the commit, that a
service restarted, that a runtime export changed, that live configuration is
fresh, or that an external dependency accepted the new shape. Those are
different surfaces, and each needs its own evidence.

Homelab Operator exists for that gap. It gives AI-assisted infrastructure work a
small contract vocabulary so maintainers can tell the difference between "this
change is correct in source" and "this change is operating downstream."

## The Overclaim Pattern

A common agent receipt looks reasonable at first glance:

```text
Claim proven: deployment workflow fixed and service is now healthy.
Checks run: unit tests, lint, documentation build.
```

The problem is not the checks. The problem is the claim. Nothing in that list
checked a host checkout, a running service, a live config file, or an external
service. The receipt may be good evidence for a source patch, but it is weak
evidence for runtime state.

The safer version is more precise:

```text
Proof kind: repo_only
Claim proven: the workflow source, docs, and contract tests pass locally.
Claim not proven: no host checkout, runtime export, live config, or external
service was checked.
```

That language is less dramatic, but it is more useful. It tells the next
maintainer exactly what can be trusted and exactly where the handoff begins.

## The Proof Ladder

Homelab Operator separates evidence by surface:

- `repo_only`: local source, docs, schemas, templates, or tests were checked.
- `github_coordination`: issue, pull request, branch, CI, or review metadata was
  checked.
- `host_checkout_only`: a target host checkout was checked.
- `runtime_export_only`: a runtime export or running service was checked.
- `live_config_only`: redacted live configuration shape or freshness was checked.
- `external_service_only`: a bounded external service probe was checked.
- `end_to_end`: source continuity and downstream live proof were both checked.
- `handoff`: the source work is ready, but another surface still needs proof.
- `blocked`: the work stopped for a concrete reason.

The ladder is not a maturity badge. Higher is not automatically better. A
documentation change may only need `repo_only` proof. A release handoff may need
`github_coordination`. A deployment claim needs something downstream. The point
is to stop one kind of evidence from borrowing authority from another.

## Synthetic Example

Imagine a public example repo with a synthetic service named `media-indexer`.
An agent changes a readiness check and runs:

```bash
python -m pytest
homelab-operator doctor --root .
```

If those checks pass, the honest receipt is:

```text
Proof kind: repo_only
Claim proven: the readiness-check source and examples pass local contract gates.
Claim not proven: no host checkout or runtime export for media-indexer was
checked.
Next safe command: have an operator verify the downstream surface before making
a runtime-health claim.
```

That is enough for a source pull request. It is not enough for "media-indexer is
healthy" or "the fix is deployed." Those claims require additional checks at the
surface where the claim lives.

## Why This Matters For AI Agents

AI agents compress work. They also compress language. Without a contract, "tests
passed" can quietly become "the system is fixed" by the time a pull request,
issue update, or handoff note is written.

Homelab Operator makes that compression visible. Its checks ask receipts and
claim bodies to name:

- what surface was checked;
- what proof kind applies;
- what claim was actually proven;
- what claim remains unproven;
- what the next safe command is.

This does not make source tests less valuable. It makes them more valuable,
because their result is no longer asked to prove more than it can.

## A Better Default

For source and documentation work, default to `repo_only` unless a public,
privacy-safe example proves a deeper surface. Say exactly what ran. Say exactly
what did not run. Keep hostnames, addresses, logs, live config, and secrets out
of public examples.

The strongest agent receipts are not the most confident ones. They are the ones
that let the next maintainer continue without guessing which world was actually
checked.
