"""JAWE v0.1: deterministic, reviewable workforce proposals. No autonomous execution."""
from dataclasses import dataclass, asdict
from typing import Sequence
import json
import re

MODEL_CATALOG = {
    "qwen": {"strengths": ("multilingual", "documents", "general"), "provider": "configurable"},
    "kimi": {"strengths": ("long_context", "coding", "research"), "provider": "configurable"},
    "glm": {"strengths": ("tools", "general"), "provider": "configurable"},
    "deepseek": {"strengths": ("reasoning", "coding"), "provider": "configurable"},
    "minimax": {"strengths": ("content", "general"), "provider": "configurable"},
    "nemotron": {"strengths": ("reasoning", "agents"), "provider": "configurable"},
}
# Registry entries describe families, not validated model versions or API access.
ROLE_SKILLS = {
    "research": ("research", "documents"),
    "engineering": ("coding", "tools"),
    "marketing": ("content", "multilingual"),
    "finance": ("reasoning", "documents"),
    "operations": ("tools", "general"),
}
SENSITIVE = ("payment", "transfer", "send email", "delete", "deploy", "medical", "financial advice")

@dataclass(frozen=True)
class RoleProposal:
    name: str
    mission: str
    model_family: str
    skills: tuple[str, ...]
    status: str = "pending_human_approval"
    execution_enabled: bool = False
    training_enabled: bool = False

def route_model(skills: Sequence[str], allowed: Sequence[str] | None = None) -> str:
    """Simple transparent baseline router; replace only after benchmark evaluation."""
    eligible = set(MODEL_CATALOG if allowed is None else allowed)
    scores = {model: len(set(skills) & set(info["strengths"]))
              for model, info in MODEL_CATALOG.items() if model in eligible}
    if not scores:
        raise ValueError("No permitted model family")
    return sorted(scores, key=lambda model: (-scores[model], model))[0]

def propose_role(business_need: str, existing_roles: Sequence[str] = ()) -> RoleProposal:
    """Generate a proposed role template, never an executable agent."""
    need = business_need.strip()
    if not 5 <= len(need) <= 2000:
        raise ValueError("Business need must contain 5–2000 characters")
    lowered = need.lower()
    categories = {
        "engineering": ("code", "software", "website", "app", "开发", "网站"),
        "marketing": ("market", "campaign", "brand", "营销", "品牌"),
        "finance": ("budget", "invoice", "finance", "预算", "财务"),
        "research": ("research", "analyse", "report", "研究", "报告"),
    }
    category = next((name for name, terms in categories.items()
                     if any(term in lowered for term in terms)), "operations")
    name = category + "-specialist"
    if name in {r.lower() for r in existing_roles}:
        raise ValueError("Existing role can cover this category; review reuse first")
    skills = ROLE_SKILLS[category]
    return RoleProposal(name=name, mission=need, model_family=route_model(skills), skills=skills)

def record_feedback(task_id: str, approved: bool, quality: float, cost_usd: float) -> str:
    """Return a redacted training-candidate record, not a model update."""
    if not re.fullmatch(r"[A-Za-z0-9_-]{1,80}", task_id):
        raise ValueError("Invalid task id")
    import math
    if not (math.isfinite(quality) and math.isfinite(cost_usd) and 0 <= quality <= 1 and 0 <= cost_usd <= 100000):
        raise ValueError("Invalid metrics")
    return json.dumps({"task_id": task_id, "approved": approved,
                       "quality": quality, "cost_usd": cost_usd,
                       "training_consent": False, "eligible_for_training": False})

if __name__ == "__main__":
    print(json.dumps(asdict(propose_role("Build a multilingual marketing campaign")),
                     indent=2, ensure_ascii=False))
