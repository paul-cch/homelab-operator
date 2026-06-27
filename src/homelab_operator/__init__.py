"""Homelab Operator contract toolkit."""

from .contracts import (
    ContractResult,
    PrivacyConfigError,
    PrivacyRule,
    evaluate_estate,
    evaluate_pr_body,
    evaluate_receipt,
    evaluate_surface_claim,
    load_privacy_config,
    receipt_template,
    scan_privacy,
)

__all__ = [
    "ContractResult",
    "PrivacyConfigError",
    "PrivacyRule",
    "evaluate_estate",
    "evaluate_pr_body",
    "evaluate_receipt",
    "evaluate_surface_claim",
    "load_privacy_config",
    "receipt_template",
    "scan_privacy",
]
