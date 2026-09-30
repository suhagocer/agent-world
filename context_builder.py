"""Context builder. Behavior contract for Faz 0 golden-file tests."""

from __future__ import annotations

from dataclasses import dataclass

TOKEN_BUDGET_DEFAULT = 8000

_HIDDEN = frozenset({"quarantined", "rejected", "superseded"})
_STATUS_RANK = {
    "verified": 5,
    "verified-weak": 4,
    "disputed": 3,
    "unverified": 2,
    "superseded": 1,
    "rejected": 0,
}


@dataclass
class Claim:
    id: str
    statement: str
    status: str
    tokens: int
    contradicts: str | None = None
    recency: int = 0  # larger = newer


def _sort_key(c: Claim) -> tuple[int, int, str]:
    return (_STATUS_RANK.get(c.status, 0), c.recency, c.id)


def build_context(
    agent: dict,
    mission: dict,
    claims: list[Claim],
    token_budget: int = TOKEN_BUDGET_DEFAULT,
) -> dict:
    visible = [c for c in claims if c.status not in _HIDDEN]
    ordered = sorted(visible, key=_sort_key, reverse=True)
    used, kept = 0, []
    for c in ordered:
        if used + c.tokens > token_budget:
            continue  # skip-over on the frozen order; order does not change
        kept.append(c)
        used += c.tokens
    kept_ids = {c.id for c in kept}
    unresolved = []
    unresolved_incomplete = []
    for c in kept:
        if not c.contradicts:
            continue
        unresolved.append(c.id)
        if c.contradicts not in kept_ids:
            unresolved_incomplete.append(c.id)
    return {
        "agent_id": agent["agent_id"],
        "mission_id": mission["id"],
        "claims": [c.id for c in kept],
        "unresolved": unresolved,
        "unresolved_incomplete": unresolved_incomplete,
        "tokens_used": used,
        "budget_truncated": len(kept) < len(visible),
        "order": [c.id for c in ordered],
    }
