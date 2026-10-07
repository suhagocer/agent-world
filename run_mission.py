#!/usr/bin/env python3
"""
AGENT WORLD — Faz 0 ilk uçtan uca mission (DeepSeek'in önerisi, Claude'un
uygulaması; rule-based, LLM yok, Postgres yok)
"""
from __future__ import annotations

from agents.critic import run_critic
from agents.researcher import run_researcher
from agents.verifier import run_verifier
from store import Store

def setup_models(store: Store) -> None:
    store.append_event("world", "model.upsert", {
        "model_id": "deepseek-engineer", "provider": "deepseek",
        "family": "deepseek-family", "family_verified": True,
    })
    store.append_event("world", "model.upsert", {
        "model_id": "claude-sonnet-5", "provider": "anthropic",
        "family": "claude-family", "family_verified": True,
    })

def setup_agents(store: Store) -> None:
    store.append_event("world", "agent.upsert", {"agent_id": "researcher-1", "capability": "producer", "model_id": "deepseek-engineer"})
    store.append_event("world", "agent.upsert", {"agent_id": "critic-1", "capability": "critic", "model_id": "claude-sonnet-5"})
    store.append_event("world", "agent.upsert", {"agent_id": "verifier-1", "capability": "verifier", "model_id": "claude-sonnet-5"})

def run_one_mission(store: Store, mission_id: str, doc_path: str, skill_reused: bool) -> dict[str, str]:
    store.append_event("world", "mission.upsert", {
        "id": mission_id,
        "objective": f"{doc_path} içindeki gerçekleri çıkar, doğrula",
        "claim_type": "factual",
        "budget_time_seconds": 600,
    })
    store.acquire_lease(mission_id, "researcher-1", ttl=600)

    producer_model = store.agents["researcher-1"].model_id
    critic_model = store.agents["verifier-1"].model_id

    claim_ids = run_researcher(
        store, mission_id, "researcher-1", producer_model, doc_path,
        skill_reused=skill_reused,
    )
    verdicts = run_critic(store, mission_id, "critic-1", claim_ids)
    final_status = run_verifier(
        store, mission_id, verdicts, producer_model, critic_model,
    )

    store.append_event("world", "mission.upsert", {"id": mission_id, "status": "submitted"})
    all_resolved = all(s in ("verified", "verified-weak", "disputed") for s in final_status.values())
    store.append_event("world", "mission.upsert", {
        "id": mission_id, "status": "verified" if all_resolved else "evaluating",
    })

    # Current canonical store.py has no release_lease() method.
    # Voluntary release is represented by the canonical lease.release event.
    store.append_event(
        "researcher-1", "lease.release",
        {"mission_id": mission_id},
        mission_id=mission_id,
    )
    return final_status

def token_cost_for_mission(store: Store, mission_id: str) -> int:
    return sum(
        ev.payload.get("token_cost", 0)
        for ev in store.events
        if ev.mission_id == mission_id and ev.type == "research.extracted"
    )

def main() -> None:
    store = Store()
    setup_models(store)
    setup_agents(store)

    print("=== Mission 1: docs/sample_source_1.txt (ilk kullanım, skill yok) ===")
    final_1 = run_one_mission(store, "mission-1", "docs/sample_source_1.txt", skill_reused=False)
    for claim_id, status in final_1.items():
        stmt = store.claims[claim_id].statement
        print(f"  [{status:14s}] {claim_id}  — {stmt}")
    cost_1 = token_cost_for_mission(store, "mission-1")
    print(f"  token_cost (mission-1): {cost_1}")
    print(f"  lease_holder (mission-1) bitişte: {store.missions['mission-1'].lease_holder!r} (None olmalı)")

    print()
    print("=== Mission 2: docs/sample_source_2.txt (aynı desen, skill_reused=True) ===")
    final_2 = run_one_mission(store, "mission-2", "docs/sample_source_2.txt", skill_reused=True)
    for claim_id, status in final_2.items():
        stmt = store.claims[claim_id].statement
        print(f"  [{status:14s}] {claim_id}  — {stmt}")
    cost_2 = token_cost_for_mission(store, "mission-2")
    print(f"  token_cost (mission-2): {cost_2}")

    print()
    reduction_pct = round(100 * (1 - cost_2 / cost_1), 1) if cost_1 else 0.0
    # Yer tutucu. Yüzde, elde yazılı 120 ve 40 sayısından çıkar. Ölçülmüş LLM token değildir.
    print(
        f"Skill reuse etkisi: mission-1={cost_1} token -> mission-2={cost_2} token "
        f"({reduction_pct}% düşüş, yer tutucu, ölçülmüş LLM token değil)."
    )
    print()
    print(f"Hash zinciri (verify_chain): {'SAĞLAM' if store.verify_chain() else 'BOZUK'}")
    print(f"Toplam event sayısı: {len(store.events)}")

    disputed = [cid for cid, st in {**final_1, **final_2}.items() if st == "disputed"]
    verified = [cid for cid, st in {**final_1, **final_2}.items() if st in ("verified", "verified-weak")]
    print()
    print(f"Sonuç: {len(verified)} claim verified/verified-weak, {len(disputed)} claim disputed (Critic'in yakaladığı yanlış 'başkent' iddiaları).")

if __name__ == "__main__":
    main()
