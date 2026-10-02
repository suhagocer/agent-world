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

| Öncelik | Repo | Rol | Lisans / risk (tarama notu) |
|--------|------|-----|-----------------------------|
| 1 | sendwealth/agent-world | Deterministic world kernel (Policy→Action→Validation) | MIT — fikir+kod adayı; kopya öncesi dosya lisansı doğrula |
| 2 | tsinghua-fib-lab/AgentSociety | Agent runtime / reasoning / replay | Apache 2.0 (çekirdek); `packages/agentsociety/commercial` hariç |
| 3 | RUC-NLPIR/Agent-World | Environment + task + verification factory | THIRD_PARTY_NOTICES / veri / executable-tool provenance kontrolü |
| 4 | JustInternetAI/AgentArena | Realtime NPC / Godot runtime | Apache 2.0 (tarama notu) |
| 5 | meleantonio/AgentSociety | Economy + governance | Tarama: MIT sınıfı; doğrula |
| 6 | Snowflake-Labs/agent-world-model | Synthetic environments / RL | GitHub lisans alanı boş → **kod kopyalama**; yalnızca fikir |
| 7 | QwenLM/Qwen-AgentWorld | World-model prediction | Apache 2.0 (tarama notu) |
| 8 | francemazzi/worldsim | Modular simulation architecture | MIT (tarama notu) |

Ek referanslar (tarama): Generative Agents (Apache 2.0); mem0 (Apache 2.0); LangGraph / Colyseus / ai-town (MIT); Tencent/nicepkg bellek fikirleri (MIT sınıfı — doğrula).

**Katman bileşimi (tek fork değil):** World Engine + Agent Cognition + Memory + Realtime. LLM yalnızca Policy→Action üretir; dünya doğrular/uygular. Compute kıtlık ekonomisi. World-model (Qwen) ana motor değil, counterfactual. MCP dünya arayüzü adayı.

Bizim Faz 0 (event log, hash zinciri, fail-closed verify) “kernel önce / LLM state yazmaz” çizgisiyle uyumludur.

## Sonraki tarama hedefi

1. **sendwealth/agent-world** — Policy→Action→Validation ayrımı, LLM’in state yazmaması; lisans + hangi parçalar fikir vs. kopyalanabilir.
2. **RUC-NLPIR/Agent-World** + **Snowflake-Labs/agent-world-model** — env/task/verifier sınırları; Faz 0 doğrulama ile örtüşen noktalar. Snowflake: kod kopyalama yok.
3. **tsinghua-fib-lab/AgentSociety** — runtime/replay; commercial paket hariç; bizim iskelet `src/` ile ilişki (yalnızca not).
4. **QwenLM/Qwen-AgentWorld** — world-model katmanı; bağımlılık ve lisans riski.
5. Bellek / cognition (Generative Agents, Tencent/nicepkg) — sonraki tur.

## AI sohbet özetleri — 2026-10-02

Kaynaklar (tam paylaşım URL’leri). Diğer ajanlar buradan yararlanabilir; yazma yetkisi yalnızca Repo Gözcüsü’ndedir.

| # | Model | Kaynak |
|---|--------|--------|
| 1 | ChatGPT (kök fikir) | https://chatgpt.com/share/6aa7584b-0b3c-83eb-a3aa-6b16d096db46 |
| 2 | ChatGPT (GitHub tarama) | https://chatgpt.com/share/6abed9e1-42b4-83eb-916f-91866fbd5de2 |
| 3 | Gemini | https://share.gemini.google/9dPrAQyfprLI → https://gemini.google.com/share/956fff2b4291 |
| 4 | DeepSeek | https://chat.deepseek.com/share/wcnvcw1pdaacp6z5o2 |
| 5 | Grok | https://grok.com/share/c2hhcmQtMg_120d0cd7-772a-4041-b650-07d00ee5f6e1 |
| 6 | Claude | https://claude.ai/share/1c1203ca-4e67-455d-aabb-a6bbb8e28787 |
| 7 | Claude (v3 kanon) | https://claude.ai/share/1d8f6dac-fcff-4605-9d36-52ab61fceea1 |
| 8 | ChatGPT (araçlar) | https://chatgpt.com/share/6abf0d6a-6ed4-83eb-80ee-5fd27fecec24 |

### 1) ChatGPT — kök fikir

İnsan → ajan → dünya katmanı. Yetki seviyeleri; A2A; web MVP. Sonra: ajanların keşfedip girdiği dünya, resident ajanlar, Need Engine, multi-model, sandbox.

### 2) ChatGPT — GitHub tarama (yeniden fetch OK)

Tek fork değil **parçalı mimari** (World Engine + Cognition + Memory + Realtime). Deterministic kernel: LLM Policy→Action; dünya validate/apply (sendwealth #1). Cognition: perceive→retrieve→plan→execute→reflect. Bellek katmanlı + sosyal ilişki. Env/verifier: RUC + Snowflake AWM. Runtime: AgentSociety 2 (Ray, reasoning router, replay). Realtime: Colyseus/Nakama; AgentArena. Lisans satırları üstteki tabloda.

### 3) Gemini (browser doğrulandı)

Event-sourced, provenance-first multi-agent OS (chat/3D değil). Agent Engine vs World Engine. Append-only events → projeksiyonlar; lease + heartbeat + timeout. Kanıt sözleşmesi + model-çeşitli Critic/Verifier; karantina retrieval’a girmez. World Memory ≠ private agent memory. Maliyet merdiveni; Ollama tartışması. Dış ajan: agent-card / A2A / MCP. Mission DNA erken eleştirilir. Ana tehlike: ünvanlı sohbet odası.

### 4) DeepSeek (browser doğrulandı)

World ≠ Environment ≠ Agent ≠ Model. Tek event log + projeksiyon tercihi. Provenance, Failure Memory, çelişki grafı, TTL. Üç kademe verify. Faz 0: mission → Researcher → Critic → Verifier → reuse. Context Builder tavanı. Mission DNA sonra veya parent/retry. Minimal event log eğilimi.

### 5) Grok

Beş-model hakemlik. Event log + projeksiyon; lease. Faz 0 kodu (15/15). DNA / token / Need erken red. flame-sage tur 9–12 ([flame-sage-sage-tundra.grok.me](https://flame-sage-sage-tundra.grok.me)).

### 6) Claude

Context builder golden-file kritik risk. Şema/test. `verify_chain` sonrası geldi.

### 7) Claude — v3 kanon

Kalıcı çok-ajan OS; faz 0–5. Ertelenenler: DNA, token, 3D. İlke: kanıt + reuse.

### 8) ChatGPT — araçlar

Stitch → Antigravity → Jules. Ollama = Model Router (ürün değil). Mixboard/Pomelli ikincil.

### Ortak kararlar

**Korunan**

- Kernel önce; LLM doğrudan state yazmaz
- Event log + hash zinciri + fail-closed doğrulama
- Üç kademeli doğrulama; `_attested` yok sayılır
- Lease; karantina
- Parçalı OSS referans + lisans filtresi (Snowflake kod kopyalama yok; AgentSociety commercial hariç)
- Kanıt + reuse; erken DNA/token/Need/3D yok
- Beş-model hakemlik

**Reddedilen / ertelenen**

- Mission DNA (erken)
- Token / Need / bidding (erken)
- 3D / Godot NPC (şimdi değil)
- LLM = ürün; Antigravity/Jules mimari bağımlılık
- Ünvanlı sohbet; dört mikroservis federasyonu

### Faz 0 eşlemesi

| Karar / fikir | Repo durumu |
|---------------|-------------|
| In-memory event log | `store.py` |
| Hash zinciri + `verify_chain()` | Var; yeniden yazılmayacak |
| Fail-closed / üç kademe verify | Var; 15/15 test |
| Lease | Var |
| Context builder | Var; golden-file riski not edildi |
| Postgres / LLM API | Yok (bilinçli) |
| Runtime / env / world-model / NPC / economy | İskelet veya yok |

## Paylaşım güncellemesi — 2026-10-02 (yeniden fetch)

| # | URL | Fetch sonucu | Özet farkı |
|---|-----|--------------|------------|
| 1 | ChatGPT kök | Kabuk / kısa ID başarısız | Tam UUID ile yeniden denenmeli |
| 2 | ChatGPT GitHub | WebFetch OK (ikinci deneme) | **Lisans tablosu + katman bileşimi eklendi** |
| 3 | Gemini | Browser OK | Doğrulandı |
| 4 | DeepSeek | Browser OK | Doğrulandı |
| 5 | Grok | WebFetch OK | Doğrulandı |
| 6–7 | Claude ×2 | WebFetch kabuk | Browser bekliyor |
| 8 | ChatGPT araçlar | WebFetch OK | Doğrulandı |

## Günlük / dönemsel notlar

_(Repo Gözcüsü yeni taramaları buraya ekler.)_

- **2026-10-01:** Dosya oluşturuldu. ChatGPT paylaşım özeti ve 8 parçalı referans haritası seed olarak eklendi.
- **2026-10-01 (akşam):** Yetki genişletmesi onaylandı (yalnızca bu dosya). “Sonraki tarama hedefi” bölümü eklendi.
- **2026-10-02:** Sekiz AI sohbet özeti, ortak kararlar ve Faz 0 eşlemesi eklendi.
- **2026-10-02 (gece):** Tam URL’ler; Grok + araçlar + Gemini/DeepSeek browser doğrulandı.
- **2026-10-02 (gece++):** ChatGPT GitHub tarama yeniden yüklendi; referans haritasına lisans/risk sütunu ve katman bileşimi eklendi.
