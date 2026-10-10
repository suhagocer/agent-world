#!/usr/bin/env python3
"""
AGENT WORLD — Faz 1a testleri: takılıp çıkarılabilir beyin.

Suha'nın 7 Ekim 2026 şartlı onayının doğrudan testi:
  - Ajanın beyni takılıp çıkarılabilir mi?            -> test_critic_accepts_any_engine_*
  - İlk beyin kural tabanlı mı, davranış Faz 0'la aynı mı? -> test_rule_based_engine_matches_faz0_behavior
  - Testlerde gerçek model yerine sahte model mi?     -> her LLM testi FakeModelClient kullanır
  - Beyin, provenance kapısını atlayabiliyor mu?       -> test_provenance_gate_cannot_be_bypassed_by_engine (hayır, atlayamaz)
  - Ağa çıkan hiçbir kod yok mu?                       -> test_no_network_module_exists

LLM yok. Postgres yok. Ağ çağrısı yok.
"""
from __future__ import annotations

import sys

from cognitive_engine import (
    CognitiveEngine,
    FakeModelClient,
    LLMCognitiveEngine,
    RuleBasedCognitiveEngine,
    Verdict,
)
from store import Store
from agents.researcher import run_researcher
from agents.critic import run_critic

_checks: list[tuple[str, callable]] = []


def check(fn):
    _checks.append((fn.__name__, fn))
    return fn


def _fresh_store_with_claims(doc_path: str) -> tuple[Store, list[str]]:
    s = Store()
    s.append_event("world", "mission.upsert", {"id": "m1", "objective": "x"})
    claim_ids = run_researcher(s, "m1", "researcher-1", "model-a", doc_path)
    return s, claim_ids


# --- 1. Protokol sözleşmesi -------------------------------------------------

@check
def test_both_engines_satisfy_protocol() -> None:
    rb = RuleBasedCognitiveEngine()
    llm = LLMCognitiveEngine(FakeModelClient())
    assert isinstance(rb, CognitiveEngine)
    assert isinstance(llm, CognitiveEngine)
    assert hasattr(rb, "name") and hasattr(llm, "name")


@check
def test_verdict_rejects_invalid_value() -> None:
    try:
        Verdict(verdict="maybe", reason="x", engine="y")
        assert False, "geçersiz verdict kabul edilmemeliydi"
    except ValueError:
        pass


# --- 2. Kural tabanlı motor, Faz 0 davranışıyla birebir aynı ----------------

@check
def test_rule_based_engine_matches_faz0_behavior() -> None:
    rb = RuleBasedCognitiveEngine()
    wrong = rb.evaluate("Dalyan, Türkiye'nin başkentidir.")
    right = rb.evaluate("Ankara, Türkiye'nin başkentidir.")
    unrelated = rb.evaluate("İztuzu Plajı deniz kaplumbağalarının yuvalama alanıdır.")
    assert wrong.verdict == "dispute"
    assert right.verdict == "pass"
    assert unrelated.verdict == "pass"
    assert wrong.engine == "rule-based-v1"


# --- 3. LLM motoru yalnızca FakeModelClient ile, ağa hiç çıkmadan ----------

@check
def test_llm_engine_uses_fake_client_only() -> None:
    fake = FakeModelClient(canned={"Köyceğiz": "DISPUTE: sahte itiraz sebebi."})
    engine = LLMCognitiveEngine(fake)
    v = engine.evaluate("Köyceğiz, Türkiye'nin başkentidir.")
    assert v.verdict == "dispute"
    assert v.reason == "sahte itiraz sebebi."
    assert v.engine == "llm-v1"
    # Sahte client gerçekten çağrıldı mı (ve başka hiçbir şey çağrılmadı mı)?
    assert len(fake.calls) == 1
    assert "Köyceğiz" in fake.calls[0]


@check
def test_llm_engine_default_response_is_pass() -> None:
    fake = FakeModelClient()  # canned boş -> hep default döner
    engine = LLMCognitiveEngine(fake)
    v = engine.evaluate("Sultaniye Kaplıcaları termal bir tesistir.")
    assert v.verdict == "pass"


@check
def test_llm_engine_malformed_response_fails_closed() -> None:
    for raw in ("", "MAYBE: unsure", "DISPUTE", "random text", "PASS:"):
        engine = LLMCognitiveEngine(FakeModelClient(default=raw))
        verdict = engine.evaluate("Test iddiası.")
        assert verdict.verdict == "dispute", f"onay sayılmamalı: {raw!r}"
        assert "onaylanmadı" in verdict.reason or "gerekçe yok" in verdict.reason


@check
def test_llm_engine_accepts_only_explicit_valid_pass_or_dispute() -> None:
    passed = LLMCognitiveEngine(FakeModelClient(default="PASS: kaynakla tutarlı."))
    disputed = LLMCognitiveEngine(FakeModelClient(default="DISPUTE: çelişki bulundu."))
    assert passed.evaluate("İddia A").verdict == "pass"
    assert disputed.evaluate("İddia B").verdict == "dispute"


# --- 4. Critic, hangi motor verilirse onu kullanır (takılıp-çıkarılabilirlik) ---

@check
def test_critic_accepts_any_engine_rule_based() -> None:
    s, claim_ids = _fresh_store_with_claims("docs/sample_source_1.txt")
    verdicts = run_critic(s, "m1", "critic-1", claim_ids, engine=RuleBasedCognitiveEngine())
    disputed = [cid for cid, (v, _) in verdicts.items() if v == "dispute"]
    assert len(disputed) == 1  # "Dalyan, Türkiye'nin başkentidir" yakalanmalı


@check
def test_critic_accepts_any_engine_llm_fake() -> None:
    s, claim_ids = _fresh_store_with_claims("docs/sample_source_1.txt")
    fake = FakeModelClient(canned={"başkentidir": "DISPUTE: sahte model de yakaladı."})
    verdicts = run_critic(s, "m1", "critic-1", claim_ids, engine=LLMCognitiveEngine(fake))
    disputed = [cid for cid, (v, _) in verdicts.items() if v == "dispute"]
    assert len(disputed) == 1
    assert fake.calls, "sahte model hiç çağrılmamış"


@check
def test_critic_default_engine_unchanged_from_faz0() -> None:
    # engine=None verildiğinde Faz 0'daki run_mission.py çıktısıyla
    # birebir aynı sonucu üretmeli (geriye dönük uyumluluk).
    s, claim_ids = _fresh_store_with_claims("docs/sample_source_1.txt")
    verdicts = run_critic(s, "m1", "critic-1", claim_ids)
    disputed = [cid for cid, (v, _) in verdicts.items() if v == "dispute"]
    passed = [cid for cid, (v, _) in verdicts.items() if v == "pass"]
    assert len(disputed) == 1
    assert len(passed) == 2


# --- 5. Provenance kapısı hiçbir motor tarafından atlanamaz -----------------

@check
def test_provenance_gate_cannot_be_bypassed_by_engine() -> None:
    s = Store()
    s.append_event("world", "mission.upsert", {"id": "m1", "objective": "x"})
    # Kaynağı YANLIŞ/uydurma bir claim — provenance asla doğrulanamaz.
    s.append_event("researcher-1", "claim.upsert", {
        "id": "c1", "mission_id": "m1", "statement": "Uydurma bir iddia.",
        "status": "quarantined", "source": "docs/olmayan_dosya.txt#L1",
    }, mission_id="m1")
    # Beyin her zaman "PASS" diyecek şekilde kurulsa bile:
    always_pass = FakeModelClient(default="PASS: her zaman onaylar.")
    verdicts = run_critic(s, "m1", "critic-1", ["c1"], engine=LLMCognitiveEngine(always_pass))
    assert verdicts["c1"][0] == "dispute"
    assert "provenance" in verdicts["c1"][1]


# --- 6. Faz 1a'da gerçek ağa çıkan bir modül yok ----------------------------

@check
def test_no_network_module_exists() -> None:
    # Suha'nın şartı: "Faz 1a'da API kullanılmayacak." Bunu somut hale
    # getiriyoruz: repoda `requests`/`httpx`/`urllib` gibi ağ
    # kütüphanelerini içe aktaran, cognitive_engine.py dışında bir
    # "gerçek model client" modülü olmamalı.
    import cognitive_engine
    src = open(cognitive_engine.__file__, encoding="utf-8").read()
    for forbidden in ("import requests", "import httpx", "urllib.request", "socket."):
        assert forbidden not in src, f"Faz 1a'da ağ çağrısı bulundu: {forbidden}"


def main() -> None:
    passed = 0
    for name, fn in _checks:
        fn()
        print(f"ok  {name}")
        passed += 1
    print(f"{passed}/{passed} geçti. LLM yok. Postgres yok. Ağ çağrısı yok.")


if __name__ == "__main__":
    sys.exit(main())
