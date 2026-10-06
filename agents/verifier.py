"""
AGENT WORLD — Faz 0 Verifier ajanı (kural-tabanlı, LLM yok)
"""
from __future__ import annotations
from store import Store

def run_verifier(store: Store, mission_id: str,
                 verdicts: dict[str, tuple[str, str]],
                 producer_model: str, critic_model: str) -> dict[str, str]:
    final: dict[str, str] = {}
    for claim_id, (verdict, _reason) in verdicts.items():
        claim = store.claims[claim_id]
        if verdict != "pass":
            final[claim_id] = claim.status
            continue
        store.verify_claim(
            claim_id,
            producer_model=producer_model,
            critic_model=critic_model,
            source=claim.source or "",
        )
        final[claim_id] = store.claims[claim_id].status
    return final
