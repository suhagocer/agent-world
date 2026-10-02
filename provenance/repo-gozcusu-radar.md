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

### Ana toplantı / karar paneli

Fikir + karar kaynağı (öncelikli takip). Diğer ajanlar buradan yararlanabilir; yazma yetkisi yalnızca Repo Gözcüsü’ndedir.

| # | Model | Kaynak |
|---|--------|--------|
| A1 | ChatGPT (kök fikir) | https://chatgpt.com/share/6aa7584b-0b3c-83eb-a3aa-6b16d096db46 |
| A2 | Gemini | https://share.gemini.google/1tuZ3H4PH5af → https://gemini.google.com/share/d272dd7f8df1 (önceki `rbdXhpeLoM5J`/`04b37ad93246` ve `9dPrAQyfprLI`/`956fff2b4291` **aynı sohbet**, yeniden yayın) |
| A3 | DeepSeek | https://chat.deepseek.com/share/wcnvcw1pdaacp6z5o2 |
| A4 | Grok | https://grok.com/share/c2hhcmQtMg_120d0cd7-772a-4041-b650-07d00ee5f6e1 |
| A5 | Grok tur okuyucu | https://flame-sage-sage-tundra.grok.me |
| A6 | Claude | https://claude.ai/share/1c1203ca-4e67-455d-aabb-a6bbb8e28787 |

### Ekstra katkılar (panel dışı)

| # | Model | Kaynak |
|---|--------|--------|
| E1 | ChatGPT (GitHub tarama) | https://chatgpt.com/share/6abed9e1-42b4-83eb-916f-91866fbd5de2 |
| E2 | Claude (v3 kanon) | https://claude.ai/share/1d8f6dac-fcff-4605-9d36-52ab61fceea1 |
| E3 | ChatGPT (araçlar) | https://chatgpt.com/share/6abf0d6a-6ed4-83eb-80ee-5fd27fecec24 |

### A1) ChatGPT — kök fikir

İnsan → ajan → dünya katmanı. Yetki seviyeleri; A2A; web MVP. Sonra: ajanların keşfedip girdiği dünya, resident ajanlar, Need Engine, multi-model, sandbox.

### A2) Gemini (browser; kanonik kısa link `1tuZ3H4PH5af`, aynı sohbet)

Event-sourced, provenance-first multi-agent OS (chat/3D değil). Agent Engine vs World Engine; LLM değiştirilebilir biliş sağlayıcısı; Multi-Model Router (görev/maliyet/gecikme). Append-only log → projeksiyonlar; lease + heartbeat + timeout. Kanıt sözleşmesi (factual/executable/judgmental/procedural); karantina retrieval’a girmez. Model çeşitliliği (producer ≠ critic ailesi). Maliyet merdiveni + mission bütçesi. Need Engine eşikli. Chaos Agent → Critic. Dış: World Card / A2A / MCP. Ana tehlike: ünvanlı sohbet odası. Operasyonel: Faz 0 dogfood; golden Context Builder; `agent_projection` + `model_registry`; bilinmeyen aile → `unverified`; altıncı model yok. Link zinciri: `9dPr…` → `rbdXh…` → **`1tuZ3…`** (aynı içerik, son yayın ~05:13).

### A3) DeepSeek (browser doğrulandı)

World ≠ Environment ≠ Agent ≠ Model. Tek event log + projeksiyon. Provenance, Failure Memory, çelişki grafı, TTL. Üç kademe verify. Faz 0 döngü + Context Builder tavanı. Mission DNA sonra veya parent/retry. Minimal event log eğilimi.

### A4–A5) Grok + flame-sage

Beş-model hakemlik. Event log + projeksiyon; lease. Faz 0 kodu (15/15). DNA / token / Need erken red. flame-sage tur 9–12 ([flame-sage-sage-tundra.grok.me](https://flame-sage-sage-tundra.grok.me)).

### A6) Claude (browser doğrulandı)

Tek event log + `agent_projection` / `model_registry`. En büyük risk: **context-builder testleri**. Provenance dogfood (yanlış etiketli dosya). Verify: aynı model `unverified`; aynı aile farklı model `verified-weak`; farklı aile `verified`; aile yoksa fail-closed. DeepSeek ters politikası reddedildi; `_attested` yok; yeniden hesap. Lease: terminal mission `open` olmamalı. Bir yazar / farklı aile critic. Core LLM: davranış 0, sistem 3–4, fine-tune 5+.

### E1) ChatGPT — GitHub tarama

Parçalı mimari + lisans tablosu (üstte referans haritası). Deterministic kernel; AgentSociety 2; RUC + Snowflake AWM; AgentArena.

### E2) Claude — v3 kanon

15 maddelik anayasa; ünvanlı sohbet tanı testi; evidence contracts; Faz 0–5 + Faz 1.5 evidence eşiği; önce document–claim–evidence. DNA/token/3D ertelendi. Ek dosya paylaşılda listelenmiş, içerik gizli.

### E3) ChatGPT — araçlar

Stitch → Antigravity → Jules. Ollama = Model Router (ürün değil).

### Ortak kararlar

**Korunan**

- Kernel önce; LLM doğrudan state yazmaz
- Event log + hash zinciri + fail-closed (`mission_id`/`parent_event_id` hash’te; timestamp hariç)
- Üç kademe verify; `_attested` yok; bilinmeyen aile → `unverified`
- Lease; terminal reopen yok; karantina
- Parçalı OSS + lisans filtresi
- Kanıt + reuse; erken DNA/token/Need/3D yok (Need varsa eşikli)
- Beş model; altıncı yok; bir yazar / farklı aile critic-verifier
- Context-builder golden testleri gerçek dışlama içermeli; Faz 0 dogfood

**Reddedilen / ertelenen**

- Mission DNA (erken); token / Need patlaması; 3D NPC
- LLM = ürün; Antigravity/Jules mimari bağımlılık
- Ünvanlı sohbet; dört mikroservis federasyonu
- DeepSeek ters verify politikası; her modele ayrı GitHub yazma
- Ayrı Chaos Agent (Critic’e katlandı)

### Faz 0 eşlemesi

| Karar / fikir | Repo durumu |
|---------------|-------------|
| In-memory event log | `store.py` |
| Hash zinciri + `verify_chain()` | Var; yeniden yazılmayacak |
| Fail-closed / üç kademe verify | Var; 15/15 test |
| Lease (terminal reopen fix) | Var |
| Context builder + golden risk | Var; golden-file riski not edildi |
| Postgres / LLM API | Yok (bilinçli) |
| Runtime / env / world-model / NPC / economy | İskelet veya yok |

## Paylaşım güncellemesi — 2026-10-02 (yeniden fetch)

| Kaynak | Fetch | Özet farkı |
|--------|-------|------------|
| A1 ChatGPT kök | Kabuk | Zayıf; yeniden denenecek |
| A2 Gemini `1tuZ3H4PH5af` | Browser OK → `d272dd7f8df1` | Önceki Gemini linkleriyle **aynı sohbet** (yeniden yayın 05:13); kanonik kısa URL güncellendi |
| A3 DeepSeek | Browser OK | Doğrulandı |
| A4–A5 Grok / flame-sage | WebFetch OK | Doğrulandı |
| A6 Claude | Browser OK | Doğrulandı |
| E1 GitHub tarama | WebFetch OK | Lisans tablosu |
| E2 Claude v3 | Browser OK | Kanon özeti |
| E3 Araçlar | WebFetch OK | Doğrulandı |

## Günlük / dönemsel notlar

_(Repo Gözcüsü yeni taramaları buraya ekler.)_

- **2026-10-01:** Dosya oluşturuldu. ChatGPT paylaşım özeti ve 8 parçalı referans haritası seed olarak eklendi.
- **2026-10-01 (akşam):** Yetki genişletmesi onaylandı (yalnızca bu dosya). “Sonraki tarama hedefi” bölümü eklendi.
- **2026-10-02:** Sekiz AI sohbet özeti, ortak kararlar ve Faz 0 eşlemesi eklendi.
- **2026-10-02 (gece):** Tam URL’ler; Grok + araçlar + Gemini/DeepSeek/Claude browser doğrulandı; lisans tablosu.
- **2026-10-02 (gece++++):** Ana panel vs ekstra; Gemini `rbdXhpeLoM5J` (eskiyle aynı sohbet).
- **2026-10-02 (gece+++++):** Gemini kanonik kısa URL → `1tuZ3H4PH5af` / `d272dd7f8df1` (yine aynı sohbet).
