from __future__ import annotations

import json
from pathlib import Path

from homelab_operator.cli import main
from homelab_operator.contracts import (
    ProofKind,
    RECEIPT_FIELDS,
    SurfaceKind,
    evaluate_estate,
    evaluate_pr_body,
    evaluate_receipt,
    evaluate_surface_claim,
    receipt_template,
    scan_privacy,
)


FIXTURES = Path(__file__).parent / "fixtures"
SCHEMAS = Path(__file__).parents[1] / "schemas"
HOOKS = Path(__file__).parents[1] / ".pre-commit-hooks.yaml"

RECEIPT_SCHEMA_KEYS = {
    "Exit state": "exit_state",
    "Issue": "issue",
    "Branch / worktree": "branch_or_worktree",
    "PR": "pr",
    "Owned paths": "owned_paths",
    "Surface classification": "surface_classification",
    "Proof kind": "proof_kind",
    "Claim proven": "claim_proven",
    "Claim not proven": "claim_not_proven",
    "Repo gate": "repo_gate",
    "Host/runtime handoff needed": "host_runtime_handoff_needed",
    "Host gate needed": "host_gate_needed",
    "Runtime gate needed": "runtime_gate_needed",
    "Live config gate needed": "live_config_gate_needed",
    "Checks or commands run": "checks_or_commands_run",
    "Blockers": "blockers",
    "Next safe command": "next_safe_command",
}


def load_schema(name: str) -> dict[str, object]:
    return json.loads((SCHEMAS / name).read_text(encoding="utf-8"))


def test_good_pr_body_passes() -> None:
    result = evaluate_pr_body((FIXTURES / "good_pr_body.md").read_text(encoding="utf-8"))

    assert result.ok
    assert "src/homelab_operator/contracts.py" in result.owned_paths


def test_missing_claim_boundary_fails() -> None:
    result = evaluate_pr_body((FIXTURES / "bad_pr_body_missing_boundary.md").read_text(encoding="utf-8"))

    assert not result.ok
    assert "PR body must state the source/host/runtime/live-config claim boundary" in result.errors


def test_partial_work_cannot_close_issue() -> None:
    body = """## Summary
First slice of the checker.

## Linked Issue
Closes #12

## Owned Paths
- `src/homelab_operator/contracts.py`

## Validation
- `python -m pytest` passed.

## Claim Boundary
Repo-only proof. No runtime claim.
"""

    result = evaluate_pr_body(body)

    assert not result.ok
    assert "Partial or follow-up work must use `Refs #...` or `Part of #...`, not a closing keyword" in result.errors


def test_receipt_template_includes_state() -> None:
    receipt = receipt_template("CLEAN_NO_OP")

    assert "- Exit state: CLEAN_NO_OP" in receipt
    assert "- Claim not proven:" in receipt


def test_good_receipt_passes() -> None:
    result = evaluate_receipt((FIXTURES / "good_receipt.md").read_text(encoding="utf-8"))

    assert result.ok
    assert result.fields["Proof kind"] == "repo_only"


def test_bad_receipt_fails_on_empty_claim() -> None:
    result = evaluate_receipt((FIXTURES / "bad_receipt_empty_claim.md").read_text(encoding="utf-8"))

    assert not result.ok
    assert "Claim proven must not be empty" in result.errors


def test_receipt_rejects_empty_gate_field() -> None:
    receipt = (FIXTURES / "good_receipt.md").read_text(encoding="utf-8").replace(
        "- Host gate needed: no", "- Host gate needed:"
    )

    result = evaluate_receipt(receipt)

    assert not result.ok
    assert "Host gate needed must not be empty" in result.errors


def test_receipt_schema_requires_runtime_fields() -> None:
    schema = load_schema("lane-receipt.schema.json")
    expected = {RECEIPT_SCHEMA_KEYS[field] for field in RECEIPT_FIELDS}

    assert set(schema["required"]) == expected


def test_receipt_schema_includes_gate_properties() -> None:
    properties = load_schema("lane-receipt.schema.json")["properties"]

    for key in (
        "host_runtime_handoff_needed",
        "host_gate_needed",
        "runtime_gate_needed",
        "live_config_gate_needed",
    ):
        assert properties[key]["minLength"] == 1


def test_surface_claim_passes() -> None:
    result = evaluate_surface_claim((FIXTURES / "surface_claim.json").read_text(encoding="utf-8"))

    assert result.ok


def test_surface_claim_rejects_unknown_surface() -> None:
    result = evaluate_surface_claim(
        json.dumps(
            {
                "surface": "runtime",
                "proof_kind": "runtime_export_only",
                "claim_proven": "synthetic runtime export checked",
                "claim_not_proven": "no live service checked",
            }
        )
    )

    assert not result.ok
    assert "Surface claim has unknown surface" in result.errors


def test_surface_claim_schema_enums_match_runtime() -> None:
    properties = load_schema("surface-claim.schema.json")["properties"]

    assert properties["surface"]["enum"] == [kind.value for kind in SurfaceKind]
    assert properties["proof_kind"]["enum"] == [kind.value for kind in ProofKind]


def test_estate_passes() -> None:
    result = evaluate_estate(Path("examples/minimal-homelab/estate.yaml").read_text(encoding="utf-8"))

    assert result.ok
    assert set(result.surfaces) == {"source", "host", "runtime", "live-config"}


def test_estate_rejects_unknown_flow_target() -> None:
    result = evaluate_estate(
        """name: bad
surfaces:
  - id: source
    kind: repo
flows:
  - from: source
    to: missing
    proof_required: runtime_export_only
"""
    )

    assert not result.ok
    assert "Estate flow references unknown target surface `missing`" in result.errors


def test_estate_rejects_missing_name_and_flows_section() -> None:
    result = evaluate_estate(
        """surfaces:
  - id: source
    kind: repo
    authority: synthetic-source
"""
    )

    assert not result.ok
    assert "Estate must define non-empty name" in result.errors
    assert "Estate must define flows section" in result.errors


def test_estate_rejects_unknown_surface_kind_and_proof_required() -> None:
    result = evaluate_estate(
        """name: bad
surfaces:
  - id: source
    kind: runtime
    authority: synthetic-source
  - id: runtime
    kind: runtime_export
    authority: synthetic-runtime
flows:
  - from: source
    to: runtime
    proof_required: runtime
"""
    )

    assert not result.ok
    assert "Estate surface `source` has unknown kind `runtime`" in result.errors
    assert "Estate flow from `source` to `runtime` has unknown proof_required `runtime`" in result.errors


def test_estate_schema_enums_match_runtime() -> None:
    schema = load_schema("estate.schema.json")
    surface_properties = schema["properties"]["surfaces"]["items"]["properties"]
    flow_properties = schema["properties"]["flows"]["items"]["properties"]

    assert surface_properties["kind"]["enum"] == [kind.value for kind in SurfaceKind]
    assert flow_properties["proof_required"]["enum"] == [kind.value for kind in ProofKind]


def test_privacy_scan_rejects_private_ip() -> None:
    result = scan_privacy("host: " + ".".join(["192", "168", "1", "20"]))

    assert not result.ok


def test_privacy_scan_accepts_policy_text() -> None:
    result = scan_privacy("Do not publish secrets or private topology.")

    assert result.ok


def test_init_writes_templates(tmp_path: Path) -> None:
    assert main(["init", "--target", str(tmp_path)]) == 0

    assert (tmp_path / "AGENTS.md").exists()
    assert (tmp_path / ".github/pull_request_template.md").exists()
    assert (tmp_path / ".github/workflows/homelab-operator-contract.yml").exists()


def test_doctor_passes_for_repo() -> None:
    assert main(["doctor", "--root", "."]) == 0


def test_pre_commit_hooks_target_supported_cli_commands() -> None:
    hooks = HOOKS.read_text(encoding="utf-8")

    assert "id: homelab-operator-check-privacy" in hooks
    assert "entry: homelab-operator check-privacy --root ." in hooks
    assert "id: homelab-operator-doctor" in hooks
    assert "entry: homelab-operator doctor --root ." in hooks
    assert hooks.count("pass_filenames: false") == 2

    assert main(["check-privacy", "--root", "."]) == 0
    assert main(["doctor", "--root", "."]) == 0
