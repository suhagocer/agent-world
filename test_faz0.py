#!/usr/bin/env python3
"""Faz 0 golden-file + event log + lease. No network. No LLM."""

from __future__ import annotations

from datetime import timedelta

from context_builder import TOKEN_BUDGET_DEFAULT, Claim, build_context
from store import Store, _now


def test_budget_overflow() -> None:
    claims = [Claim(f"c{i}", f"stmt{i}", "verified", 3000, recency=i) for i in range(6)]
    ctx = build_context({"agent_id": "producer-1"}, {"id": "m1"}, claims)
    assert ctx["tokens_used"] <= TOKEN_BUDGET_DEFAULT
    assert ctx["budget_truncated"] is True
    # Frozen order: higher recency first among equals.
    assert ctx["order"] == ["c5", "c4", "c3", "c2", "c1", "c0"]


def test_quarantine_filter() -> None:
    claims = [
        Claim("c1", "v", "verified", 500),
        Claim("c2", "v", "verified", 500),
        Claim("c3", "v", "verified", 500),
        Claim("c4", "q", "quarantined", 500),
        Claim("c5", "q", "quarantined", 500),
    ]
    ctx = build_context({"agent_id": "producer-1"}, {"id": "m2"}, claims)
    assert set(ctx["claims"]) == {"c1", "c2", "c3"}
    assert "c4" not in ctx["claims"] and "c5" not in ctx["claims"]


def test_contradiction_carry() -> None:
    claims = [
        Claim("c1", "X doğrudur", "disputed", 500, contradicts="c2"),
        Claim("c2", "X yanlıştır", "disputed", 500, contradicts="c1"),
    ]
    ctx = build_context({"agent_id": "critic-1"}, {"id": "m3"}, claims)
    assert "c1" in ctx["claims"] and "c2" in ctx["claims"]
    assert "c1" in ctx["unresolved"] and "c2" in ctx["unresolved"]
    assert ctx["unresolved_incomplete"] == []


def test_contradiction_incomplete() -> None:
    claims = [
        Claim("c1", "X", "disputed", 500, contradicts="c2", recency=2),
        Claim("c2", "not X", "disputed", 8000, contradicts="c1", recency=1),
    ]
    ctx = build_context({"agent_id": "critic-1"}, {"id": "m4"}, claims)
    assert "c1" in ctx["unresolved"]
    assert "c1" in ctx["unresolved_incomplete"]


def test_rejected_and_superseded_stay_out() -> None:
    claims = [
        Claim("ok", "v", "verified", 100),
        Claim("no", "r", "rejected", 100),
        Claim("old", "s", "superseded", 100),
        Claim("q", "q", "quarantined", 100),
    ]
    ctx = build_context({"agent_id": "a"}, {"id": "m"}, claims)
    assert ctx["claims"] == ["ok"]


def test_skip_over_drops_oversized() -> None:
    claims = [
        Claim("huge", "h", "verified", 9000, recency=2),
        Claim("small", "s", "verified", 500, recency=1),
    ]
    ctx = build_context({"agent_id": "a"}, {"id": "m"}, claims)
    assert ctx["claims"] == ["small"]
    assert ctx["budget_truncated"] is True
    assert ctx["order"][0] == "huge"


def test_append_only_hash_chain() -> None:
    s = Store()
    a = s.append_event("world", "agent.upsert", {"agent_id": "p1", "capability": "producer"})
    b = s.append_event("world", "mission.upsert", {"id": "m1", "objective": "extract", "claim_type": "factual"})
    assert a.prev_hash == "0" * 64
    assert b.prev_hash == a.hash
    assert len(s.events) == 2
    assert s.agents["p1"].updated_from_event == a.id
    assert s.missions["m1"].claim_type == "factual"


def test_lease_exclusive_and_timeout() -> None:
    s = Store()
    s.append_event("world", "agent.upsert", {"agent_id": "p1"})
    s.append_event("world", "agent.upsert", {"agent_id": "p2"})
    s.append_event("world", "mission.upsert", {"id": "m1", "objective": "x", "budget_time_seconds": 1})
    s.acquire_lease("m1", "p1", ttl=1)
    try:
        s.acquire_lease("m1", "p2", ttl=1)
        raise AssertionError("second lease must fail")
    except PermissionError:
        pass
    s.missions["m1"].lease_until = _now() - timedelta(seconds=1)
    n = s.expire_leases()
    assert n == 1
    assert s.missions["m1"].lease_holder is None
    s.acquire_lease("m1", "p2", ttl=60)
    assert s.missions["m1"].lease_holder == "p2"


def test_verified_write_is_gated() -> None:
    s = Store()
    s.append_event("world", "model.upsert", {
        "model_id": "gpt-x", "provider": "openai", "family": "gpt-family", "family_verified": True,
    })
    s.append_event("world", "model.upsert", {
        "model_id": "claude-x", "provider": "anthropic", "family": "claude-family", "family_verified": True,
    })
    try:
        s.append_event("p1", "claim.upsert", {
            "id": "c1", "mission_id": "m1", "statement": "x", "status": "verified",
        })
        raise AssertionError("ungated verified must fail")
    except PermissionError:
        pass
    s.append_event("critic", "claim.upsert", {
        "id": "c1", "mission_id": "m1", "statement": "x", "status": "verified",
        "producer_model": "gpt-x", "critic_model": "claude-x", "source": "obs-1",
    })
    assert s.claims["c1"].status == "verified"


def test_chain_detects_tamper() -> None:
    s = Store()
    s.append_event("world", "agent.upsert", {"agent_id": "p1"})
    assert s.verify_chain() is True
    s.events[0].payload["agent_id"] = "tampered"
    assert s.verify_chain() is False


def test_release_does_not_reopen_verified() -> None:
    s = Store()
    s.append_event("world", "mission.upsert", {
        "id": "m1", "objective": "x", "status": "verified",
    })
    s.missions["m1"].lease_holder = "p1"
    s.missions["m1"].lease_until = _now() - timedelta(seconds=5)
    s.expire_leases()
    assert s.missions["m1"].lease_holder is None
    assert s.missions["m1"].status == "verified"


def test_verified_fail_closed() -> None:
    s = Store()
    s.append_event("world", "model.upsert", {
        "model_id": "gpt-x", "provider": "openai", "family": "gpt-family", "family_verified": False,
    })
    s.append_event("world", "model.upsert", {
        "model_id": "claude-x", "provider": "anthropic", "family": "claude-family", "family_verified": True,
    })
    # unverified family → same-family → cannot write verified
    assert s.can_write_verified("gpt-x", "claude-x") is False
    s.append_event("world", "model.upsert", {
        "model_id": "gpt-x", "provider": "openai", "family": "gpt-family", "family_verified": True,
    })
    assert s.can_write_verified("gpt-x", "claude-x") is True
    assert s.can_write_verified("missing", "claude-x") is False


def main() -> None:
    tests = [
        test_budget_overflow,
        test_quarantine_filter,
        test_contradiction_carry,
        test_contradiction_incomplete,
        test_rejected_and_superseded_stay_out,
        test_skip_over_drops_oversized,
        test_append_only_hash_chain,
        test_lease_exclusive_and_timeout,
        test_verified_write_is_gated,
        test_chain_detects_tamper,
        test_release_does_not_reopen_verified,
        test_verified_fail_closed,
    ]
    for t in tests:
        t()
        print(f"ok  {t.__name__}")
    print(f"{len(tests)}/{len(tests)} geçti. LLM yok. Postgres yok.")


if __name__ == "__main__":
    main()
