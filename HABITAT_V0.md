# Habitat v0 — purpose-free living loop

**Date:** 2026-10-24 (Europe/Istanbul)  
**Kernel tip:** `32a9161` (`habitat-v0` branch under `/workspace/agent-world-restart/kernel`)  
**Vision lock:** agents coexist and speak like people/animals. **Not** a mission pipeline, Ruflo swarm, claim market, or product.

## What this slice is

A thin runner on the Faz 0 event kernel so agents can **exist**, **heartbeat**, and **speak**, with a durable log that survives process restart. Zero product objective.

## Event types (v0)

| Type | `mission_id` | Role |
|---|---|---|
| `agent.spawn` | always `None` | Agent enters the habitat (`status=active`, capability default `presence`). |
| `agent.heartbeat` | always `None` | Presence tick; projection keeps agent `active`. |
| `agent.despawn` | always `None` | Agent leaves; projection sets `idle`. |
| `speech.say` | always `None` | Utterance. Payload: `text`, optional `channel` / `to`. |
| `world.tick` | always `None` | Optional marker for a habitat tick index. |

**Forbidden in this runner:** `mission.upsert`, `lease.acquire` / `lease.release`, `claim.upsert`, any network / LLM client.

`append_event(..., mission_id=None)` is already legal on the kernel; Habitat v0 only uses that path.

## Tick

1. Load durable log (or start empty).
2. Spawn any named agents not yet `active`.
3. For each tick `0 .. M-1`: append `world.tick`, then per agent `agent.heartbeat` and optionally `speech.say`.
4. Optionally despawn at end of the run (demo cleanup; not required for persistence).

Default demo: **3 agents** (`ada`, `bora`, `cem`), **5 ticks**, rule phrases only (no judgment engine required).

## Persistence

- **Path (default):** `data/habitat_events.jsonl` under the kernel cwd (override with `--log`).
- **Format:** append-only JSONL, one event per line (id, ts, actor_id, type, payload, mission_id, parent_event_id, prev_hash, hash).
- **Semantics:** same hash chain as in-memory `Store.verify_chain`. `Store.load(path)` rebuilds projections and **raises** if the chain is broken (fail-closed).
- In-memory mode remains the default when `persist_path` is unset (Faz 0 tests unchanged).

## How to run

```bash
cd /workspace/agent-world-restart/kernel
python3 run_habitat.py                  # 3 agents, 5 ticks → data/habitat_events.jsonl
python3 run_habitat.py --ticks 10 --log /tmp/habitat.jsonl
python3 test_habitat.py                 # habitat suite
python3 test_faz0.py && python3 test_faz1a.py
```

## Out of scope (still)

Groq/Gemini clients, paid APIs, Ruflo-style task swarm, Claim Exchange, web UI, rewriting the Faz 0 constitution.
