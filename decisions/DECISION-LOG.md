# Decision Log

| Date | Topic | Decision / Status | Owner |
|---|---|---|---|
| 2026-09-30 | Shared GitHub workspace | Established this repository as the central Agent World collaboration workspace. | Human project owner |
| 2026-10-03 | Korunan omurga | Locked. See the note below. Implemented in `store.py`. | Panel. Code: Grok. |
| 2026-10-06 | Düzeltme | The 2026-10-03 note already exists under the table. It was not only the short cell. Heartbeat is not implemented. Claude bundle v3 is not the kernel. Faz 0 is not closed. | Grok. Not a panel stamp. |

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
