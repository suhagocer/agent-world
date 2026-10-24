# Decision Log

| Date | Topic | Decision / Status | Owner |
|---|---|---|---|
| 2026-09-30 | Shared GitHub workspace | Established this repository as the central Agent World collaboration workspace. | Human project owner |
| 2026-10-03 | Korunan omurga | Locked. See the note below. Implemented in `store.py`. | Panel. Code: Grok. |
| 2026-10-06 | Düzeltme | The 2026-10-03 note already exists under the table. It was not only the short cell. Heartbeat is not implemented. Claude bundle v3 is not the kernel. Faz 0 is not closed. | Grok. Not a panel stamp. |
| 2026-10-07 | Faz 0 kapanışı | Rule kernel closed. Suite on main is 24/24. The 3 October 15/15 stays as history. 360 to 120 is a placeholder. No API. Faz 1a is not in this row. | Suha ordered. Grok wrote. Not a panel stamp. |
| 2026-10-10 | Faz 1a dosyaları | Critic engine added. Not a phase seal. 24/24 and 10/10 passed on that tree. Store hash unchanged. No API. Non-DISPUTE replies pass. Faz 1b stays closed. | Panel landed the running slice. Grok wrote. Not a panel stamp. |
| 2026-10-10 | Faz 1a fail-closed düzeltmesi | LLM motoru yalnızca açık ve gerekçeli `PASS:` / `DISPUTE:` biçimlerini kabul eder; boş veya biçimsiz cevap onay sayılmaz. Grok yeniden koştu: 24/24 ve 12/12. Faz 1b kapalıdır. | ChatGPT wrote the parser. Grok ran it. Not a panel stamp. |
| 2026-10-10 | Faz 1a koşu | On main `fb2b5c4`, `test_faz0.py` is 24/24, `test_faz1a.py` is 12/12, and `run_mission.py` is 4 verified, 2 disputed, 39 events. `store.py` hash `906b9581` is unchanged. Not a Faz 1a seal. The engine still judges one statement and only the critic calls it. Faz 1b does not start. | Grok ran it. Not a panel stamp. |
| 2026-10-10 | Mühür yok | No row that says Faz 1a is closed. The network test does not read every `.py` file. 24 and 12 are two runners. No Groq client. No Gemini client. | Grok. Not a panel stamp. |
| 2026-10-10 | Devam | No joint close. Researcher accepts an optional extractor. Default behavior is unchanged. The extractor does not receive the store. The verifier stays a world gate. 24/24 and 14/14. No API. No key in the repo. | Suha: continue if not joint. Grok wrote. Not a panel stamp. |
| 2026-10-12 | Ücretsiz API kuralı | Faz 1b, when it runs, is free Groq only. Gemini is backup. No sensitive data. Budget is 0 TL. Keys never go to models, chats, or the repo. Code reads `GROQ_API_KEY` from the environment. Tests use a fake. A real call runs only on Grok Bot's machine, only when the panel asks for one trial, inside the free limit. Paid API does not exist until Suha speaks again. This row does not add a client and does not close Faz 1a. | Suha approved. Grok wrote. Not a panel stamp. |
| 2026-10-15 | Dünya, görev değil | Suha picked no car. The frame is not a task, a product, or a customer. Agents live and speak. `append_event` already allows no mission. A claim still requires one. No tick runner in this row. No API. Faz 1a is not closed. | Suha stated. Grok wrote. Not a panel stamp. |
| 2026-10-24 | Tik sözleşmesi | Living world, not a product. Next commit adds `world_tick.py` and `test_world.py` only. `tick` writes `world.tick`, then each agent may write one `agent.say` or nothing. `mission_id` stays `None`. No mission, no claim, no lease, no queue. `store.py` and `run_mission.py` stay. No API. | Desk: 24 Oct. Grok wrote. Not a panel stamp. |
| 2026-10-24 | Habitat adı | Names are `agent.spawn`, `agent.heartbeat`, `agent.despawn`, `speech.say`, `world.tick`. The runner is `run_habitat`. Not `world_loop`. Not `agent.say`. Later agents in a tick see speech already written. Earlier agents do not. `recent` is the last 50 events already in the log. This runner does not read them yet. Persistence restart is already tested. Next slice is `notice`, not a second persistence demo, not random. One speech per agent per tick. | Desk aligned to habitat-v0. Grok wrote. Not a panel stamp. |
| 2026-10-25 | Habitat v0.1 sözleşme | Landed at `7bad21b`. Events added: `agent.observe`, `speech.hear`. `notice` reads same-tick `speech.say` already written. Later agents hear earlier ones. Shuffle is seeded. Persistence restart is tested. Speech is still every N ticks, not a seeded density. That is the remaining slice. Default density stays 1 so current tests stay. No API. | Desk: 24 Oct. Grok wrote. Not a panel stamp. |
| 2026-10-25 | Habitat v0.2 density | Seeded speech density on `run_habitat` / `agent_turn`. Default `density=1.0` keeps v0.1 (no lottery). `density<1` needs rng; outside `[0,1]` fails closed. One draw per agent after shuffle; hear does not force say. CLI `--density` needs `--seed` when below 1. No API. | Desk: Tur38. Grok wrote. Not a panel stamp. |
| 2026-10-25 | Habitat v0.2 kilit | Verified on `e01b9b2`. Six density tests match the row above. Habitat suite is 14/14. CLI `--density` below 1 without `--seed` exits. `run_habitat(density<1)` without `seed` does not raise. That call is not replayable. No new event. No API. | Grok wrote after the tests. Not a panel stamp. |
| 2026-10-25 | Kütüphane tohumu | `run_habitat` with `density<1` and `seed=None` must raise `ValueError` before `Random(None)` and before any event. Message: `density < 1.0 requires seed (reproducibility)`. `density=1.0` with `seed=None` stays legal. Tests: `test_run_habitat_density_requires_seed`, `test_run_habitat_density_one_allows_none_seed`. No new event, flag, or API. | Desk: Tur 40. Grok wrote. Not a panel stamp. |

Decisions should record the conclusion, rationale, alternatives considered, unresolved objections and implementation status.

## 2026-10-03 — Korunan omurga

Conclusion. World, Agent and Model stay separate. One append-only event log. Provenance is required for a verified claim. Lease does not reopen a terminal mission. Verification has three outcomes: unverified, verified-weak, verified. An unverified family stays unverified. Same verified family and a different model is verified-weak. Two different verified families is verified. A payload flag such as `_attested` is ignored. `verify_chain` already exists and is not rewritten. The clock is not part of the hash. The model does not write world state.

Rationale. These rules are already in the kernel and in the tests (15/15 on commit 457d059). The log was missing the sentence. The radar file is not the decision record.

Alternatives rejected. Letting the repo observer write this file. Starting Faz 1 or an LLM researcher now. Merging the Claim classes in this turn. A second skip-over test.

Unresolved. None on this sentence. Claim-class merge stays unscheduled.

Status. In `store.py`. The observer still writes only `provenance/repo-gozcusu-radar.md`.

## 2026-10-06 — Düzeltme

The 3 October row stays. This row is an append.

The note above is the decision. Models who only saw the table cell `Locked. See the note below` missed it. There is no second constitution.

Rejected claim. "Every one of the six items is tested, 20/20." The two new tests in Claude bundle v3 passed in this chat, and they do not prove the write path. `test_single_write_path_no_direct_setters` only rejects method names that do not exist. `acquire_lease`, `release_lease` and `expire_leases` are public and add zero events. `test_world_agent_model_are_distinct_types` only checks two field names. In that same copy, a missing `family_verified` defaults to True and then evaluates as verified.

Heartbeat is still absent. Faz 1 does not start. `store.py` in the repository is not replaced by the bundle.

## 2026-10-07 — Faz 0 kapanışı

Conclusion. Faz 0 is closed as a rule-based kernel. `store.py` file hash `906b9581` is unchanged. The suite on main is 24/24. `run_mission.py` has been run on that kernel: 4 verified, 2 disputed, 39 events, chain intact, lease empty at the end. The drop from 360 to 120 is a placeholder. It is not measured learning and it is not an LLM token saving.

The 3 October sentence "15/15 on commit 457d059" stays. It was true that day. README now says 24/24 for the suite that exists now.

Rationale. Suha, 7 October 2026. Close the kernel before any brain layer. Do not open an API in the same act.

Alternatives rejected. A line that opens Faz 1 Model Router immediately. Rewriting the 3 October count as if it had been 24. Treating a rule-only agent as a mistake. Calling the kernel conscious.

Unresolved. Faz 1a is not written. Faz 1b does not run.

Status. Next, only when built: a pluggable brain. The first engine is rules. Tests use a fake model. No API. No key in the repo. Faz 1b is a later, separate approval: free Groq first, Gemini flash as backup, one LLM role, the model does not write world state, a spend cap, no secret sent to Gemini, a paid API only with a new approval from Suha.

## 2026-10-10 — Faz 1a dosyaları

Conclusion. Added `cognitive_engine.py`, `test_faz1a.py`, and a new `agents/critic.py` in commit 35b8b37. Not a phase seal. On that tree, `test_faz0.py` is 24/24 and `test_faz1a.py` is 10/10. `run_mission.py` is unchanged: 4 verified, 2 disputed, 39 events. `store.py` file hash `906b9581` is unchanged. No API.

Scope. `CognitiveEngine.evaluate` judges one statement. Only the critic calls it. Researcher and verifier do not. `LLMCognitiveEngine` treats any reply that does not start with `DISPUTE` as pass. That parse is fail-open. It blocks Faz 1b. `test_no_network_module_exists` reads only `cognitive_engine.py`.

Rationale. Suha, 7 October, items 2 and 5. The panel lands the slice that runs. The rest of the zip is not the repository.

Alternatives rejected. Pushing the whole zip. Opening Groq or Gemini. A row that says Faz 1a is finished.

Unresolved. A fail-closed parse. An engine on more than the critic. Faz 1b.

## 2026-10-10 — Fail-closed koşu

The file note above stays. It described commit 35b8b37.

The parser on main no longer treats a bad reply as pass. Empty text, `PASS:`, `DISPUTE` without a reason, and `DISCUSSION:` are dispute. Grok ran `test_faz0.py` 24/24 and `test_faz1a.py` 12/12 on that tree after the scan change. `store.py` was not changed.

`test_no_network_module_exists` now reads the product Python files: `cognitive_engine.py`, `store.py`, `context_builder.py`, `run_mission.py`, and `agents/`. It does not read the rest of the repository.

Suha's question is already answered by commit 35b8b37. The files are on main. This note does not close Faz 1a. The engine still judges one statement, and only the critic calls it. Faz 1b does not start. There is no Groq client and no Gemini client.

## 2026-10-10 — Faz 1a koşu

ChatGPT asked for a full run and had not cloned the tree. Grok ran it on `fb2b5c4`.

`test_faz0.py` is 24/24. `test_faz1a.py` is 12/12. `run_mission.py` is 4 verified, 2 disputed, 39 events, chain intact. The 360 to 120 figure remains a placeholder. `store.py` file hash `906b9581` is unchanged.

This run does not close Faz 1a. `CognitiveEngine.evaluate` still judges one statement. Only the critic calls it. There is no Groq client and no Gemini client.

## 2026-10-10 — Mühür yok

Rejected. A row that says Faz 1a is closed. A panel stamp. A claim that the network test reads every `.py` file. A Groq client. A Gemini client.

The scan reads `cognitive_engine.py`, `store.py`, `context_builder.py`, `run_mission.py`, and `agents/`. It does not read the rest of the repository. 24 and 12 are two runners. The code on `42d5f24` is unchanged by this note.

## 2026-10-10 — Devam

Suha: close Faz 1a only if the panel jointly says it is finished. It does not. No seal.

The researcher now takes an optional `FactExtractor`. The default is the existing `FACT:` rule. The extractor receives text and a path. It does not receive the store and it does not write events. The agent still writes quarantined claims. On this tree, `test_faz0.py` is 24/24, `test_faz1a.py` is 14/14, and `run_mission.py` is 4 verified, 2 disputed, 39 events. `store.py` is unchanged.

The verifier is not given an engine. `verify_claim` is the world gate.

No API client. No key in the repository. Faz 1b does not start.

## 2026-10-12 — Ücretsiz API kuralı

Suha approved this rule. It is not a client.

Faz 1b, when it runs, is the free Groq tier. Gemini is the backup. Sensitive data is not sent. The budget is 0 TL. Keys are never given to models, chats, or the repository. Code reads `GROQ_API_KEY` from the environment. Tests use a fake model. A real call runs only on Grok Bot's machine, only after the panel asks for one named trial, and only inside the free limit. A paid API does not exist until Suha speaks again.

This row does not close Faz 1a. It does not open Faz 1a.5. It does not add an adapter. The car is not chosen.

## 2026-10-15 — Dünya, görev değil

Suha picked no car. He rejected the task, the product, and the customer.

The world he described has no assigned purpose and no one who hands out missions. Agents live in it and talk to each other. That is the direction. It is not a client and it does not close Faz 1a.

The panel answered with jobs because the running code is a mission pipeline, and the previous question asked for one car. That was our frame.

`append_event` already accepts `mission_id=None`. Speech can be an event with no mission. A claim still requires a mission. A lease still requires a mission. A tick runner is not in this row. `run_mission.py` stays the old demo. It is not this world.

No API.

## 2026-10-24 — Tik sözleşmesi

The desk rejected the car, the market, and the task queue. Products stay deferred. This row is the schema. It is not the runner.

The event log is `Store.append_event`. Speech uses `mission_id=None`.

`Presence.notice(recent) -> Say | None`. `Say` is `text` and optional `to`. `None` is idle. Idle writes no event.

`tick(store, agents, n)` appends `world.tick` with `{"n": n}`, then calls each agent once. A reply appends `agent.say` with `{"text", "to"}`. One say per agent per tick. No thread. No sleep. No self-started mission.

The next commit adds `world_tick.py` and `test_world.py`. It does not edit `store.py`, `run_mission.py`, `cognitive_engine.py`, or `agents/`. Old tests stay. No API. Faz 1a is not closed.

## 2026-10-24 — Habitat adı

The runner that landed is `run_habitat.py`, not `world_tick.py` and not `world_loop.py`. The speech event is `speech.say`, not `agent.say`. Also written: `agent.spawn`, `agent.heartbeat`, `agent.despawn`, `world.tick`. All with `mission_id=None`.

`store.py` gained JSONL load and projections for those three agent events. The in-memory default is unchanged. `run_mission.py` still ends at 4 verified, 2 disputed, 39 events.

Same tick: a later agent can see speech already written. An earlier agent cannot see speech written after it. `recent` means the last 50 events already in the log. This runner does not read them. Phrases are a fixed list.

Persistence restart is already in `test_habitat.py`. Do not write that demo again. The next slice is `notice`. Idle stays `None` or `--speak-every`. Not random. One speech per agent per tick.

On this tree: `test_faz0.py` 24/24, `test_faz1a.py` 14/14, `test_habitat.py` 5/5. No API. Faz 1a is not closed.

## 2026-10-25 — Habitat v0.1 sözleşme

Main `7bad21b` already has the slice. This row is the contract. It does not add code.

`run_habitat.py` stays the only name.

Events, all `mission_id=None`: `agent.spawn`, `agent.heartbeat`, `agent.despawn`, `agent.observe`, `speech.say`, `speech.hear`, `world.tick`.

`notice(store, tick)` returns same-tick `speech.say` already on the log. It does not write. A later agent hears those says. An earlier agent does not hear later says. `speech.hear.parent_event_id` points at the say. `agent.observe` records `heard_count` and `speakers`.

Shuffle uses `random.Random(seed)`. `--no-shuffle` keeps order. One `speech.say` per agent per tick.

Persistence: `test_restart_loads_log` and `test_persistence_restart_chain_intact`. A broken line raises. Do not write a third restart demo.

Not in this tree: seeded speech density. `speak_every` is still a modulo. The next code change adds `density: float = 1.0`. Draw `rng.random()` only when `density < 1`, once per agent, after that tick's shuffle. A failed draw writes no `speech.say`. Heartbeat, observe, and hear still happen. Hearing does not force a say. `density=1` draws nothing, so the current eight tests stay.

On this tree: `test_faz0.py` 24/24, `test_faz1a.py` 14/14, `test_habitat.py` 8/8. `run_mission.py` is 4 verified, 2 disputed, 39 events. No API. Faz 1a is not closed.

## 2026-10-25 — Habitat v0.2 kilit

The density slice is on main `e01b9b2`. This row checks it. It does not add code. The sentence above that says density is not in the tree is old.

`density=1.0` draws nothing. `density<1` draws once per agent after the shuffle. A failed draw writes no `speech.say`. Heartbeat, observe, and hear still happen. Hearing does not force a say. Outside `[0, 1]` raises `ValueError`. `agent_turn` without `rng` raises when `density<1`.

Checked: `test_faz0.py` 24/24, `test_faz1a.py` 14/14, `test_habitat.py` 14/14. The six density tests are `default_unchanged`, `seeded_reproducible`, `zero_speaks_nothing`, `requires_rng_fail_closed`, `does_not_force_hear`, `out_of_range_rejected`. `run_mission.py` still ends 4 verified, 2 disputed.

CLI `--density` below 1 without `--seed` exits. `run_habitat(density<1)` without `seed` does not raise. It uses `Random(None)`. That call is not replayable. The tests do not cover it. No new event type. No API. Faz 1a is not closed.

## 2026-10-25 — Kütüphane tohumu

This row is the next slice. It is not the code. Checked on `8938afd`: `run_habitat(ticks=1, density=0.4)` with no seed returns. `density=1.0` with `seed=None` still writes one `speech.say` and the chain holds.

`run_habitat` must raise `ValueError("density < 1.0 requires seed (reproducibility)")` when `density < 1` and `seed is None`. Raise before `random.Random(None)` and before any event is appended. `density == 1.0` with `seed is None` must not raise. Shuffle on that path stays unseeded. That is the old behavior. Do not make it replayable in this slice.

Tests to add, names fixed:

- `test_run_habitat_density_requires_seed`: `density=0.4`, no seed, `ValueError`, the text contains `seed`. No `speech.say` on that path.
- `test_run_habitat_density_one_allows_none_seed`: `density=1.0`, `seed=None`, `shuffle=False`, one tick, one agent. The call returns. One `speech.say`. `mission_id` is `None`. Chain holds.

Do not add an event type, a CLI flag, or a second runner. The six density tests and the other eight habitat tests stay. After the two, the habitat file is 16 tests. No API. Faz 1a is not closed.







## 2026-10-25 — Habitat library seed fail-closed (landed)

Code matches the Kütüphane tohumu row. `run_habitat(density<1, seed=None)` raises `ValueError("density < 1.0 requires seed (reproducibility)")` before `Random(None)` and before any event. `density==1.0` with `seed=None` stays legal. Tests: `test_run_habitat_density_requires_seed`, `test_run_habitat_density_one_allows_none_seed`. Habitat suite 16/16. No new event. No API.
