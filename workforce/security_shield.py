"""JBASS: fail-closed policy gate for proposed AI workforce actions.

This is a policy enforcement prototype, NOT a network firewall, cryptographic
vault, malware scanner, or production identity provider.
"""
from dataclasses import dataclass
from typing import FrozenSet
import re

HIGH_RISK = frozenset({"send_email", "deploy", "payment", "transfer_funds", "delete_data",
                       "install_code", "execute_code", "model_training", "read_health_data",
                       "read_genetic_data", "export_data", "change_permissions"})
READ_ONLY = frozenset({"read_public_repo", "propose_role", "propose_upgrade", "read_public_docs"})
VALID_ACTIONS = HIGH_RISK | READ_ONLY

@dataclass(frozen=True)
class Principal:
    bot_id: str
    tenant_id: str
    permissions: FrozenSet[str]

@dataclass(frozen=True)
class Decision:
    allowed: bool
    reason: str

def authorize(principal: Principal, action: str, resource_tenant: str,
              approval: bool = False, sandbox: bool = False) -> Decision:
    """Deny unknown operations, cross-tenant access, and unapproved high-risk actions."""
    if not principal.bot_id or not re.fullmatch(r"[A-Za-z0-9_-]{1,80}", principal.tenant_id):
        return Decision(False, "invalid_identity")
    if action not in VALID_ACTIONS:
        return Decision(False, "unknown_action")
    if resource_tenant != principal.tenant_id:
        return Decision(False, "cross_tenant_denied")
    if action not in principal.permissions:
        return Decision(False, "permission_denied")
    if action in HIGH_RISK and not approval:
        return Decision(False, "human_approval_required")
    if action in {"execute_code", "install_code", "model_training"} and not sandbox:
        return Decision(False, "sandbox_required")
    return Decision(True, "authorized")

def default_new_role(bot_id: str, tenant_id: str) -> Principal:
    """Newly generated roles cannot execute external actions or access private data."""
    return Principal(bot_id, tenant_id, frozenset({"propose_role", "propose_upgrade", "read_public_docs"}))
