"""Side-effect-free contract checks for agent-authored infrastructure work."""

from __future__ import annotations

import json
import re
import tomllib
from dataclasses import dataclass
from enum import Enum
from pathlib import Path


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


class SurfaceKind(str, Enum):
    REPO = "repo"
    GITHUB = "github"
    HOST_CHECKOUT = "host_checkout"
    RUNTIME_EXPORT = "runtime_export"
    LIVE_CONFIG = "live_config"
    EXTERNAL_SERVICE = "external_service"


PROOF_KIND_VALUES = tuple(kind.value for kind in ProofKind)
SURFACE_KIND_VALUES = tuple(kind.value for kind in SurfaceKind)

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

NON_EMPTY_RECEIPT_FIELDS = (
    "Exit state",
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
PRIVACY_RULE_ID_RE = re.compile(r"^[a-z0-9][a-z0-9_.-]{0,63}$")
ESTATE_TOP_LEVEL_KEYS = {"name", "surfaces", "flows"}
ESTATE_SURFACE_KEYS = {"id", "kind", "authority", "owner", "description", "handoff", "services"}
ESTATE_SERVICE_KEYS = {"id", "owner", "purpose", "proof_required", "handoff"}
ESTATE_FLOW_KEYS = {"from", "to", "proof_required", "intent", "handoff"}


@dataclass(frozen=True)
class PrivacyRule:
    rule_id: str
    description: str
    pattern: re.Pattern[str] | None = None
    literal: str | None = None
    source: str = "built-in"

    def matches(self, text: str) -> bool:
        if self.literal is not None:
            return self.literal in text
        return bool(self.pattern and self.pattern.search(text))


class PrivacyConfigError(ValueError):
    """Raised when a privacy config cannot be loaded safely."""


BUILTIN_PRIVACY_RULES = (
    PrivacyRule(
        rule_id="builtin.private-ipv4",
        description="Private or loopback IPv4 address",
        pattern=re.compile(r"\b(?:10|127|172\.(?:1[6-9]|2\d|3[0-1])|192\.168)\.\d{1,3}\.\d{1,3}\b"),
    ),
    PrivacyRule(
        rule_id="builtin.credential-assignment",
        description="Credential-like assignment",
        pattern=re.compile(
            r"(?i)\b(?:authorization|api[_-]?key|access[_-]?token|secret[_-]?key|password)\s*[:=]\s*['\"]?[^'\"\s]+"
        ),
    ),
    PrivacyRule(
        rule_id="builtin.private-key-block",
        description="Private key block marker",
        pattern=re.compile(r"-----BEGIN (?:RSA |OPENSSH |EC |DSA )?PRIVATE KEY-----"),
    ),
)
PRIVATE_PATTERNS = tuple(rule.pattern for rule in BUILTIN_PRIVACY_RULES)


@dataclass(frozen=True)
class ContractResult:
    errors: tuple[str, ...]
    warnings: tuple[str, ...]
    owned_paths: tuple[str, ...]

    @property
    def ok(self) -> bool:
        return not self.errors


@dataclass(frozen=True)
class PrivacyFinding:
    line: int
    rule_id: str
    description: str


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


def privacy_match_error(rule: PrivacyRule) -> str:
    return f"Privacy scan matched rule `{rule.rule_id}`: {rule.description}"


def privacy_finding_error(finding: PrivacyFinding) -> str:
    return f"Privacy scan matched rule `{finding.rule_id}`: {finding.description}"


def load_privacy_config(path: Path) -> tuple[PrivacyRule, ...]:
    if not path.exists():
        raise PrivacyConfigError(f"Privacy config not found: {path}")

    try:
        raw_config = path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise PrivacyConfigError("Privacy config must be valid UTF-8 text") from exc

    try:
        data = tomllib.loads(raw_config)
    except tomllib.TOMLDecodeError as exc:
        raise PrivacyConfigError(f"Privacy config is not valid TOML: {exc.msg}") from exc

    privacy = data.get("privacy")
    if not isinstance(privacy, dict):
        raise PrivacyConfigError("Privacy config must define a [privacy] table")

    deny_patterns = privacy.get("deny_patterns")
    if deny_patterns is None:
        return ()
    if not isinstance(deny_patterns, list):
        raise PrivacyConfigError("Privacy config `privacy.deny_patterns` must be a list")

    rules: list[PrivacyRule] = []
    for index, item in enumerate(deny_patterns, start=1):
        if not isinstance(item, dict):
            raise PrivacyConfigError(f"Privacy config rule {index} must be a table")

        rule_id = item.get("id")
        description = item.get("description")
        pattern = item.get("pattern")
        if not isinstance(rule_id, str) or not rule_id.strip():
            raise PrivacyConfigError(f"Privacy config rule {index} must include non-empty `id`")
        if not PRIVACY_RULE_ID_RE.fullmatch(rule_id):
            raise PrivacyConfigError(f"Privacy config rule {index} has invalid `id`")
        if not isinstance(description, str) or not description.strip():
            raise PrivacyConfigError(f"Privacy config rule `{rule_id}` must include non-empty `description`")
        if not isinstance(pattern, str) or not pattern:
            raise PrivacyConfigError(f"Privacy config rule `{rule_id}` must include non-empty `pattern`")
        if len(pattern) > 256:
            raise PrivacyConfigError(f"Privacy config rule `{rule_id}` has `pattern` longer than 256 characters")

        rules.append(
            PrivacyRule(
                rule_id=rule_id,
                description=description.strip(),
                literal=pattern,
                source=str(path),
            )
        )

    return tuple(rules)


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

    for field in NON_EMPTY_RECEIPT_FIELDS:
        if field in fields and not fields[field]:
            errors.append(f"{field} must not be empty")

    exit_state = fields.get("Exit state", "")
    if exit_state and exit_state not in {state.value for state in ExitState}:
        errors.append("Exit state must be one of: " + ", ".join(state.value for state in ExitState))

    proof_kind = fields.get("Proof kind", "")
    if proof_kind and proof_kind not in PROOF_KIND_VALUES:
        errors.append("Proof kind must be one of: " + ", ".join(PROOF_KIND_VALUES))

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
        if not isinstance(data.get(field), str) or not data[field].strip():
            errors.append(f"Surface claim must include non-empty `{field}`")

    if data.get("surface") and data["surface"] not in SURFACE_KIND_VALUES:
        errors.append("Surface claim has unknown surface")

    if data.get("proof_kind") and data["proof_kind"] not in PROOF_KIND_VALUES:
        errors.append("Surface claim has unknown proof_kind")

    return ContractResult(errors=tuple(errors), warnings=(), owned_paths=())


def split_estate_field(line: str) -> tuple[str, str] | None:
    if ":" not in line:
        return None
    key, value = line.split(":", 1)
    return key.strip(), value.strip()


def estate_record_label(record: dict[str, object], fallback: str = "<unknown>") -> str:
    value = record.get("id", "")
    return str(value) if value else fallback


def add_estate_field(
    record: dict[str, object],
    key: str,
    value: str,
    allowed_keys: set[str],
    context: str,
    errors: list[str],
) -> None:
    if key not in allowed_keys:
        errors.append(f"{context} has unsupported field `{key}`")
        return
    record[key] = value


def parse_estate_subset(payload: str) -> tuple[list[str], list[dict[str, object]], list[dict[str, object]], bool, bool]:
    errors: list[str] = []
    surface_records: list[dict[str, object]] = []
    flow_records: list[dict[str, object]] = []
    current_section: str | None = None
    current_surface: dict[str, object] | None = None
    current_flow: dict[str, object] | None = None
    current_service: dict[str, object] | None = None
    name_seen = False
    flows_seen = False

    for raw in payload.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue

        indent = len(raw) - len(raw.lstrip(" "))
        line = raw.strip()

        if indent == 0:
            current_surface = None
            current_flow = None
            current_service = None
            parsed = split_estate_field(line)
            if parsed is None:
                errors.append(f"Estate has unsupported top-level line `{line}`")
                continue
            key, value = parsed
            if key not in ESTATE_TOP_LEVEL_KEYS:
                errors.append(f"Estate has unsupported top-level field `{key}`")
                continue
            if key == "name":
                name_seen = True
                if not value:
                    errors.append("Estate must define non-empty name")
            elif key == "surfaces":
                if value:
                    errors.append("Estate `surfaces` must be a nested list")
                current_section = "surfaces"
            elif key == "flows":
                if value:
                    errors.append("Estate `flows` must be a nested list")
                flows_seen = True
                current_section = "flows"
            continue

        if current_section == "surfaces":
            if indent == 2 and line.startswith("- "):
                current_surface = {}
                current_service = None
                surface_records.append(current_surface)
                parsed = split_estate_field(line[2:].strip())
                if parsed is None:
                    errors.append("Estate surface list item must include `key: value`")
                    continue
                key, value = parsed
                if key == "services":
                    if value:
                        errors.append("Estate surface `<unknown>` field `services` must be a nested list")
                    current_surface["services"] = []
                    continue
                add_estate_field(current_surface, key, value, ESTATE_SURFACE_KEYS, "Estate surface `<unknown>`", errors)
                continue

            if current_surface is None:
                errors.append("Estate surface field appears before a surface list item")
                continue

            surface_label = estate_record_label(current_surface)
            if indent == 4:
                parsed = split_estate_field(line)
                if parsed is None:
                    errors.append(f"Estate surface `{surface_label}` has unsupported line `{line}`")
                    continue
                key, value = parsed
                if key == "services":
                    if value:
                        errors.append(f"Estate surface `{surface_label}` field `services` must be a nested list")
                    current_surface["services"] = []
                    current_service = None
                    continue
                add_estate_field(
                    current_surface,
                    key,
                    value,
                    ESTATE_SURFACE_KEYS,
                    f"Estate surface `{surface_label}`",
                    errors,
                )
                continue

            if indent == 6 and line.startswith("- "):
                services = current_surface.get("services")
                if not isinstance(services, list):
                    errors.append(f"Estate surface `{surface_label}` field `services` must be a nested list")
                    continue
                current_service = {}
                services.append(current_service)
                parsed = split_estate_field(line[2:].strip())
                if parsed is None:
                    errors.append(f"Estate service on surface `{surface_label}` must include `key: value`")
                    continue
                key, value = parsed
                add_estate_field(
                    current_service,
                    key,
                    value,
                    ESTATE_SERVICE_KEYS,
                    f"Estate service `<unknown>` on surface `{surface_label}`",
                    errors,
                )
                continue

            if indent == 8 and current_service is not None:
                service_label = estate_record_label(current_service)
                parsed = split_estate_field(line)
                if parsed is None:
                    errors.append(f"Estate service `{service_label}` on surface `{surface_label}` has unsupported line `{line}`")
                    continue
                key, value = parsed
                add_estate_field(
                    current_service,
                    key,
                    value,
                    ESTATE_SERVICE_KEYS,
                    f"Estate service `{service_label}` on surface `{surface_label}`",
                    errors,
                )
                continue

            errors.append(f"Estate surface `{surface_label}` has unsupported nested line `{line}`")
            continue

        if current_section == "flows":
            if indent == 2 and line.startswith("- "):
                current_flow = {}
                flow_records.append(current_flow)
                parsed = split_estate_field(line[2:].strip())
                if parsed is None:
                    errors.append("Estate flow list item must include `key: value`")
                    continue
                key, value = parsed
                add_estate_field(current_flow, key, value, ESTATE_FLOW_KEYS, "Estate flow `<unknown>`", errors)
                continue

            if indent == 4 and current_flow is not None:
                parsed = split_estate_field(line)
                if parsed is None:
                    errors.append(f"Estate flow has unsupported line `{line}`")
                    continue
                key, value = parsed
                source = str(current_flow.get("from", "<unknown>") or "<unknown>")
                target = str(current_flow.get("to", "<unknown>") or "<unknown>")
                add_estate_field(
                    current_flow,
                    key,
                    value,
                    ESTATE_FLOW_KEYS,
                    f"Estate flow from `{source}` to `{target}`",
                    errors,
                )
                continue

            errors.append(f"Estate flow has unsupported nested line `{line}`")
            continue

        errors.append(f"Estate field appears outside `surfaces` or `flows`: `{line}`")

    return errors, surface_records, flow_records, name_seen, flows_seen


def evaluate_estate(payload: str) -> EstateResult:
    """Validate the supported YAML subset used by Homelab Operator examples."""

    errors, surface_records, flow_records, name_seen, flows_seen = parse_estate_subset(payload)
    warnings: list[str] = []

    surfaces: list[str] = []
    for surface in surface_records:
        surface_id = str(surface.get("id", ""))
        if surface_id:
            surfaces.append(surface_id)
        else:
            errors.append("Estate surface has an empty id")

        display_id = surface_id or "<unknown>"
        surface_kind = str(surface.get("kind", ""))
        if not surface_kind:
            errors.append(f"Estate surface `{display_id}` must include kind")
        elif surface_kind not in SURFACE_KIND_VALUES:
            errors.append(f"Estate surface `{display_id}` has unknown kind `{surface_kind}`")

        if not surface.get("authority", ""):
            errors.append(f"Estate surface `{display_id}` must include authority")

        for optional_field in ("owner", "description", "handoff"):
            if optional_field in surface and not str(surface[optional_field]).strip():
                errors.append(f"Estate surface `{display_id}` has empty {optional_field}")

        services = surface.get("services", [])
        if isinstance(services, list):
            if "services" in surface and not services:
                warnings.append(f"Estate surface `{display_id}` defines no services")
            for service in services:
                if not isinstance(service, dict):
                    continue
                service_id = str(service.get("id", ""))
                service_label = service_id or "<unknown>"
                if not service_id:
                    errors.append(f"Estate service on surface `{display_id}` has an empty id")
                if not str(service.get("owner", "")).strip():
                    errors.append(f"Estate service `{service_label}` on surface `{display_id}` must include owner")
                proof_required = str(service.get("proof_required", ""))
                if not proof_required:
                    errors.append(
                        f"Estate service `{service_label}` on surface `{display_id}` must include proof_required"
                    )
                elif proof_required not in PROOF_KIND_VALUES:
                    errors.append(
                        f"Estate service `{service_label}` on surface `{display_id}` "
                        f"has unknown proof_required `{proof_required}`"
                    )
                for optional_field in ("purpose", "handoff"):
                    if optional_field in service and not str(service[optional_field]).strip():
                        errors.append(
                            f"Estate service `{service_label}` on surface `{display_id}` has empty {optional_field}"
                        )

    if not name_seen:
        errors.append("Estate must define non-empty name")

    if not surfaces:
        errors.append("Estate must define at least one surface with `- id:`")

    known_surfaces = set(surfaces)
    for flow in flow_records:
        source = str(flow.get("from", ""))
        target = str(flow.get("to", ""))
        proof_required = str(flow.get("proof_required", ""))

        if not source:
            errors.append("Estate flow has an empty source surface")
        if not target:
            errors.append("Estate flow has an empty target surface")
        if source not in known_surfaces:
            errors.append(f"Estate flow references unknown source surface `{source}`")
        if target not in known_surfaces:
            errors.append(f"Estate flow references unknown target surface `{target}`")

        if not proof_required:
            errors.append(f"Estate flow from `{source}` to `{target}` must include proof_required")
        elif proof_required not in PROOF_KIND_VALUES:
            errors.append(f"Estate flow from `{source}` to `{target}` has unknown proof_required `{proof_required}`")

        for optional_field in ("intent", "handoff"):
            if optional_field in flow and not str(flow[optional_field]).strip():
                errors.append(f"Estate flow from `{source}` to `{target}` has empty {optional_field}")

    if not flows_seen:
        errors.append("Estate must define flows section")
    elif not flow_records:
        warnings.append("Estate defines no flows")

    return EstateResult(errors=tuple(errors), warnings=tuple(warnings), surfaces=tuple(surfaces))


def line_for_offset(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def rule_match_offsets(text: str, rule: PrivacyRule) -> tuple[int, ...]:
    if rule.literal is not None:
        if not rule.literal:
            return ()
        offsets: list[int] = []
        start = 0
        while True:
            index = text.find(rule.literal, start)
            if index < 0:
                return tuple(offsets)
            offsets.append(index)
            start = index + len(rule.literal)

    if rule.pattern is None:
        return ()
    return tuple(match.start() for match in rule.pattern.finditer(text))


def scan_privacy_findings(text: str, extra_rules: tuple[PrivacyRule, ...] = ()) -> tuple[PrivacyFinding, ...]:
    findings: list[PrivacyFinding] = []
    for rule in (*BUILTIN_PRIVACY_RULES, *extra_rules):
        for offset in rule_match_offsets(text, rule):
            findings.append(
                PrivacyFinding(line=line_for_offset(text, offset), rule_id=rule.rule_id, description=rule.description)
            )
    return tuple(findings)


def scan_privacy(text: str, extra_rules: tuple[PrivacyRule, ...] = ()) -> ContractResult:
    errors: list[str] = []
    seen_rules: set[str] = set()
    for finding in scan_privacy_findings(text, extra_rules):
        if finding.rule_id in seen_rules:
            continue
        seen_rules.add(finding.rule_id)
        errors.append(privacy_finding_error(finding))
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
