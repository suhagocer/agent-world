#!/usr/bin/env python3
"""Habitat v0 tests. No network. No mission required for speech."""

from __future__ import annotations

import os
import tempfile
from pathlib import Path

from run_habitat import FORBIDDEN_TYPES, format_transcript, run_habitat
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
        s1 = run_habitat(ticks=2, agents=("ada", "bora"), log_path=path, despawn=False)
        n1 = len(s1.events)
        tip = s1.events[-1].hash
        assert s1.verify_chain()
        assert any(ev.type == "speech.say" and ev.mission_id is None for ev in s1.events)

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


def test_broken_chain_fail_closed() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "broken.jsonl")
        run_habitat(ticks=1, agents=("ada",), log_path=path)
        with open(path, encoding="utf-8") as f:
            lines = f.read().splitlines()
        # Tamper middle payload without fixing hash
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
        s = run_habitat(ticks=3, agents=("ada", "bora", "cem"), log_path=path, despawn=True)
        types = {ev.type for ev in s.events}
        assert types & FORBIDDEN_TYPES == set()
        assert all(ev.mission_id is None for ev in s.events)
        assert "agent.spawn" in types
        assert "agent.heartbeat" in types
        assert "speech.say" in types
        assert "world.tick" in types
        assert "agent.despawn" in types
        assert s.agents["ada"].status == "idle"
        transcript = format_transcript(s)
        assert "say" in transcript
        assert "[-]" in transcript  # mission column shows dash


def test_no_network_imports_in_habitat() -> None:
    # Product modules only (this test file lists needles and would self-match).
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


def main() -> None:
    tests = [
        test_speech_without_mission,
        test_restart_loads_log,
        test_broken_chain_fail_closed,
        test_run_never_emits_mission_machinery,
        test_no_network_imports_in_habitat,
    ]
    for fn in tests:
        fn()
        print(f"ok  {fn.__name__}")
    print(f"{len(tests)}/{len(tests)} geçti. Habitat. Ağ yok. Görev yok.")


if __name__ == "__main__":
    main()
