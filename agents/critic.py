"""
AGENT WORLD — Faz 0 Critic ajanı (kural-tabanlı, LLM yok)
"""
from __future__ import annotations
import re
from pathlib import Path
from store import Store

_KNOWN_CAPITALS = {"Türkiye": "Ankara"}
_CAPITAL_CLAIM = re.compile(r"^(?P<subject>.+?),?\s*Türkiye'nin başkentidir\.?$")

def _rule_based_check(statement: str) -> tuple[bool, str]:
    m = _CAPITAL_CLAIM.match(statement)
    if m:
        subject = m.group("subject").strip()
        known = _KNOWN_CAPITALS["Türkiye"]
        if subject != known:
            return False, f"bilinen-gerçekler çelişkisi: Türkiye'nin başkenti '{known}'dır, '{subject}' değil."
    return True, ""

def _source_actually_contains(statement: str, source_ref: str) -> bool:
    path_part, _, line_part = source_ref.rpartition("#L")
    if not path_part or not line_part.isdigit():
        return False
    path = Path(path_part)
    if not path.exists():
        return False
    lines = path.read_text(encoding="utf-8").splitlines()
    idx = int(line_part) - 1
    if idx < 0 or idx >= len(lines):
        return False
    return statement in lines[idx]

def run_critic(store: Store, mission_id: str, agent_id: str,
               claim_ids: list[str]) -> dict[str, tuple[str, str]]:
    verdicts: dict[str, tuple[str, str]] = {}
    for claim_id in claim_ids:
        claim = store.claims[claim_id]
        provenance_ok = _source_actually_contains(claim.statement, claim.source or "")
        rule_ok, reason = _rule_based_check(claim.statement)
        if not provenance_ok:
            verdict, why = "dispute", "provenance kontrolü başarısız: kaynakta birebir bulunamadı."
        elif not rule_ok:
            verdict, why = "dispute", reason
        else:
            verdict, why = "pass", "provenance doğrulandı, bilinen-gerçekler çelişkisi yok."
        store.append_event(agent_id, "critic.review", {
            "claim_id": claim_id, "verdict": verdict, "reason": why,
        }, mission_id=mission_id)
        if verdict == "dispute":
            store.append_event(agent_id, "claim.upsert", {
                "id": claim_id, "mission_id": mission_id, "status": "disputed",
            }, mission_id=mission_id)
        verdicts[claim_id] = (verdict, why)
    return verdicts
