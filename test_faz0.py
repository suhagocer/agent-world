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
    s.append_event("p1", "claim.upsert", {
        "id": "c1", "mission_id": "m1", "statement": "x", "status": "verified",
        "_attested": True,
    })
    assert s.claims["c1"].status == "unverified"
    s.append_event("critic", "claim.upsert", {
        "id": "c2", "mission_id": "m1", "statement": "x", "status": "verified",
        "producer_model": "gpt-x", "critic_model": "claude-x", "source": "obs-1",
    })
    assert s.claims["c2"].status == "verified"


def test_verify_claim_requires_source() -> None:
    s = Store()
    s.append_event("world", "mission.upsert", {"id": "m1", "objective": "x"})
    s.append_event("p1", "claim.upsert", {"id": "c1", "mission_id": "m1", "statement": "X"})
    try:
        s.verify_claim("c1", "gpt-x", "claude-x", source="")
        raise AssertionError("must require source")
    except ValueError:
        pass


def test_evaluate_verification_three_tier() -> None:
    s = Store()
    s.append_event("world", "model.upsert", {
        "model_id": "gpt-4o", "provider": "openai", "family": "gpt-family", "family_verified": True,
    })
    s.append_event("world", "model.upsert", {
        "model_id": "gpt-4o-mini", "provider": "openai", "family": "gpt-family", "family_verified": True,
    })
    s.append_event("world", "model.upsert", {
        "model_id": "claude-x", "provider": "anthropic", "family": "claude-family", "family_verified": True,
    })
    s.append_event("world", "model.upsert", {
        "model_id": "gpt-unv", "provider": "openai", "family": "gpt-family", "family_verified": False,
    })
    assert s.evaluate_verification("gpt-4o", "gpt-4o") == "unverified"
    assert s.evaluate_verification("gpt-4o", "gpt-4o-mini") == "verified-weak"
    assert s.evaluate_verification("gpt-4o", "claude-x") == "verified"
    assert s.evaluate_verification("gpt-unv", "claude-x") == "unverified"


def test_hash_covers_mission_id() -> None:
    s = Store()
    e1 = s.append_event("world", "agent.upsert", {"agent_id": "p1"}, mission_id="m1")
    s2 = Store()
    e2 = s2.append_event("world", "agent.upsert", {"agent_id": "p1"}, mission_id="m2")
    assert e1.hash != e2.hash


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



def test_skip_over_keeps_small_after_sort() -> None:
    claims = [
        Claim("big", "b", "unverified", 7000, recency=1),
        Claim("small", "s", "verified", 500, recency=0),
    ]
    ctx = build_context({"agent_id": "a"}, {"id": "m"}, claims)
    assert ctx["claims"][0] == "small"
    assert set(ctx["claims"]) == {"small", "big"}


def test_claim_upsert_cannot_self_declare_verified() -> None:
    s = Store()
    s.append_event("world", "mission.upsert", {"id": "m1", "objective": "x"})
    s.append_event("producer-1", "claim.upsert", {
        "id": "c1", "mission_id": "m1", "statement": "X is true", "status": "verified",
    })
    assert s.claims["c1"].status == "unverified"


def test_verify_claim_recomputes_status_end_to_end() -> None:
    s = Store()
    s.append_event("world", "model.upsert", {
        "model_id": "gpt-4o", "provider": "openai",
        "family": "gpt-family", "family_verified": True,
    })
    s.append_event("world", "model.upsert", {
        "model_id": "claude-x", "provider": "anthropic",
        "family": "claude-family", "family_verified": True,
    })
    s.append_event("world", "mission.upsert", {"id": "m1", "objective": "x"})
    s.append_event("producer-1", "claim.upsert", {
        "id": "c1", "mission_id": "m1", "statement": "X",
    })
    s.verify_claim("c1", producer_model="gpt-4o",
                   critic_model="claude-x", source="doc.pdf#p3")
    assert s.claims["c1"].status == "verified"
    assert s.claims["c1"].source == "doc.pdf#p3"


def test_hash_covers_parent_event_id() -> None:
    s1 = Store()
    e1 = s1.append_event("world", "agent.upsert", {"agent_id": "p1"},
                          mission_id="m1", parent_event_id="parent-A")
    s2 = Store()
    e2 = s2.append_event("world", "agent.upsert", {"agent_id": "p1"},
                          mission_id="m1", parent_event_id="parent-B")
    assert e1.hash != e2.hash


def test_can_write_verified_excludes_same_family_weak_case() -> None:
    s = Store()
    s.append_event("world", "model.upsert", {
        "model_id": "gpt-4o", "provider": "openai",
        "family": "gpt-family", "family_verified": True,
    })
    s.append_event("world", "model.upsert", {
        "model_id": "gpt-4o-mini", "provider": "openai",
        "family": "gpt-family", "family_verified": True,
    })
    s.append_event("world", "model.upsert", {
        "model_id": "claude-x", "provider": "anthropic",
        "family": "claude-family", "family_verified": True,
    })
    assert s.evaluate_verification("gpt-4o", "gpt-4o-mini") == "verified-weak"
    assert s.can_write_verified("gpt-4o", "gpt-4o-mini") is False
    assert s.evaluate_verification("gpt-4o", "claude-x") == "verified"
    assert s.can_write_verified("gpt-4o", "claude-x") is True


def test_unspecified_family_verified_defaults_fail_closed() -> None:
    s = Store()
    s.append_event("world", "model.upsert", {
        "model_id": "mystery-model", "provider": "unknown",
        "family": "mystery-family",
    })
    assert s.models["mystery-model"].family_verified is False
    s.append_event("world", "model.upsert", {
        "model_id": "claude-x", "provider": "anthropic",
        "family": "claude-family", "family_verified": True,
    })
    assert s.evaluate_verification("mystery-model", "claude-x") == "unverified"


def test_lease_operations_are_event_logged() -> None:
    s = Store()
    s.append_event("world", "agent.upsert", {"agent_id": "p1"})
    s.append_event("world", "mission.upsert", {"id": "m1", "objective": "x"})
    n_before = len(s.events)
    s.acquire_lease("m1", "p1", ttl=1)
    assert len(s.events) == n_before + 1
    assert s.events[-1].type == "lease.acquire"
    assert s.events[-1].mission_id == "m1"
    s.missions["m1"].lease_until = _now() - timedelta(seconds=1)
    expired = s.expire_leases()
    assert expired == 1
    assert s.events[-1].type == "lease.release"
    assert s.events[-1].actor_id == "world"


def test_single_write_path_no_direct_setters() -> None:
    s = Store()
    public_methods = {
        name for name in dir(s)
        if not name.startswith("_") and callable(getattr(s, name))
    }
    forbidden = {
        "add_agent", "add_mission", "add_claim", "add_model",
        "set_agent", "set_mission", "set_claim", "set_model",
        "update_agent", "update_mission", "update_claim",
    }
    assert public_methods.isdisjoint(forbidden)
    assert "append_event" in public_methods


def test_world_agent_model_are_distinct_types() -> None:
    from store import Agent, Model
    agent_fields = set(Agent.__dataclass_fields__)
    model_fields = set(Model.__dataclass_fields__)
    assert "family" not in agent_fields
    assert "reputation" not in model_fields
    assert agent_fields != model_fields

def main() -> None:
    tests = [
        test_skip_over_keeps_small_after_sort,
        test_claim_upsert_cannot_self_declare_verified,
        test_verify_claim_recomputes_status_end_to_end,
        test_hash_covers_parent_event_id,
        test_can_write_verified_excludes_same_family_weak_case,
        test_unspecified_family_verified_defaults_fail_closed,
        test_lease_operations_are_event_logged,
        test_single_write_path_no_direct_setters,
        test_world_agent_model_are_distinct_types,
        test_budget_overflow,
        test_quarantine_filter,
        test_contradiction_carry,
        test_contradiction_incomplete,
        test_rejected_and_superseded_stay_out,
        test_skip_over_drops_oversized,
        test_append_only_hash_chain,
        test_lease_exclusive_and_timeout,
        test_verified_write_is_gated,
        test_verify_claim_requires_source,
        test_evaluate_verification_three_tier,
        test_hash_covers_mission_id,
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
