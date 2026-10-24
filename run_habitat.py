#!/usr/bin/env python3
"""Habitat v0 — agents coexist, heartbeat, and speak. No mission. No network."""

from __future__ import annotations

import argparse
import os
from pathlib import Path

from store import Store

# Fixed coexistence phrases — not goals, not tasks.
PHRASES: dict[str, list[str]] = {
    "ada": ["Merhaba.", "Güneş var.", "Buradayım.", "Sessizlik güzel.", "Dinliyorum."],
    "bora": ["Selam.", "Rüzgar hafif.", "Ben de buradayım.", "Bir şey duydum.", "Duruyorum."],
    "cem": ["Hey.", "Gölgede duruyorum.", "Burada olmak yeterli.", "Ne varsa o.", "Yine buradayım."],
}

DEFAULT_AGENTS = ("ada", "bora", "cem")
FORBIDDEN_TYPES = frozenset(
    {
        "mission.upsert",
        "lease.acquire",
        "lease.release",
        "claim.upsert",
    }
)


def _ensure_parent(path: str) -> None:
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)


def open_habitat(log_path: str) -> Store:
    """Load durable log if present; otherwise start a new append-only file."""
    _ensure_parent(log_path)
    if os.path.exists(log_path) and os.path.getsize(log_path) > 0:
        return Store.load(log_path)
    return Store(persist_path=log_path)


def spawn_if_needed(store: Store, agent_id: str) -> None:
    existing = store.agents.get(agent_id)
    if existing is not None and existing.status == "active":
        return
    store.append_event(
        actor_id="world",
        typ="agent.spawn",
        payload={"agent_id": agent_id, "capability": "presence", "status": "active"},
        mission_id=None,
    )


def say(store: Store, agent_id: str, text: str, tick: int) -> None:
    store.append_event(
        actor_id=agent_id,
        typ="speech.say",
        payload={"text": text, "channel": "habitat", "tick": tick},
        mission_id=None,
    )


def heartbeat(store: Store, agent_id: str, tick: int) -> None:
    store.append_event(
        actor_id=agent_id,
        typ="agent.heartbeat",
        payload={"agent_id": agent_id, "tick": tick},
        mission_id=None,
    )


def run_habitat(
    ticks: int = 5,
    agents: tuple[str, ...] = DEFAULT_AGENTS,
    log_path: str = "data/habitat_events.jsonl",
    despawn: bool = False,
    speak_every: int = 1,
) -> Store:
    """Run M ticks of coexistence. Always mission_id=None. No lease/claim."""
    store = open_habitat(log_path)
    for agent_id in agents:
        spawn_if_needed(store, agent_id)

    for tick in range(ticks):
        store.append_event(
            actor_id="world",
            typ="world.tick",
            payload={"tick": tick},
            mission_id=None,
        )
        for agent_id in agents:
            heartbeat(store, agent_id, tick)
            if speak_every > 0 and tick % speak_every == 0:
                bank = PHRASES.get(agent_id) or ["..."]
                say(store, agent_id, bank[tick % len(bank)], tick)

    if despawn:
        for agent_id in agents:
            store.append_event(
                actor_id=agent_id,
                typ="agent.despawn",
                payload={"agent_id": agent_id, "status": "idle"},
                mission_id=None,
            )

    bad = [ev for ev in store.events if ev.type in FORBIDDEN_TYPES or ev.mission_id is not None]
    if bad:
        raise RuntimeError(f"habitat violated purpose-free rule: {bad[0].type} mission_id={bad[0].mission_id}")
    if not store.verify_chain():
        raise RuntimeError("habitat chain broken after run")
    return store


def format_transcript(store: Store) -> str:
    lines: list[str] = []
    for ev in store.events:
        mid = ev.mission_id if ev.mission_id is not None else "-"
        if ev.type == "speech.say":
            text = ev.payload.get("text", "")
            lines.append(f"{ev.ts.isoformat()}  {ev.actor_id:8}  say       [{mid}]  {text}")
        elif ev.type == "agent.heartbeat":
            lines.append(f"{ev.ts.isoformat()}  {ev.actor_id:8}  heartbeat [{mid}]  tick={ev.payload.get('tick')}")
        elif ev.type == "world.tick":
            lines.append(f"{ev.ts.isoformat()}  world     tick      [{mid}]  {ev.payload.get('tick')}")
        elif ev.type in ("agent.spawn", "agent.despawn"):
            lines.append(
                f"{ev.ts.isoformat()}  {ev.actor_id:8}  {ev.type:9} [{mid}]  "
                f"{ev.payload.get('agent_id')}"
            )
        else:
            lines.append(f"{ev.ts.isoformat()}  {ev.actor_id:8}  {ev.type:9} [{mid}]")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Agent World Habitat v0 — live, no mission")
    p.add_argument("--ticks", type=int, default=5, help="number of habitat ticks")
    p.add_argument("--agents", default=",".join(DEFAULT_AGENTS), help="comma-separated agent ids")
    p.add_argument("--log", default="data/habitat_events.jsonl", help="durable JSONL path")
    p.add_argument("--despawn", action="store_true", help="despawn agents at end of this run")
    p.add_argument("--speak-every", type=int, default=1, help="speak every N ticks (0=silent)")
    p.add_argument("--quiet", action="store_true", help="suppress transcript print")
    args = p.parse_args(argv)

    agents = tuple(a.strip() for a in args.agents.split(",") if a.strip())
    store = run_habitat(
        ticks=args.ticks,
        agents=agents,
        log_path=args.log,
        despawn=args.despawn,
        speak_every=args.speak_every,
    )
    if not args.quiet:
        print(format_transcript(store))
        print("---")
        print(
            f"events={len(store.events)} agents={sorted(store.agents)} "
            f"chain_ok={store.verify_chain()} log={args.log}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
