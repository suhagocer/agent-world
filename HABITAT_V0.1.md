# Habitat v0.1 — purpose-free living loop

**Date:** 2026-10-24 (Europe/Istanbul)  
**Base:** main `5308e19` (Habitat v0)  
**Branch:** `habitat-v0.1`  
**Vision lock:** agents coexist and speak like people/animals. **Not** a mission pipeline, Ruflo swarm, claim market, or product.

## What changed from v0

| Slice | Behavior |
|---|---|
| `agent.observe` | Each agent turn logs what they notice this tick (heard_count, speakers). |
| `speech.hear` | Later agents in the same tick hear earlier `speech.say` (`parent_event_id` → say). |
| `notice()` | Helper: same-tick `speech.say` already on the log (Grok/Claude same-tick visibility). |
| Tick shuffle | Agent order randomized each tick (`--seed` for repro; `--no-shuffle` for debug). |
| Persistence demo | Tests write JSONL, `Store.load`, continue run — hash chain intact. |

## Event types (v0.1)

| Type | `mission_id` | Role |
|---|---|---|
| `agent.spawn` | always `None` | Agent enters (`status=active`, capability `presence`). |
| `agent.heartbeat` | always `None` | Presence tick. |
| `agent.despawn` | always `None` | Agent leaves; projection `idle`. |
| `agent.observe` | always `None` | Perception snapshot for this tick. |
| `speech.say` | always `None` | Utterance (`text`, `channel`, `tick`). |
| `speech.hear` | always `None` | Heard utterance; `parent_event_id` links to say. |
| `world.tick` | always `None` | Tick marker. |

**Forbidden:** `mission.upsert`, `lease.*`, `claim.upsert`, any network / LLM client.

## Tick (v0.1)

1. Load durable log (or start empty).
2. Spawn named agents not yet `active`.
3. For each tick: append `world.tick`, **shuffle** agent order, then per agent:
   - `agent.heartbeat`
   - `notice()` → `agent.observe` + `speech.hear` for earlier same-tick speech
   - optional `speech.say`
4. Optional despawn at end.

Default demo: **3 agents** (`ada`, `bora`, `cem`), **5 ticks**, rule phrases only.

## Persistence

- **Path (default):** `data/habitat_events.jsonl`
- **Format:** append-only JSONL with hash chain
- **Semantics:** `Store.load(path)` rebuilds projections; **raises** if chain broken

## How to run

```bash
cd kernel   # or repo root if files live at root
python3 run_habitat.py
python3 run_habitat.py --ticks 10 --seed 42 --log /tmp/habitat.jsonl
python3 run_habitat.py --no-shuffle   # fixed order (debug / notice tests)
python3 test_habitat.py
python3 test_faz0.py && python3 test_faz1a.py
```

## Out of scope (still)

Groq/Gemini clients, paid APIs, Ruflo-style task swarm, Claim Exchange, web UI, rewriting the Faz 0 constitution.
