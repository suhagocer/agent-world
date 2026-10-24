#!/usr/bin/env python3
"""Habitat v0.2 tests. No network. No mission. Observe/hear/shuffle/notice/density."""

from __future__ import annotations

import os
import tempfile
from pathlib import Path

import random

from run_habitat import (
    FORBIDDEN_TYPES,
    HABITAT_EVENT_TYPES,
    agent_turn,
    format_transcript,
    notice,
    open_habitat,
    run_habitat,
    spawn_if_needed,
)
from store import Store


def test_speech_without_mission() -> None:
    s = Store()
    s.append_event("world", "agent.spawn", {"agent_id": "ada", "capability": "presence"}, mission_id=None)
    ev = s.append_event(
        "ada",
        "speech.say",
        {"text": "Merhaba.", "channel": "habitat"},
        mission_id=None,
    )
    assert ev.mission_id is None
    assert s.agents["ada"].status == "active"
    assert s.verify_chain()
    assert not s.missions
    assert not s.claims


def test_restart_loads_log() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "habitat.jsonl")
        s1 = run_habitat(ticks=2, agents=("ada", "bora"), log_path=path, despawn=False, seed=1)
        n1 = len(s1.events)
        tip = s1.events[-1].hash
        assert s1.verify_chain()
        assert any(ev.type == "speech.say" and ev.mission_id is None for ev in s1.events)
        assert any(ev.type == "agent.observe" for ev in s1.events)
        assert any(ev.type == "speech.hear" for ev in s1.events)

        s2 = Store.load(path)
        assert len(s2.events) == n1
        assert s2.events[-1].hash == tip
        assert s2.verify_chain()
        assert s2.agents["ada"].status == "active"
        assert s2.agents["bora"].status == "active"
        assert not s2.missions

        # Continue world after restart
        s2.append_event("ada", "speech.say", {"text": "Yeniden buradayım."}, mission_id=None)
        assert len(s2.events) == n1 + 1
        assert s2.verify_chain()

        s3 = Store.load(path)
        assert len(s3.events) == n1 + 1
        assert s3.events[-1].payload.get("text") == "Yeniden buradayım."
        assert s3.verify_chain()


def test_persistence_restart_chain_intact() -> None:
    """Write log, reload Store twice, append across restarts — hash chain stays intact."""
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "persist.jsonl")
        s1 = run_habitat(ticks=3, agents=("ada", "bora", "cem"), log_path=path, seed=42)
        tip1 = s1.events[-1].hash
        n1 = len(s1.events)
        assert s1.verify_chain()

        s2 = Store.load(path)
        assert s2.verify_chain()
        assert s2.events[-1].hash == tip1
        assert len(s2.events) == n1

        # Second run appends onto the same durable log
        s3 = run_habitat(ticks=2, agents=("ada", "bora", "cem"), log_path=path, seed=7)
        assert len(s3.events) > n1
        assert s3.verify_chain()
        assert s3.events[n1 - 1].hash == tip1

        s4 = Store.load(path)
        assert len(s4.events) == len(s3.events)
        assert s4.verify_chain()
        assert s4.events[-1].hash == s3.events[-1].hash
        assert not s4.missions
        assert all(ev.mission_id is None for ev in s4.events)


def test_broken_chain_fail_closed() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "broken.jsonl")
        run_habitat(ticks=1, agents=("ada",), log_path=path, seed=0, shuffle=False)
        with open(path, encoding="utf-8") as f:
            lines = f.read().splitlines()
        bad = lines[0].replace('"presence"', '"tampered"')
        with open(path, "w", encoding="utf-8") as f:
            f.write(bad + "\n" + "\n".join(lines[1:]) + "\n")
        try:
            Store.load(path)
            raise AssertionError("tampered log must raise")
        except RuntimeError as e:
            assert "chain broken" in str(e)


def test_run_never_emits_mission_machinery() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "h.jsonl")
        s = run_habitat(ticks=3, agents=("ada", "bora", "cem"), log_path=path, despawn=True, seed=3)
        types = {ev.type for ev in s.events}
        assert types & FORBIDDEN_TYPES == set()
        assert all(ev.mission_id is None for ev in s.events)
        assert types <= HABITAT_EVENT_TYPES
        assert "agent.spawn" in types
        assert "agent.heartbeat" in types
        assert "agent.observe" in types
        assert "speech.say" in types
        assert "speech.hear" in types
        assert "world.tick" in types
        assert "agent.despawn" in types
        assert s.agents["ada"].status == "idle"
        transcript = format_transcript(s)
        assert "say" in transcript
        assert "hear" in transcript
        assert "observe" in transcript
        assert "[-]" in transcript


def test_notice_same_tick_later_hears_earlier() -> None:
    """With fixed order ada→bora→cem, later agents hear earlier speech in the same tick."""
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "notice.jsonl")
        s = run_habitat(
            ticks=1,
            agents=("ada", "bora", "cem"),
            log_path=path,
            seed=0,
            shuffle=False,
            speak_every=1,
        )
        tick0_says = [ev for ev in s.events if ev.type == "speech.say" and ev.payload.get("tick") == 0]
        assert len(tick0_says) == 3
        # bora should hear ada; cem should hear ada and bora
        hears = [ev for ev in s.events if ev.type == "speech.hear" and ev.payload.get("tick") == 0]
        bora_hears = [ev for ev in hears if ev.actor_id == "bora"]
        cem_hears = [ev for ev in hears if ev.actor_id == "cem"]
        ada_hears = [ev for ev in hears if ev.actor_id == "ada"]
        assert ada_hears == []  # first speaker: nothing earlier this tick
        assert {ev.payload["from"] for ev in bora_hears} == {"ada"}
        assert {ev.payload["from"] for ev in cem_hears} == {"ada", "bora"}
        # parent_event_id links hear → say
        say_ids = {ev.id for ev in tick0_says}
        assert all(ev.parent_event_id in say_ids for ev in hears)
        # notice() helper agrees with logged says
        assert len(notice(s, 0)) == 3


def test_tick_shuffle_changes_order() -> None:
    """Different seeds produce different first-speaker patterns across ticks."""
    with tempfile.TemporaryDirectory() as tmp:
        path_a = os.path.join(tmp, "a.jsonl")
        path_b = os.path.join(tmp, "b.jsonl")
        sa = run_habitat(ticks=5, agents=("ada", "bora", "cem"), log_path=path_a, seed=1)
        sb = run_habitat(ticks=5, agents=("ada", "bora", "cem"), log_path=path_b, seed=99)

        def first_speakers(store: Store) -> list[str]:
            out: list[str] = []
            for tick in range(5):
                for ev in store.events:
                    if ev.type == "speech.say" and ev.payload.get("tick") == tick:
                        out.append(ev.actor_id)
                        break
            return out

        assert first_speakers(sa) != first_speakers(sb)


def test_no_network_imports_in_habitat() -> None:
    files = [Path("store.py"), Path("run_habitat.py")]
    forbidden = [
        "import " + "requests",
        "import " + "httpx",
        "urllib" + ".request",
        "import " + "socket",
        "from " + "socket",
        "from " + "urllib",
        "import " + "groq",
        "google" + ".generativeai",
        "import " + "openai",
    ]
    for path in files:
        src = path.read_text(encoding="utf-8")
        for needle in forbidden:
            assert needle not in src, f"{path} contains network needle: {needle}"


def test_density_default_unchanged() -> None:
    """density=1.0 (default) matches explicit density=1.0; no lottery."""
    with tempfile.TemporaryDirectory() as tmp:
        path_a = os.path.join(tmp, "a.jsonl")
        path_b = os.path.join(tmp, "b.jsonl")
        sa = run_habitat(ticks=3, agents=("ada", "bora", "cem"), log_path=path_a, seed=11)
        sb = run_habitat(
            ticks=3, agents=("ada", "bora", "cem"), log_path=path_b, seed=11, density=1.0
        )
        types_a = [ev.type for ev in sa.events]
        types_b = [ev.type for ev in sb.events]
        assert types_a == types_b
        says_a = [ev.payload.get("text") for ev in sa.events if ev.type == "speech.say"]
        says_b = [ev.payload.get("text") for ev in sb.events if ev.type == "speech.say"]
        assert says_a == says_b
        assert len(says_a) == 9  # 3 agents * 3 ticks


def test_density_seeded_reproducible() -> None:
    """Same seed + density < 1 yields identical speech.say pattern."""
    with tempfile.TemporaryDirectory() as tmp:
        path_a = os.path.join(tmp, "a.jsonl")
        path_b = os.path.join(tmp, "b.jsonl")
        sa = run_habitat(
            ticks=8, agents=("ada", "bora", "cem"), log_path=path_a, seed=123, density=0.4
        )
        sb = run_habitat(
            ticks=8, agents=("ada", "bora", "cem"), log_path=path_b, seed=123, density=0.4
        )
        says_a = [
            (ev.actor_id, ev.payload.get("tick"), ev.payload.get("text"))
            for ev in sa.events
            if ev.type == "speech.say"
        ]
        says_b = [
            (ev.actor_id, ev.payload.get("tick"), ev.payload.get("text"))
            for ev in sb.events
            if ev.type == "speech.say"
        ]
        assert says_a == says_b
        assert 0 < len(says_a) < 24  # some speak, not all of 8*3


def test_density_zero_speaks_nothing() -> None:
    """density=0 → no speech.say; heartbeat/observe still written."""
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "z.jsonl")
        s = run_habitat(
            ticks=4, agents=("ada", "bora"), log_path=path, seed=0, density=0.0, shuffle=False
        )
        assert not any(ev.type == "speech.say" for ev in s.events)
        assert not any(ev.type == "speech.hear" for ev in s.events)
        assert any(ev.type == "agent.heartbeat" for ev in s.events)
        assert any(ev.type == "agent.observe" for ev in s.events)
        assert all(ev.mission_id is None for ev in s.events)


def test_density_requires_rng_fail_closed() -> None:
    """density < 1.0 without rng → ValueError."""
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "r.jsonl")
        store = open_habitat(path)
        spawn_if_needed(store, "ada")
        try:
            agent_turn(store, "ada", tick=0, speak_every=1, density=0.5, rng=None)
            raise AssertionError("must require rng when density < 1")
        except ValueError as e:
            assert "rng" in str(e).lower()


def test_density_does_not_force_hear() -> None:
    """Hearing earlier speech does not force a speech.say when density draw fails."""
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "h.jsonl")
        store = open_habitat(path)
        spawn_if_needed(store, "ada")
        spawn_if_needed(store, "bora")
        store.append_event(
            actor_id="world",
            typ="world.tick",
            payload={"tick": 0},
            mission_id=None,
        )
        agent_turn(store, "ada", tick=0, speak_every=1, density=1.0)
        assert any(ev.type == "speech.say" and ev.actor_id == "ada" for ev in store.events)
        rng = random.Random(0)
        agent_turn(store, "bora", tick=0, speak_every=1, density=0.0, rng=rng)
        bora_hears = [
            ev for ev in store.events if ev.type == "speech.hear" and ev.actor_id == "bora"
        ]
        bora_says = [
            ev for ev in store.events if ev.type == "speech.say" and ev.actor_id == "bora"
        ]
        assert len(bora_hears) == 1
        assert bora_hears[0].payload.get("from") == "ada"
        assert bora_says == []
        assert any(
            ev.type == "agent.observe" and ev.actor_id == "bora" for ev in store.events
        )


def test_density_out_of_range_rejected() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "o.jsonl")
        for bad in (-0.1, 1.1, 2.0, -1.0):
            try:
                run_habitat(ticks=1, agents=("ada",), log_path=path, seed=0, density=bad)
                raise AssertionError(f"density={bad} must raise")
            except ValueError as e:
                assert "density" in str(e).lower()



def main() -> None:
    tests = [
        test_speech_without_mission,
        test_restart_loads_log,
        test_persistence_restart_chain_intact,
        test_broken_chain_fail_closed,
        test_run_never_emits_mission_machinery,
        test_notice_same_tick_later_hears_earlier,
        test_tick_shuffle_changes_order,
        test_no_network_imports_in_habitat,
        test_density_default_unchanged,
        test_density_seeded_reproducible,
        test_density_zero_speaks_nothing,
        test_density_requires_rng_fail_closed,
        test_density_does_not_force_hear,
        test_density_out_of_range_rejected,
    ]
    for fn in tests:
        fn()
        print(f"ok  {fn.__name__}")
    print(f"{len(tests)}/{len(tests)} geçti. Habitat v0.2. Ağ yok. Görev yok.")


if __name__ == "__main__":
    main()
