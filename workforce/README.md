# Jessica's Autonomous Workforce Engine (JAWE) — experimental v0.1

**Status: proposal engine only. No provider API, GPU training, automatic role activation, or production deployment.**

## Architecture
Business need → reuse check → role proposal → capability/model routing → sandbox evaluation → human approval → execution (future) → redacted traces → consented training dataset → offline fine-tuning/evaluation (future) → gated rollout.

`engine.py` is a standard-library-only starting point that:
- proposes a specialist role from a business need without granting permissions;
- routes among configurable model *families* (Qwen, Kimi, GLM, DeepSeek, MiniMax, Nemotron) using an auditable capability heuristic;
- refuses duplicate category roles and records minimal metrics with training consent disabled by default.

Run: `python workforce/engine.py`

## Integration backlog
1. Replace keyword proposal with schema-validated LLM planner, with role reuse, budgets, provenance and adversarial-input tests.
2. Add versioned provider adapters and model registry (model IDs, licenses, regions, pricing, availability, tool support, eval scores).
3. Implement benchmark-based model router with fallback, per-request quality/cost/latency metrics and provider circuit breakers.
4. Add scoped Skills, sandbox, immutable audit logs, explicit approval for external actions and spending caps.
5. Separate customer data by tenant. Never use private data for training without affirmative, revocable permission; redact PII and secrets.
6. Add training pipeline: curated traces → human-reviewed labels → held-out evaluation → LoRA/SFT or RL when justified → rollback-capable canary deployment.
7. Test against the existing 000–019 roles and governance before merging or enabling.

## Applied Compute inspiration
AC2 describes open-weight model post-training, production trace capture, online evaluation and model routing. This is a clean-room architectural adaptation, **not** AC2 source code, an AC2 integration, or proof of model training.

Official technical references:
- https://www.appliedcompute.com/platform/introducing-ac2
- https://www.appliedcompute.com/routers
- https://www.appliedcompute.com/inference

**Security:** no auto-generated role may send mail, transfer funds, deploy code, access health records, or train on customer data without separately granted authorization.
