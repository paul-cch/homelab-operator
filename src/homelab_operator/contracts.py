"""Side-effect-free contract checks for agent-authored infrastructure work."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from enum import Enum


class ExitState(str, Enum):
    MERGE_READY = "MERGE_READY"
    BLOCKED_WITH_EVIDENCE = "BLOCKED_WITH_EVIDENCE"
    CLEAN_NO_OP = "CLEAN_NO_OP"
    HOST_RUNTIME_HANDOFF = "HOST_RUNTIME_HANDOFF"


class ProofKind(str, Enum):
    REPO_ONLY = "repo_only"
    GITHUB_COORDINATION = "github_coordination"
    HOST_CHECKOUT_ONLY = "host_checkout_only"
    RUNTIME_EXPORT_ONLY = "runtime_export_only"
    LIVE_CONFIG_ONLY = "live_config_only"
    EXTERNAL_SERVICE_ONLY = "external_service_only"
    END_TO_END = "end_to_end"
    HANDOFF = "handoff"
    BLOCKED = "blocked"


RECEIPT_FIELDS = (
    "Exit state",
    "Issue",
    "Branch / worktree",
    "PR",
    "Owned paths",
    "Surface classification",
    "Proof kind",
    "Claim proven",
    "Claim not proven",
    "Repo gate",
    "Host/runtime handoff needed",
    "Host gate needed",
    "Runtime gate needed",
    "Live config gate needed",
    "Checks or commands run",
    "Blockers",
    "Next safe command",
)

REQUIRED_PR_SECTIONS = (
    ("Summary",),
    ("Linked Issue", "Linked Issues"),
    ("Owned Paths",),
    ("Validation", "Verification"),
    ("Claim Boundary", "Surface Classification", "Host / Runtime Handoff"),
)

HEADING_RE = re.compile(r"^##\s+(.+?)\s*$")
ISSUE_REF_RE = re.compile(r"\b(?:close[sd]?|fix(?:e[sd])?|resolve[sd]?|refs?|part of)\s+#\d+\b", re.I)
CLOSING_REF_RE = re.compile(r"\b(?:close[sd]?|fix(?:e[sd])?|resolve[sd]?)\s+#\d+\b", re.I)
BARE_CLOSING_RE = re.compile(r"\b(?:close[sd]?|fix(?:e[sd])?|resolve[sd]?)\s+#(?:\D|$)", re.I)
PARTIAL_WORK_RE = re.compile(r"\b(first|remaining|partial|slice|part of|follow-up|coordinator|later|not close|refs?)\b", re.I)
COMMAND_RE = re.compile(r"`[^`]+`|\b(?:python|pytest|ruff|mypy|git |bash |shellcheck |npm |pnpm |cargo |go test)\b")
PRIVATE_PATTERNS = (
    re.compile(r"\b(?:10|127|172\.(?:1[6-9]|2\d|3[0-1])|192\.168)\.\d{1,3}\.\d{1,3}\b"),
    re.compile(r"(?i)\b(?:authorization|api[_-]?key|access[_-]?token|secret[_-]?key|password)\s*[:=]\s*['\"]?[^'\"\s]+"),
    re.compile(r"-----BEGIN (?:RSA |OPENSSH |EC |DSA )?PRIVATE KEY-----"),
)


@dataclass(frozen=True)
class ContractResult:
    errors: tuple[str, ...]
    warnings: tuple[str, ...]
    owned_paths: tuple[str, ...]

    @property
    def ok(self) -> bool:
        return not self.errors


@dataclass(frozen=True)
class ReceiptResult:
    errors: tuple[str, ...]
    warnings: tuple[str, ...]
    fields: dict[str, str]

    @property
    def ok(self) -> bool:
        return not self.errors


@dataclass(frozen=True)
class EstateResult:
    errors: tuple[str, ...]
    warnings: tuple[str, ...]
    surfaces: tuple[str, ...]

    @property
    def ok(self) -> bool:
        return not self.errors


def section_key(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", title.lower()).strip()


def parse_sections(body: str) -> dict[str, str]:
    sections: dict[str, list[str]] = {"": []}
    current = ""
    for line in body.splitlines():
        match = HEADING_RE.match(line)
        if match:
            current = section_key(match.group(1))
            sections.setdefault(current, [])
            continue
        sections.setdefault(current, []).append(line)
    return {key: "\n".join(lines).strip() for key, lines in sections.items()}


def find_section(sections: dict[str, str], *names: str) -> str:
    for name in names:
        text = sections.get(section_key(name), "")
        if text:
            return text
    return ""


def useful_lines(text: str) -> list[str]:
    ignored = {"-", "- [ ]", "- [x]", "Not supplied.", "None supplied."}
    return [line for raw in text.splitlines() if (line := raw.strip()) and line not in ignored]


def owned_path_lines(owned_section: str) -> tuple[str, ...]:
    paths: list[str] = []
    for line in useful_lines(owned_section):
        value = line[2:].strip() if line.startswith("- ") else line
        value = value.strip("`").strip()
        if value:
            paths.append(value)
    return tuple(paths)


def receipt_template(state: str = "MERGE_READY") -> str:
    lines = ["## Agent Lane Receipt", "", f"- Exit state: {state}"]
    lines.extend(f"- {field}:" for field in RECEIPT_FIELDS if field != "Exit state")
    return "\n".join(lines) + "\n"


def receipt_fields(receipt: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for raw in receipt.splitlines():
        line = raw.strip()
        if not line.startswith("- ") or ":" not in line:
            continue
        name, value = line[2:].split(":", 1)
        fields[name.strip()] = value.strip()
    return fields


def evaluate_receipt(receipt: str) -> ReceiptResult:
    fields = receipt_fields(receipt)
    errors: list[str] = []
    warnings: list[str] = []

    missing = [field for field in RECEIPT_FIELDS if field not in fields]
    if missing:
        errors.append("Receipt is missing fields: " + ", ".join(missing))

    exit_state = fields.get("Exit state", "")
    if exit_state and exit_state not in {state.value for state in ExitState}:
        errors.append("Exit state must be one of: " + ", ".join(state.value for state in ExitState))

    proof_kind = fields.get("Proof kind", "")
    if proof_kind and proof_kind not in {kind.value for kind in ProofKind}:
        errors.append("Proof kind must be one of: " + ", ".join(kind.value for kind in ProofKind))

    for field in ("Claim proven", "Claim not proven", "Next safe command"):
        if field in fields and not fields[field]:
            errors.append(f"{field} must not be empty")

    if fields.get("Exit state") == ExitState.MERGE_READY.value and fields.get("Blockers", "").lower() not in {"", "none", "n/a"}:
        warnings.append("MERGE_READY receipts should normally have no blockers")

    return ReceiptResult(errors=tuple(errors), warnings=tuple(warnings), fields=fields)


def evaluate_surface_claim(payload: str) -> ContractResult:
    try:
        data = json.loads(payload)
    except json.JSONDecodeError as exc:
        return ContractResult(errors=(f"Surface claim is not valid JSON: {exc.msg}",), warnings=(), owned_paths=())

    errors: list[str] = []
    required = ("surface", "proof_kind", "claim_proven", "claim_not_proven")
    for field in required:
        if not data.get(field):
            errors.append(f"Surface claim must include non-empty `{field}`")

    if data.get("surface") and data["surface"] not in {
        "repo",
        "github",
        "host_checkout",
        "runtime_export",
        "live_config",
        "external_service",
    }:
        errors.append("Surface claim has unknown surface")

    if data.get("proof_kind") and data["proof_kind"] not in {kind.value for kind in ProofKind}:
        errors.append("Surface claim has unknown proof_kind")

    return ContractResult(errors=tuple(errors), warnings=(), owned_paths=())


def evaluate_estate(payload: str) -> EstateResult:
    """Validate the simple YAML subset used by Homelab Operator examples."""

    errors: list[str] = []
    warnings: list[str] = []
    surfaces: list[str] = []
    flow_refs: list[tuple[str, str]] = []
    current_from: str | None = None

    for raw in payload.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("- id:"):
            surface_id = line.split(":", 1)[1].strip()
            if surface_id:
                surfaces.append(surface_id)
            else:
                errors.append("Estate surface has an empty id")
            continue
        if line.startswith("- from:"):
            current_from = line.split(":", 1)[1].strip()
            continue
        if line.startswith("to:") and current_from is not None:
            flow_refs.append((current_from, line.split(":", 1)[1].strip()))
            current_from = None

    if not surfaces:
        errors.append("Estate must define at least one surface with `- id:`")

    known_surfaces = set(surfaces)
    for source, target in flow_refs:
        if source not in known_surfaces:
            errors.append(f"Estate flow references unknown source surface `{source}`")
        if target not in known_surfaces:
            errors.append(f"Estate flow references unknown target surface `{target}`")

    if not flow_refs:
        warnings.append("Estate defines no flows")

    return EstateResult(errors=tuple(errors), warnings=tuple(warnings), surfaces=tuple(surfaces))


def scan_privacy(text: str) -> ContractResult:
    errors = [f"Privacy scan matched `{pattern.pattern}`" for pattern in PRIVATE_PATTERNS if pattern.search(text)]
    return ContractResult(errors=tuple(errors), warnings=(), owned_paths=())


def body_has_placeholders(body: str) -> list[str]:
    errors: list[str] = []
    if re.search(r"(?m)^\s*-\s*$", body):
        errors.append("PR body still contains an empty bullet placeholder")
    if BARE_CLOSING_RE.search(body):
        errors.append("Linked issue contains a bare closing placeholder like `Closes #`")
    return errors


def evaluate_pr_body(body: str) -> ContractResult:
    sections = parse_sections(body)
    errors = body_has_placeholders(body)
    warnings: list[str] = []

    summary = find_section(sections, *REQUIRED_PR_SECTIONS[0])
    if not useful_lines(summary):
        errors.append("## Summary must describe the change")

    linked_issue = find_section(sections, *REQUIRED_PR_SECTIONS[1])
    if not linked_issue:
        errors.append("PR body must include ## Linked Issue or ## Linked Issues")
    elif not ISSUE_REF_RE.search(linked_issue) and "none supplied" not in linked_issue.lower():
        errors.append("Linked issue must use Closes/Fixes/Refs/Part of #number, or say None supplied")

    owned_section = find_section(sections, *REQUIRED_PR_SECTIONS[2])
    owned_paths = owned_path_lines(owned_section)
    if not owned_section:
        errors.append("PR body must include ## Owned Paths")
    elif not owned_paths:
        errors.append("## Owned Paths must include at least one concrete path")

    validation = find_section(sections, *REQUIRED_PR_SECTIONS[3])
    if not validation:
        errors.append("PR body must include ## Validation or ## Verification")
    elif not COMMAND_RE.search(validation) and not re.search(r"\b(?:not run|not needed|blocked|unavailable)\b", validation, re.I):
        errors.append("Validation section must include commands/results or an explicit blocker")

    claim_boundary = find_section(sections, *REQUIRED_PR_SECTIONS[4])
    if not claim_boundary:
        errors.append("PR body must state the source/host/runtime/live-config claim boundary")

    if CLOSING_REF_RE.search(linked_issue) and PARTIAL_WORK_RE.search(body):
        errors.append("Partial or follow-up work must use `Refs #...` or `Part of #...`, not a closing keyword")

    return ContractResult(errors=tuple(errors), warnings=tuple(warnings), owned_paths=owned_paths)
