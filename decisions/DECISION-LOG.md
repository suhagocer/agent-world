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
