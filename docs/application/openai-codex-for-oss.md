# OpenAI Codex For OSS Application Packet

This file is a ready-to-edit packet for the OpenAI Codex for Open Source form.
The form was checked on 2026-06-05. It asks for a public GitHub profile, public
repository URL, maintainer role, a qualification answer under 500 characters,
API-credit usage under 500 characters, OpenAI organization ID, and optional
additional context under 500 characters.

## Repository URL

`https://github.com/paul-cch/homelab-operator`

## Role

Primary maintainer.

## Why this repository qualifies

Homelab Operator provides reusable contracts for AI-assisted infrastructure maintenance: PR checks, receipt schemas, and examples that separate source changes from host, runtime, live-config, and external-service proof. It helps maintainers use Codex safely without overstating deployment or live-state claims.

## API credits usage

We would use API credits to run Codex on PR contract review, maintainer automation, release-note generation, example-repo validation, and security-focused review of claim-boundary templates. The goal is to reduce review load while keeping agent-authored infra changes evidence-based and safe.

## Anything else

This is an early project based on patterns proven in a private production homelab, rewritten as a privacy-safe OSS toolkit. Its importance is the emerging need for maintainers to control what coding agents may claim across source, deployment, runtime, and live config surfaces.
