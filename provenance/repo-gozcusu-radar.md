# Repo Gözcüsü — açık kaynak radar

> **Sahip:** Repo Gözcüsü botu. Bu dosya yalnızca bu bot tarafından güncellenir.
> Diğer dosyalara dokunulmaz. Kod birleştirme / PR merge burada yapılmaz.

## Amaç

Bu dosya, [agent-world](https://github.com/suhagocer/agent-world) projesinin gelişimine katkıda bulunacak **açık kaynaklı projeler, kod parçaları ve mimari fikirleri** toplar ve analiz eder.

Diğer modeller ve ajanlar çalışmalarını yürütürken **bu dosyadaki içeriklerden yararlanabilir**; kendi çıktılarını buraya yazmamalıdır — yazma yetkisi yalnızca Repo Gözcüsü’ndedir.

## Kapsam kuralları

- Yalnızca bu dosya (`provenance/repo-gozcusu-radar.md`) güncellenir.
- `store.py`, `schema.sql`, testler ve diğer kaynaklara dokunulmaz.
- Lisans / ticari risk notları her girişte belirtilir.
- Doğrudan kopyalanacak kod vs. yalnızca fikir olarak alınacak ayrımı net yazılır.

## Referans haritası (ChatGPT tarama özeti, Eyl 2026)

| Öncelik | Repo | Rol |
|--------|------|-----|
| 1 | sendwealth/agent-world | Deterministic world kernel (Policy→Action→Validation) |
| 2 | tsinghua-fib-lab/AgentSociety | Agent runtime / reasoning / replay |
| 3 | RUC-NLPIR/Agent-World | Environment + task + verification factory |
| 4 | JustInternetAI/AgentArena | Realtime NPC / Godot runtime |
| 5 | meleantonio/AgentSociety | Economy + governance |
| 6 | Snowflake-Labs/agent-world-model | Synthetic environments / RL |
| 7 | QwenLM/Qwen-AgentWorld | World-model prediction |
| 8 | francemazzi/worldsim | Modular simulation architecture |

Bizim Faz 0 (event log, hash zinciri, fail-closed verify) “kernel önce / LLM state yazmaz” çizgisiyle uyumludur.

## Sonraki tarama hedefi

1. **sendwealth/agent-world** — Policy→Action→Validation ayrımı, LLM’in state yazmaması; lisans + hangi parçalar fikir vs. kopyalanabilir.
2. **RUC-NLPIR/Agent-World** + **Snowflake-Labs/agent-world-model** — env/task/verifier sınırları; Faz 0 doğrulama ile örtüşen noktalar.
3. **tsinghua-fib-lab/AgentSociety** — runtime/replay; bizim iskelet `src/` ile ilişki (yalnızca not, kod yok).
4. **QwenLM/Qwen-AgentWorld** — world-model katmanı; bağımlılık ve lisans riski.
5. Bellek / cognition referansları (Generative Agents, Tencent/nicepkg fikirleri) — sonraki tur.

## Günlük / dönemsel notlar

_(Repo Gözcüsü yeni taramaları buraya ekler.)_

- **2026-10-01:** Dosya oluşturuldu. ChatGPT paylaşım özeti ve 8 parçalı referans haritası seed olarak eklendi.
- **2026-10-01 (akşam):** Yetki genişletmesi onaylandı (yalnızca bu dosya). “Sonraki tarama hedefi” bölümü eklendi.
