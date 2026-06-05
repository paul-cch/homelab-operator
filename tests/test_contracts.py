from __future__ import annotations

from pathlib import Path

from homelab_operator.cli import main
from homelab_operator.contracts import evaluate_pr_body, evaluate_receipt, evaluate_surface_claim, receipt_template


FIXTURES = Path(__file__).parent / "fixtures"


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


def test_surface_claim_passes() -> None:
    result = evaluate_surface_claim((FIXTURES / "surface_claim.json").read_text(encoding="utf-8"))

    assert result.ok


def test_init_writes_templates(tmp_path: Path) -> None:
    assert main(["init", "--target", str(tmp_path)]) == 0

    assert (tmp_path / "AGENTS.md").exists()
    assert (tmp_path / ".github/pull_request_template.md").exists()
    assert (tmp_path / ".github/workflows/homelab-operator-contract.yml").exists()
