"""
AGENT WORLD — Faz 0 Researcher ajanı (kural-tabanlı, LLM yok)
"""
from __future__ import annotations
import re
from dataclasses import dataclass
from pathlib import Path
from store import Store

_FACT_LINE = re.compile(r"^FACT:\s*(.+)$")

@dataclass
class ExtractedFact:
    line_no: int
    statement: str
    source_ref: str

def extract_facts(doc_path: str | Path) -> list[ExtractedFact]:
    doc_path = Path(doc_path)
    facts: list[ExtractedFact] = []
    for i, line in enumerate(doc_path.read_text(encoding="utf-8").splitlines(), start=1):
        m = _FACT_LINE.match(line.strip())
        if m:
            facts.append(ExtractedFact(i, m.group(1).strip(), f"{doc_path.as_posix()}#L{i}"))
    return facts

def run_researcher(store: Store, mission_id: str, agent_id: str,
                   producer_model: str, doc_path: str | Path,
                   skill_reused: bool = False) -> list[str]:
    facts = extract_facts(doc_path)
    claim_ids: list[str] = []
    # Yer tutucu. Ölçülmüş LLM token değildir. 120 ve 40 elde yazılı sayıdır.
    token_cost_per_fact = 40 if skill_reused else 120
    for fact in facts:
        claim_id = f"{mission_id}:{fact.line_no}"
        store.append_event(agent_id, "claim.upsert", {
            "id": claim_id, "mission_id": mission_id, "statement": fact.statement,
            "status": "quarantined", "source": fact.source_ref,
            "producer_model": producer_model,
        }, mission_id=mission_id)
        store.append_event(agent_id, "research.extracted", {
            "claim_id": claim_id, "source": fact.source_ref,
            "skill_reused": skill_reused, "token_cost": token_cost_per_fact,
        }, mission_id=mission_id)
        claim_ids.append(claim_id)
    return claim_ids
