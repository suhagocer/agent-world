# Habitat v0.2 — seeded speech density

**Date:** 2026-10-25 (Europe/Istanbul)  
**Base:** main `4698ef3` (v0.1 contract) / code `7bad21b`  
**Branch:** `habitat-v0.2`  
**Vision lock:** purpose-free living world. **Not** a mission pipeline, Ruflo swarm, claim market, or product.

## What changed from v0.1

| Slice | Behavior |
|---|---|
| `density` | Parameter on `agent_turn` / `run_habitat` (default `1.0`). |
| `density == 1.0` | Current v0.1 behavior — **no lottery**. Existing tests stay green. |
| `density < 1.0` | Requires `rng` (`random.Random`). Missing rng → `ValueError` (fail-closed). |
| Draw | Once per agent **after** tick shuffle. Fail → no `speech.say`; still heartbeat / observe / hear. |
| Hear | Does **not** force speech. |
| Range | `density` outside `[0, 1]` → `ValueError`. |
| CLI | `--density FLOAT` default `1.0`; `--density < 1` without `--seed` → error. |
| Library | `run_habitat(density<1, seed=None)` → `ValueError` (same fail-closed as CLI). `density==1.0` still allows `seed=None`. |

Runner name stays `run_habitat.py`. `mission_id` always `None`.

## Tick (v0.2)

1. Load durable log (or start empty).
2. Spawn named agents not yet `active`.
3. For each tick: append `world.tick`, **shuffle** agent order, then per agent:
   - `agent.heartbeat`
   - `notice()` → `agent.observe` + `speech.hear` for earlier same-tick speech
   - optional `speech.say` gated by `speak_every` and density lottery
4. Optional despawn at end.

## How to run

```bash
python3 run_habitat.py
python3 run_habitat.py --ticks 10 --seed 42 --density 0.4 --log /tmp/habitat.jsonl
python3 test_habitat.py
python3 test_faz0.py && python3 test_faz1a.py
```

## Out of scope (still)

Groq/Gemini clients, paid APIs, Ruflo-style task swarm, Claim Exchange, web UI, rewriting the Faz 0 constitution.
