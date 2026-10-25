#!/usr/bin/env python3
"""Habitat v0.2 — agents coexist, notice, hear, speak; seeded density; tick continuity. No mission. No network."""

from __future__ import annotations

import argparse
import os
import random
from pathlib import Path

from store import Event, Store

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
HABITAT_EVENT_TYPES = frozenset(
    {
        "agent.spawn",
        "agent.heartbeat",
        "agent.despawn",
        "agent.observe",
        "speech.say",
        "speech.hear",
        "world.tick",
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

def _is_tick_int(value: object) -> bool:
    """True for real ints only. bool is a subclass of int in Python — reject it."""
    return isinstance(value, int) and not isinstance(value, bool)


def next_start_tick(store: Store) -> int:
    """One past the max world.tick payload that is an int (not bool). Empty → 0.

    Uses max, not the last event, so a legacy rewound log (…2, then 1…)
    still continues from 3 rather than from 2.
    """
    best: int | None = None
    for ev in store.events:
        if ev.type != "world.tick":
            continue
        t = ev.payload.get("tick")
        if not _is_tick_int(t):
            continue
        if best is None or t > best:
            best = t
    return 0 if best is None else best + 1


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


def say(store: Store, agent_id: str, text: str, tick: int) -> Event:
    return store.append_event(
        actor_id=agent_id,
        typ="speech.say",
        payload={"text": text, "channel": "habitat", "tick": tick},
        mission_id=None,
    )


def heartbeat(store: Store, agent_id: str, tick: int) -> Event:
    return store.append_event(
        actor_id=agent_id,
        typ="agent.heartbeat",
        payload={"agent_id": agent_id, "tick": tick},
        mission_id=None,
    )


def notice(store: Store, tick: int, window: int = 50) -> list[Event]:
    """speech.say in the last `window` events. Does not write. Default window=50.

    `tick` is kept so `notice(store, tick)` stays valid; filtering is by window, not same-tick.
    """
    _ = tick
    recent = store.events[-window:] if window > 0 else []
    return [ev for ev in recent if ev.type == "speech.say"]


def observe(store: Store, agent_id: str, tick: int, noticed: list[Event]) -> Event:
    speakers = [ev.actor_id for ev in noticed if ev.actor_id != agent_id]
    return store.append_event(
        actor_id=agent_id,
        typ="agent.observe",
        payload={
            "agent_id": agent_id,
            "tick": tick,
            "heard_count": len(speakers),
            "speakers": speakers,
        },
        mission_id=None,
    )


def hear(store: Store, agent_id: str, say_ev: Event, tick: int) -> Event:
    return store.append_event(
        actor_id=agent_id,
        typ="speech.hear",
        payload={
            "text": say_ev.payload.get("text", ""),
            "from": say_ev.actor_id,
            "tick": tick,
            "channel": say_ev.payload.get("channel", "habitat"),
        },
        mission_id=None,
        parent_event_id=say_ev.id,
    )


def _validate_density(density: float) -> None:
    if not (0.0 <= density <= 1.0):
        raise ValueError(f"density must be in [0, 1], got {density!r}")


def agent_turn(
    store: Store,
    agent_id: str,
    tick: int,
    speak_every: int,
    density: float = 1.0,
    rng: random.Random | None = None,
    window: int = 50,
) -> None:
    _validate_density(density)
    if density < 1.0 and rng is None:
        raise ValueError("density < 1.0 requires rng (Random)")

    heartbeat(store, agent_id, tick)
    noticed = notice(store, tick, window=window)
    already_heard = {
        ev.parent_event_id
        for ev in store.events
        if ev.type == "speech.hear"
        and ev.actor_id == agent_id
        and ev.parent_event_id is not None
    }
    to_hear = [
        ev
        for ev in noticed
        if ev.actor_id != agent_id and ev.id not in already_heard
    ]
    observe(store, agent_id, tick, to_hear)
    for say_ev in to_hear:
        hear(store, agent_id, say_ev, tick)
    if speak_every > 0 and tick % speak_every == 0:
        # density==1.0: no lottery (v0.1 behavior). density<1: one draw after shuffle.
        if density < 1.0 and rng.random() >= density:
            return
        bank = PHRASES.get(agent_id) or ["..."]
        say(store, agent_id, bank[tick % len(bank)], tick)


def run_habitat(
    ticks: int = 5,
    agents: tuple[str, ...] = DEFAULT_AGENTS,
    log_path: str = "data/habitat_events.jsonl",
    despawn: bool = False,
    speak_every: int = 1,
    seed: int | None = None,
    shuffle: bool = True,
    density: float = 1.0,
    window: int = 50,
) -> Store:
    """Run M ticks of coexistence. Always mission_id=None. No lease/claim."""
    _validate_density(density)
    if density < 1.0 and seed is None:
        raise ValueError("density < 1.0 requires seed (reproducibility)")
    store = open_habitat(log_path)
    for agent_id in agents:
        spawn_if_needed(store, agent_id)

    rng = random.Random(seed)
    start = next_start_tick(store)
    for tick in range(start, start + ticks):
        store.append_event(
            actor_id="world",
            typ="world.tick",
            payload={"tick": tick},
            mission_id=None,
        )
        order = list(agents)
        if shuffle:
            rng.shuffle(order)
        for agent_id in order:
            agent_turn(
                store, agent_id, tick, speak_every, density=density, rng=rng, window=window
            )

    if despawn:
        for agent_id in agents:
            store.append_event(
                actor_id=agent_id,
                typ="agent.despawn",
                payload={"agent_id": agent_id, "status": "idle"},
                mission_id=None,
            )

    bad = [
        ev
        for ev in store.events
        if ev.type in FORBIDDEN_TYPES or ev.mission_id is not None
    ]
    if bad:
        raise RuntimeError(
            f"habitat violated purpose-free rule: {bad[0].type} mission_id={bad[0].mission_id}"
        )
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
        elif ev.type == "speech.hear":
            lines.append(
                f"{ev.ts.isoformat()}  {ev.actor_id:8}  hear      [{mid}]  "
                f"from={ev.payload.get('from')} {ev.payload.get('text', '')}"
            )
        elif ev.type == "agent.observe":
            lines.append(
                f"{ev.ts.isoformat()}  {ev.actor_id:8}  observe   [{mid}]  "
                f"heard={ev.payload.get('heard_count')} speakers={ev.payload.get('speakers')}"
            )
        elif ev.type == "agent.heartbeat":
            lines.append(
                f"{ev.ts.isoformat()}  {ev.actor_id:8}  heartbeat [{mid}]  tick={ev.payload.get('tick')}"
            )
        elif ev.type == "world.tick":
            lines.append(
                f"{ev.ts.isoformat()}  world     tick      [{mid}]  {ev.payload.get('tick')}"
            )
        elif ev.type in ("agent.spawn", "agent.despawn"):
            lines.append(
                f"{ev.ts.isoformat()}  {ev.actor_id:8}  {ev.type:9} [{mid}]  "
                f"{ev.payload.get('agent_id')}"
            )
        else:
            lines.append(f"{ev.ts.isoformat()}  {ev.actor_id:8}  {ev.type:9} [{mid}]")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Agent World Habitat v0.2 — live, notice, seeded density, no mission")
    p.add_argument("--ticks", type=int, default=5, help="number of habitat ticks")
    p.add_argument("--agents", default=",".join(DEFAULT_AGENTS), help="comma-separated agent ids")
    p.add_argument("--log", default="data/habitat_events.jsonl", help="durable JSONL path")
    p.add_argument("--despawn", action="store_true", help="despawn agents at end of this run")
    p.add_argument("--speak-every", type=int, default=1, help="speak every N ticks (0=silent)")
    p.add_argument("--seed", type=int, default=None, help="RNG seed for tick shuffle and density lottery")
    p.add_argument("--density", type=float, default=1.0, help="speech density in [0,1]; 1.0 = always (no lottery)")
    p.add_argument("--no-shuffle", action="store_true", help="keep agent order fixed (debug)")
    p.add_argument("--quiet", action="store_true", help="suppress transcript print")
    args = p.parse_args(argv)

    if args.density < 1.0 and args.seed is None:
        p.error("--density < 1 requires --seed")
    try:
        _validate_density(args.density)
    except ValueError as e:
        p.error(str(e))

    agents = tuple(a.strip() for a in args.agents.split(",") if a.strip())
    store = run_habitat(
        ticks=args.ticks,
        agents=agents,
        log_path=args.log,
        despawn=args.despawn,
        speak_every=args.speak_every,
        seed=args.seed,
        shuffle=not args.no_shuffle,
        density=args.density,
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
