"""
AGENT WORLD — Faz 0/1a Critic ajanı.

Faz 1a değişikliği (Suha'nın 7 Ekim 2026 şartlı onayı, madde 2+5): içerik
kararı artık sabit kodlanmış değil, takılıp çıkarılabilir bir
CognitiveEngine'den geliyor. Varsayılan hâlâ RuleBasedCognitiveEngine —
davranış Faz 0'dakiyle birebir aynı. Provenance kontrolü ise HİÇBİR
motor tarafından atlanamayan, world-seviyesinde ayrı bir kapı olarak
kalıyor (bir "beyin" kaynağı sahte/yanlış olduğunu söyleyemez).
"""
from __future__ import annotations
from pathlib import Path
from store import Store
from cognitive_engine import CognitiveEngine, RuleBasedCognitiveEngine

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
               claim_ids: list[str],
               engine: CognitiveEngine | None = None) -> dict[str, tuple[str, str]]:
    """`engine` verilmezse Faz 0 davranışıyla birebir aynı
    RuleBasedCognitiveEngine kullanılır — geriye dönük uyumluluk
    korunur, run_mission.py'de hiçbir çağrı değişmeden çalışmaya
    devam eder."""
    engine = engine or RuleBasedCognitiveEngine()
    verdicts: dict[str, tuple[str, str]] = {}
    for claim_id in claim_ids:
        claim = store.claims[claim_id]
        # Provenance kapısı: hiçbir beyin bunu atlayamaz (world kuralı,
        # "cognition" değil).
        provenance_ok = _source_actually_contains(claim.statement, claim.source or "")
        content_verdict = engine.evaluate(claim.statement)
        if not provenance_ok:
            verdict, why = "dispute", "provenance kontrolü başarısız: kaynakta birebir bulunamadı."
        elif content_verdict.verdict == "dispute":
            verdict, why = "dispute", content_verdict.reason
        else:
            verdict, why = "pass", f"provenance doğrulandı, {content_verdict.engine}: {content_verdict.reason}"
        store.append_event(agent_id, "critic.review", {
            "claim_id": claim_id, "verdict": verdict, "reason": why,
        }, mission_id=mission_id)
        if verdict == "dispute":
            store.append_event(agent_id, "claim.upsert", {
                "id": claim_id, "mission_id": mission_id, "status": "disputed",
            }, mission_id=mission_id)
        verdicts[claim_id] = (verdict, why)
    return verdicts
