"""BOT-020 identity/key lifecycle policy prototype.

Never stores, prints, generates or exports live credentials.
"""
from dataclasses import dataclass
from datetime import datetime, timezone
import re

ALLOWED_STATES = frozenset({"requested", "approved", "active", "rotation_due", "revoked"})
ALLOWED_OPERATIONS = frozenset({"inventory", "request", "approve", "rotate", "revoke", "audit"})

@dataclass(frozen=True)
class CredentialMetadata:
    credential_id: str
    tenant_id: str
    service: str
    owner_bot: str
    vault_reference: str
    status: str = "requested"
    expires_at: str | None = None

    def __post_init__(self):
        for field in (self.credential_id, self.tenant_id, self.service, self.owner_bot):
            if not re.fullmatch(r"[A-Za-z0-9_.-]{1,100}", field):
                raise ValueError("Invalid metadata identifier")
        if not self.vault_reference.startswith("vault://"):
            raise ValueError("Only vault references, never plaintext secrets")
        if self.status not in ALLOWED_STATES:
            raise ValueError("Invalid credential lifecycle state")

def propose_key_action(metadata: CredentialMetadata, operation: str, requester: str,
                       approver: str | None = None) -> dict:
    """Emit a non-executable approval request, never a vault operation."""
    if operation not in ALLOWED_OPERATIONS:
        raise ValueError("Unknown operation")
    if not re.fullmatch(r"[A-Za-z0-9_.-]{1,100}", requester):
        raise ValueError("Invalid requester")
    if approver is not None and approver == requester:
        raise ValueError("Separation of duties required")
    return {
        "credential_id": metadata.credential_id,
        "tenant_id": metadata.tenant_id,
        "operation": operation,
        "requested_by": requester,
        "requires_independent_approval": operation in {"approve", "rotate", "revoke"},
        "status": "proposal_only",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
