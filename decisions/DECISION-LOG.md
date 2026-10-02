# Decision Log

| Date | Topic | Decision / Status | Owner |
|---|---|---|---|
| 2026-09-30 | Shared GitHub workspace | Established this repository as the central Agent World collaboration workspace. | Human project owner |
| 2026-10-03 | Korunan omurga | Locked. See the note below. Implemented in `store.py`. | Panel. Code: Grok. |

Decisions should record the conclusion, rationale, alternatives considered, unresolved objections and implementation status.

## 2026-10-03 — Korunan omurga

Conclusion. World, Agent and Model stay separate. One append-only event log. Provenance is required for a verified claim. Lease does not reopen a terminal mission. Verification has three outcomes: unverified, verified-weak, verified. An unverified family stays unverified. Same verified family and a different model is verified-weak. Two different verified families is verified. A payload flag such as `_attested` is ignored. `verify_chain` already exists and is not rewritten. The clock is not part of the hash. The model does not write world state.

Rationale. These rules are already in the kernel and in the tests (15/15 on commit 457d059). The log was missing the sentence. The radar file is not the decision record.

Alternatives rejected. Letting the repo observer write this file. Starting Faz 1 or an LLM researcher now. Merging the Claim classes in this turn. A second skip-over test.

Unresolved. None on this sentence. Claim-class merge stays unscheduled.

Status. In `store.py`. The observer still writes only `provenance/repo-gozcusu-radar.md`.
