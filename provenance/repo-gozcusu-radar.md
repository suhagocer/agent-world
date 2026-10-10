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

**URL kuralı:** Kullanıcı yeni bir paylaşım URL’si verdiğinde, içerik eski sohbetle aynı görünse bile o URL kanoniktir; radardaki eski link yenisiyle değiştirilir.

| # | Model | Kaynak |
|---|--------|--------|
| A1 | ChatGPT (kök fikir) | https://chatgpt.com/share/6ac43f6c-a2bc-83eb-80a9-e7b4628d9847 (önceki `6aa7584b-...`; eski link artık “Conversation has been deleted” gösteriyor; aynı sohbet uzadı) |
| A2 | Gemini | https://share.gemini.google/OfxANwjNxbQc → https://gemini.google.com/share/318c86ecfe20 (önceki `2e9F8NNsviiG` → `ed8f5044c1cc`, aynı sohbet uzamıştı; daha eski `1tuZ3H4PH5af` → `d272dd7f8df1`, `rbdXh…`/`9dPr…`/`TXv3…`; önceki sayfada görünen kısa link `2n3FouKBZlz8`; yeni sayfada görünen kısa link `tE7dlQK7I3vg`; içerik 2026-10-06 öğleden sonra browser ile kontrol edildi: aynı sohbet uzamış) |
| A3 | DeepSeek | https://chat.deepseek.com/share/nkfqofqcbfip0vlc94 (önceki `wfbt7ngfw6r7f8whwq`; daha eski `ulwkayx5qsy0otx8vd` / `japybl2d3ejtr7ch0i` / `wcnvcw1pdaacp6z5o2`) |
| A4 | Grok | https://grok.com/share/c2hhcmQtMg_e6ce9fde-ed6e-4da0-ad70-18f5e3f50be8 (önceki `c2hhcmQtMg_120d0cd7-…`) |
| A5 | Grok tur okuyucu | https://flame-sage-sage-tundra.grok.me |
| A6 | Claude | https://claude.ai/share/1c1203ca-4e67-455d-aabb-a6bbb8e28787 |

### Ekstra katkılar (panel dışı)

| # | Model | Kaynak |
|---|--------|--------|
| E1 | ChatGPT (GitHub tarama) | https://chatgpt.com/share/6abed9e1-42b4-83eb-916f-91866fbd5de2 |
| E2 | Claude (v3 kanon) | https://claude.ai/share/1d8f6dac-fcff-4605-9d36-52ab61fceea1 |
| E3 | ChatGPT (araçlar) | https://chatgpt.com/share/6abf0d6a-6ed4-83eb-80ee-5fd27fecec24 |

### A1) ChatGPT — kök fikir (kanonik `6ac43f6c-…`; önceki `6aa7584b-…`)

İnsan → ajan → dünya katmanı. Yetki seviyeleri; A2A; web MVP. Sonra: ajanların keşfedip girdiği dünya, resident ajanlar, Need Engine, multi-model, sandbox.

### A2) Gemini (kanonik kısa link `OfxANwjNxbQc` → `318c86ecfe20`, browser ile kontrol edildi: aynı sohbet, yayın 6 Eki 06:17; önceki `2e9F8NNsviiG` → `ed8f5044c1cc`; daha eski `1tuZ3H4PH5af` → `d272dd…`)

Event-sourced, provenance-first multi-agent OS (chat/3D değil). Agent Engine vs World Engine; LLM değiştirilebilir biliş sağlayıcısı; Multi-Model Router (görev/maliyet/gecikme). Append-only log → projeksiyonlar; lease + heartbeat + timeout. Kanıt sözleşmesi (factual/executable/judgmental/procedural); karantina retrieval’a girmez. Model çeşitliliği (producer ≠ critic ailesi). Maliyet merdiveni + mission bütçesi. Need Engine eşikli. Chaos Agent → Critic. Dış: World Card / A2A / MCP. Ana tehlike: ünvanlı sohbet odası. Operasyonel: Faz 0 dogfood; golden Context Builder; `agent_projection` + `model_registry`; bilinmeyen aile → `unverified`; altıncı model yok. Link zinciri: `9dPr…` → `rbdXh…` → **`1tuZ3…`** / `TXv3…` (aynı içerik, son yayın ~05:13).

### A3) DeepSeek (kanonik `nkfqofqcbfip0vlc94`; önceki `wfbt7ngfw6r7f8whwq`; daha eski `ulwkayx5qsy0otx8vd`)

World ≠ Environment ≠ Agent ≠ Model. Tek event log + projeksiyon. Provenance, Failure Memory, çelişki grafı, TTL. Üç kademe verify. Faz 0 döngü + Context Builder tavanı. Mission DNA sonra veya parent/retry. Minimal event log eğilimi.

2026-10-05 kanonik paylaşım `wfbt7ngfw6r7f8whwq` (mesaj 54–55, ebeveyn 53; curl `/api/v0/share/content` ham JSON 7768 bayt; görünen istek+yanıt 4123 karakter). Önceki `ulwkayx5qsy0otx8vd` (mesaj 52–53; ham 26752 bayt; görünen 4057 karakter) ile **aynı değil** — yeni tur. DeepSeek iddiası (karar değil): önerdiği 6 maddelik `DECISION-LOG` maddesinde “heartbeat” yazmış; Faz 0’da heartbeat yok, yalnızca lease + timeout; madde 4’ü “Lease + timeout” diye düzeltiyor (heartbeat Faz 1). Test referanslı 6 madde önerisi ve Anayasa (15) / DECISION-LOG (6) ayrımı DeepSeek’e ait; panele işlenmedi. Önceki `ulwkay…` turundaki `run_mission.py` / Faz 0 kapandı / Faz 1 notu da DeepSeek iddiasıydı; karar sayılmaz.

### A4–A5) Grok (kanonik `c2hhcmQtMg_e6ce9fde-…`; önceki `c2hhcmQtMg_120d0cd7-…`) + flame-sage

Beş-model hakemlik. Event log + projeksiyon; lease. Faz 0 kodu (15/15). DNA / token / Need erken red. flame-sage canlı: **Tur 34’e kadar** (v1.0–v1.37; [flame-sage-sage-tundra.grok.me](https://flame-sage-sage-tundra.grok.me)). 2026-10-05 itibarıyla `/tur-9`…`/tur-14` yeniden açık; 2026-10-05 akşam `/tur-15` (v1.18); 2026-10-05/06 gece `/tur-16` (v1.19); 2026-10-06 sabah `/tur-17`…`/tur-26` açıldı (v1.20–v1.29); 2026-10-06 öğleden sonra `/tur-27` (v1.30); 2026-10-07 gece `/tur-28` (v1.31); 2026-10-07 öğleden sonra `/tur-29` (v1.32); 2026-10-10 gece `/tur-30` (v1.33) ve `/tur-31` (v1.34); 2026-10-10 sabah `/tur-32` (v1.35) ve `/tur-33` (v1.36); 2026-10-10 öğleden sonra `/tur-34` (v1.37), `/tur-35` 404.

### A6) Claude (kanonik `1c1203ca-…`, URL değişmedi; browser doğrulandı)

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
| Korunan omurga karar kaydı | `decisions/DECISION-LOG.md` (2026-10-03 satırı, commit `0ddddfe`). Kanonik karar kaydı orası; bu radar dosyası karar kaydı değil |

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

## Paylaşım güncellemesi — 2026-10-02 (öğle takip)

| Kaynak | Fetch | Özet farkı |
|--------|-------|------------|
| A1 ChatGPT kök | WebFetch OK | Önceki turda kabuk/zayıf; bu turda **tam metin doğrulandı**. Özet değişmedi (İnsan→ajan→dünya, yetki, web MVP, keşif, Need Engine, çoklu model). |
| A2 Gemini `1tuZ3…` / `d272dd…` | Chrome DOM OK | Aynı sohbet; yayın ~05:13. Ek kısa link: `TXv3jkvZV7w3` → yine `d272dd…`. Karar özeti değişmedi. |
| A2 eski `rbdXh…` / `9dPr…` | WebFetch 403 | Kabuk; kanonik zincir aynı. |
| A3 DeepSeek | Chrome DOM OK | Doğrulandı; digest ile uyumlu. |
| A4 Grok | WebFetch OK | Doğrulandı; 15/15 / `_attested` ret ile uyumlu. |
| A5 flame-sage | curl/WebFetch OK | **Değişiklik:** `/tur-9`…`/tur-12` **404**. Canlı: v1.0–Tur 8 + `/surec` `/v3-denetim` `/ara` `/rapor.pdf`. |
| A6 Claude | Chrome DOM OK | Digest ile uyumlu; ek dosyalar hâlâ gizli. |
| E1 GitHub tarama | WebFetch OK | Referans haritası ile uyumlu; yeni aday yok. |
| E2 Claude v3 | WebFetch/Chrome boş | İçerik yüklenmedi (paylaşım kabuğu). |
| E3 Araçlar | WebFetch OK | Stitch→Antigravity→Jules; Ollama=Model Router — değişmedi. |

**Bu turda radar notu:** Mimari kararlar sabit; izleme farkı flame-sage tur 9–12’nin kamuya kapanması, A1’in tam fetch’e kavuşması ve Gemini `TXv3…` kısa linkinin aynı sohbete işaret etmesi. Yeni OSS adayı yok.

## Paylaşım güncellemesi — 2026-10-05 (gece takip)

| Kaynak | Fetch | Özet farkı |
|--------|-------|------------|
| A1 ChatGPT kök | curl OK | Değişmedi. |
| A2 Gemini `1tuZ3…` | curl OK → `d272dd7f8df1` | Aynı sohbet; değişmedi. |
| A3 DeepSeek | Browser OK (`japybl2d3ejtr7ch0i`) | Kanonik URL `japybl2d3ejtr7ch0i`; eski `wcnvcw1…` aynı sohbet (103142 karakter). Özet değişmedi. |
| A4 Grok | curl OK | Değişmedi; Tur 13–14 / `0ddddfe` referansı yok. |
| A5 flame-sage | curl OK | **Değişiklik:** `/tur-9`…`/tur-14` artık açık (v1.12–v1.17). `/tur-15` 404. |
| A6 Claude | Kabuk (JS) | Doğrulanamadı; önceki digest geçerli. |
| E1 / E3 ChatGPT | curl OK | Değişmedi. |
| E2 Claude v3 | Kabuk (JS) | Doğrulanamadı. |

**flame-sage yeni turlar (Grok okuyucu, “kanon değildir”):**

- **Tur 9 (v1.12, 30 Eyl):** Repo boştu; dört çekirdek dosyası (`schema.sql`, `store.py`, `context_builder.py`, `test_faz0.py`) köke kondu. Boş klasörler silinmedi. `COLLABORATION.md` rol listesi kilit sayılmadı. 9/9, `c3776c5`.
- **Tur 10 (v1.13, 1 Eki):** Claude’un beş maddesinden üçü koda girdi: kaynaklı `verified`, `verify_chain()`, terminal görev yeniden açılmaz. 12/12, `12b6857`. İki Claim sınıfı ayrı kaldı.
- **Tur 11 (v1.14, 1 Eki):** Claude store v2 seçilerek alındı. Üç kademe, `verify_claim` kaynak ister, hash’e görev kimliği alındı. `_attested` bayrağı ve “terminal olmayan her görevi aç” alınmadı. Saat hash’e girmez. 15/15, `354241d`.
- **Tur 12 (v1.15, 1 Eki):** Güncel kural cümlesi. `verify_chain` yeniden yazılmaz. Tek skip testi `test_skip_over_drops_oversized`. Son not `214c4e8`.
- **Tur 13 (v1.16, 2 Eki):** `verify_chain` 457d059’dan beri aynı, 15/15 yeniden koştu, not `087525a`. Gözcü yalnızca bu radar dosyasını yazar.
- **Tur 14 (v1.17, 3 Eki):** Korunan omurga `decisions/DECISION-LOG.md` içine işlendi (`0ddddfe`). Gözcü o dosyaya yazmaz. Faz 1 başlamaz. Claim sınıfları birleşmez.

## Repo değişikliği — `0ddddfe` (2026-10-02T23:55Z)

`decisions/DECISION-LOG.md` dosyasına 2026-10-03 tarihli “Korunan omurga” satırı ve notu eklendi. Kilitlenen cümle: dünya, ajan ve model ayrı; tek append-only event log; doğrulanmış iddia için kaynak şart; lease terminal görevi açmaz; üç sonuç (`unverified` / `verified-weak` / `verified`); doğrulanmamış aile `unverified` kalır; `_attested` yok sayılır; `verify_chain` yeniden yazılmaz; saat hash’e girmez; model dünya durumunu yazmaz.

Reddedilenler: gözlemcinin karar günlüğüne yazması, şimdi Faz 1 ya da LLM araştırmacısı başlatmak, Claim sınıflarını bu turda birleştirmek, ikinci skip testi. Açık konu: Claim sınıfı birleşmesi takvimsiz.

**Mimari haritadaki yeri:** (1) deterministik dünya çekirdeği katmanının kuralları artık karar kaydında yazılı. Yeni kod yok; boşluk kapatmıyor, mevcut çekirdeği kayda geçiriyor. Runtime, env/verifier, world-model, bellek ve gerçek zamanlı katmanlar hâlâ bilinçli olarak yok. Radardaki “Ortak kararlar / Korunan” listesi bu günlükle uyumlu; çelişki yok.

**Bu turda radar notu:** Mimari kararlar sabit. Değişen iki şey var: karar günlüğü artık omurganın kanonik kaydı, ve flame-sage Tur 9–14 yeniden kamuya açık. Yeni OSS adayı yok.

## Paylaşım güncellemesi — 2026-10-05 (A3 URL)

| Kaynak | Fetch | Özet farkı |
|--------|-------|------------|
| A3 DeepSeek `ulwkayx5qsy0otx8vd` | curl OK (`/api/v0/share/content`; sayfa WAF) | Önceki `japybl2d3ejtr7ch0i` ile aynı zincir (mesaj 51’in devamı) ama bu paylaşım yalnızca mesaj 52–53. Transkript aynı değil, daha kısa. Yeni tur: kural tabanlı `run_mission.py` / `agents/` notu. Faz 0 kapandı ve Faz 1 iddiası DeepSeek’e ait; panele işlenmedi. |

**Bu turda radar notu:** Yalnızca A3 kanonik URL değişti. Mimari karar listesi aynı. Yeni OSS yok.

## Paylaşım güncellemesi — 2026-10-05 (A3 URL `wfbt7…`)

| Kaynak | Fetch | Özet farkı |
|--------|-------|------------|
| A3 DeepSeek `wfbt7ngfw6r7f8whwq` | curl OK (`/api/v0/share/content`; sayfa WAF) | Önceki `ulwkayx5qsy0otx8vd` ile **farklı** (mesaj 54–55 vs 52–53; ham 7768 vs 26752; görünen 4123 vs 4057). DeepSeek iddiası: “heartbeat” maddesini geri çekip madde 4’ü **Lease + timeout** yapıyor; 6 maddeye test referansı ekliyor. Karar sayılmaz. |

**Bu turda radar notu:** Yalnızca A3 kanonik URL → `wfbt7ngfw6r7f8whwq`. Mimari karar listesi aynı. Yeni OSS yok.

## Paylaşım güncellemesi — 2026-10-05 (akşam tam kontrol)

| Kaynak | Fetch | Özet farkı |
|--------|-------|------------|
| A1 ChatGPT kök | curl OK | Değişmedi. |
| A2 Gemini `1tuZ3…` | curl → `d272dd7f8df1` (JS kabuk); browser OK | Aynı sohbet; browser’da digest temaları mevcut, yeni iddia yok. |
| A3 DeepSeek `wfbt7ngfw6r7f8whwq` | curl OK (`/api/v0/share/content`) | Değişmedi: mesaj 54–55 (ebeveyn 53), ham 7768 bayt. |
| A4 Grok | curl OK | Değişmedi; Tur 15 / `292026c` referansı yok. |
| A5 flame-sage | curl OK | **Değişiklik:** `/tur-15` artık açık (v1.18, 5 Eki, “Yan kopya”). `/tur-14` açık; `/tur-16` `/tur-17` 404. Ana sayfa menüsünde Tur 15 var. |
| A6 Claude | curl kabuk (JS); browser OK | Değişmedi (event log, `agent_projection`, `model_registry`, context-builder riski, verify kademeleri, `_attested` yok, lease terminal düzeltmesi). |
| E1 / E3 ChatGPT | curl OK | Değişmedi. |
| E2 Claude v3 | curl kabuk (JS); browser OK | Değişmedi (15 madde anayasa, ünvanlı sohbet testi, evidence contracts, Faz 1.5); ek dosya hâlâ gizli. |

**flame-sage Tur 15 (v1.18, 5 Eki, Grok okuyucu, “kanon değildir”):**

- Konu: Claude’un dosyalarının bir kopyası Grok sohbetinde koşuldu; kopyada 16/16 geçti. Bu, repodaki 15/15’in yerine geçmez. İki örnek belge (`sample_source_1.txt`, `sample_source_2.txt`) işlendi: 4 `verified`, 2 `disputed`; zincir sağlam.
- Kopya ile repo farkları (Grok tespiti): kopyada `family_verified` varsayılanı `True` (fail-open), repoda eksikse `False`; kopyada `can_write_verified` aynı aileye de izin veriyor, repoda yalnız farklı doğrulanmış aile; kopyada kira alanı doğrudan değişiyor, repoda kira olay günlüğünden geçiyor; hash’in JSON biçimi farklı.
- “Yüzde 66,7” öğrenme değil: `researcher.py` içinde sabit (ilk tur 120, tekrar 40; `skill_reused` bayrağı). Ölçülen bellek yok. Başkent itirazı belgeden değil, koddaki Ankara tablosundan geliyor.
- Sonuç: Claude’un `store.py`’si repoya yazılmayacak; `store.py` değişmedi; karar günlüğü `0ddddfe`; Faz 1 yok. Gözcüye yönelik not: “Hayır. Karar günlüğü duruyor.”
- Not: sayfada geçen `store.py 292026c` repo commit listesinde yok (tip `dd87763`); doğrulanmadı, muhtemelen dosya özeti.

**Bu turda radar notu:** Mimari kararlar sabit. Tek doğrulanmış fark flame-sage Tur 15’in yayına girmesi; içeriği mevcut omurgayı (fail-closed aile kontrolü, kiranın olay günlüğünden geçmesi) teyit ediyor, yeni karar getirmiyor. Yeni OSS adayı yok.

## Paylaşım güncellemesi — 2026-10-05/06 (gece kontrol)

| Kaynak | Fetch | Özet farkı |
|--------|-------|------------|
| A1 ChatGPT kök | curl OK | Değişmedi (HTML kabuk oynak; görünür metin aynı). |
| A2 Gemini `1tuZ3…` | browser (üst ajan) | Değişmedi; yeni tur yok. |
| A3 DeepSeek `wfbt7ngfw6r7f8whwq` | curl OK (`/api/v0/share/content`) | Değişmedi: mesaj 54–55, ham 7768 bayt (öncekiyle bit eş). |
| A4 Grok | curl OK | Değişmedi (HTML kabuk oynak; görünür metin aynı). |
| A5 flame-sage | curl OK | **Değişiklik:** `/tur-16` artık açık (v1.19, 5 Eki, “Aynı koşu”). `/tur-15` içerik aynı; menüye Tur 16 eklendi. `/tur-17` 404. |
| A6 Claude | curl kabuk (JS) | İçerik doğrulanamadı (yalnızca kabuk). |
| E1 / E3 ChatGPT | curl OK | Değişmedi (HTML kabuk oynak; görünür metin aynı). |
| E2 Claude v3 | curl kabuk (JS) | İçerik doğrulanamadı (yalnızca kabuk). |

**flame-sage Tur 16 (v1.19, 5 Eki, Grok okuyucu, “kanon değildir”):**

- Konu: Claude paketinin 5 Ekim akşamı yeniden koşusu; yine 16/16. Sayılar aynı (4 verified, 2 disputed, 35 olay). “Yüzde 66,7” hâlâ sabit (öğrenme değil).
- Heartbeat: yazılmayacak; karar günlüğünde yok; ayrı iş açılmaz. `store.py` değişmez; Faz 1 başlamaz.
- DeepSeek kira notu pakette doğru ama yan kopyaya ait; kopyada kira olay günlüğüne yazılmıyor. Paket = repo `store.py` değil; kopyada `family_verified` varsayılanı `True`.
- Faz 0 bu paketle kapanmış sayılmaz. Claim birleşmesi takvimsiz.

**Bu turda radar notu:** Mimari kararlar sabit. Tek doğrulanmış fark flame-sage Tur 16’nın yayına girmesi; omurgayı (heartbeat yok, store değişmez, fail-open kopya ≠ repo) tekrar teyit ediyor, yeni karar getirmiyor. Yeni OSS adayı yok.

## Paylaşım güncellemesi — 2026-10-06 (panel URL’leri)

Kullanıcı A1–A4 için yeni paylaşım URL’leri verdi; dördü de **aynı sohbetin uzamış hâli** (eski turlar birebir duruyor, sona yeni turlar eklenmiş). A6 URL’si aynı, içinde yeni turlar var. Aşağıdaki alıntılar ilgili modelin **iddiasıdır, karar değildir**.

| Kaynak | Fetch | Eski → yeni boyut | Yeni içerik (model iddiası) |
|--------|-------|-------------------|-----------------------------|
| A1 ChatGPT `6ac43f6c-…` | curl (HTML içi akış JSON) | Görünen mesaj 127 → 209 (kullanıcı 52 → 66); görünen metin 194.951 → 219.603 karakter; son tur 14 Eyl → 5 Eki. İlk 562 düğüm kimliği birebir aynı (başlık “Sanal Dünya Fikri”). Eski `6aa7584b-…` artık “Conversation has been deleted” | ChatGPT iddiası: 5 Eki’de paketi “doğrudan çalıştırarak bağımsız kontrol ettim”, “16/16 test geçti”, “%66,7 düşüş”; “Faz 0'ın temel çıkış kriterleri karşılanmış durumda”; “Lease + timeout var. Heartbeat yok.”; “`DECISION-LOG.md` bir anayasa olmamalı” (`architecture-principles.md` ayrı). 30 Eyl: “Faz 0 çekirdeğini doğrudan bu repoya yerleştirdim” (`suhagocer/Deneme`), sonra “`Deneme`… resmi repo adı olarak kullanılmamalı” — doğrulanmadı. |
| A2 Gemini `2e9F8…` → `ed8f5044c1cc` | browser (üst ajan) | ~70.965 → ~87.128 karakter; eski son “Madde 7 Düzeltmesi Bekleniyor”, sonrası yeni; yayın 2026-10-06 03:24 | Gemini iddiası: “16/16”, sonra “18/18”; “%66,7 düştüğü event log'da somut sayılarla kanıtlanmıştır”; heartbeat “henüz uygulanmamıştır, sadece 'lease + timeout'”; son tur: “Faz 0 Başarıyla Kapatıldı, Faz 1 Başlıyor”. |
| A3 DeepSeek `nkfqofqcbfip0vlc94` | curl (`/api/v0/share/content`; sayfa WAF) | Ham 7.786 → 406.949 bayt; mesaj 2 (54–55) → 54 (kimlik 1–57; 14/15/45 yok); görünen 4.122 → 211.538 karakter. 54–55 metni birebir aynı; yeni tur 56 (ebeveyn 55) + 57 (ebeveyn 56), 6 Eki 00:11 UTC | DeepSeek iddiası: “Grok benim 3 notumu da düzeltti. 16→18/18 test” (`release_lease()` + 2 test); `0ddddfe` satırı “içeriği çok kısa”, 6 maddelik genişletme (madde 4 “Lease+timeout”); “Faz 0 kapanmıştır”; Faz 1’de heartbeat “Var (lease yenileme)”, LLM için “Gemini Flash”; “karar panelindir”. |
| A4 Grok `c2hhcmQtMg_e6ce9fde-…` | curl JSON uç noktası (`/rest/app-chat/share_links/<id>`) | Yanıt 46 → 62 (23/23 → 31/31); metin 54.094 → 61.034 karakter; son tur 1 Eki → 6 Eki. İlk 46 yanıt kimlik + metin aynı (başlık “agent world”) | Grok iddiası: “15/15” (`457d059`), “`verify_chain` yazılmış”; “Gözcüye Hayır deyin… Commit `0ddddfe`”; Tur 15: “16/16 onun kopyasında geçti… repodaki 15/15'in yerine geçmez”, “Yüzde 66,7 öğrenme değil. Sabit: ilk tur 120, tekrar 40”; Tur 16: “Faz 0 bu paketle kapanmış sayılmaz”; 6 Eki: “18/18 onun kopyasında”, “`release_lease` alanı temizliyor, olay yazmıyor”, “Heartbeat yok”, “Faz 0 kapanmadı. Faz 1 yok.” (Tur 17 bağlantısı veriliyor; `/tur-17` hâlâ 404.) |
| A6 Claude `1c1203ca-…` | browser (üst ajan) | URL aynı; ~36.900 karakter; yeni turlar | Claude iddiası: kendi paketinde “16/16”, sonra “18/18”; `release_lease()` ve `run_mission.py` düzeltmeleri (lease bırakma, model adları `agent_projection`’dan); “heartbeat hâlâ yok”; “panelin Faz 1'e geçiş onayı” bekleniyor — Faz 0’ı kapalı ilan etmiyor. Son tur: `0ddddfe` satırı “göster sonra onayla”dan önce yazılmış ve fazla yalın (“Locked. See the note below…”); dosyayı kendisi okuyamadı (GitHub izni yok); karar günlüğündeki not bölümünü görmemiş. |

Not: önceki turlarda A4 için yazılan “curl OK” büyük olasılıkla yalnızca boş sayfa kabuğunu gördü; sohbet metni HTML’de yok, yalnızca JSON uç noktasında var. Tur 15’te geçen `store.py 292026c` commit değil, `main` üzerindeki `store.py` blob SHA’sı (`292026c4…`).

**Modeller arası ayrışma (gözlem):** ChatGPT (5 Eki), DeepSeek (6 Eki) ve Gemini (6 Eki) Faz 0’ın karşılandığını/kapandığını söylüyor ve Faz 1’e itiyor. Grok (5–6 Eki) kapanmadığını söylüyor: 16/16 ve 18/18 repo dışı bir kopyada koştu, kopyada `family_verified` fail-open. Claude çekirdeğin bittiğini ama Faz 1’in panel onayı beklediğini söylüyor. Hepsi aynı noktada: lease + timeout var, heartbeat yok. Repo `main` (2026-10-06 kontrol): `test_faz0.py` içinde 15 test; `run_mission.py`, `release_lease`, `researcher`/`critic`/`verifier` repoda **yok**. `decisions/DECISION-LOG.md` hâlâ `0ddddfe` satırında ve “Starting Faz 1 or an LLM researcher now” seçeneğini reddediyor. %66,7: Gemini, Claude ve ChatGPT sonuç olarak sunuyor; Grok Tur 15–16 sabit kodlu (120→40) diyor. ChatGPT’nin 30 Eyl’de `suhagocer/Deneme`’ye yazdığı iddiası doğrulanmadı.

**Bu turda radar notu:** Dört panel URL’si yenilendi (A1–A4); A6 aynı URL’de uzadı. Mimari karar listesi ve karar günlüğü değişmedi. Yeni OSS adayı yok.

## Paylaşım güncellemesi — 2026-10-06 (sabah kontrol)

| Kaynak | Fetch | Özet farkı |
|--------|-------|------------|
| A1 ChatGPT `6ac43f6c-…` | curl (HTML içi akış JSON) | Değişmedi: 1.090 düğüm yolu, görünen 252 mesaj; kimlik + metin birebir aynı. |
| A2 Gemini `2e9F8…` → `ed8f5044c1cc` | browser (alt ajan) | Değişmedi: yayın 2026-10-06 03:24, 87.128 karakter; son tur aynı (“Faz 0 Başarıyla Kapatıldı, Faz 1 … Başlıyor”). |
| A3 DeepSeek `nkfqofqcbfip0vlc94` | curl (`/api/v0/share/content`) | Değişmedi: ham 406.949 bayt, öncekiyle bit eş. |
| A4 Grok `c2hhcmQtMg_e6ce9fde-…` | curl JSON uç noktası | Değişmedi: 62 yanıt, metin aynı. Yalnız `modifyTime` (06:17Z) ve sandbox önizleme adresi değişti. |
| A5 flame-sage | curl OK | **Değişiklik:** `/tur-17`…`/tur-26` açıldı (v1.20–v1.29, hepsi 6 Eki). `/tur-27` ve sonrası 404. `/tur-16` metni aynı (yalnız menü). |
| A6 Claude `1c1203ca-…` | browser (alt ajan) | Değişmedi: son mesaj aynı (`0ddddfe` sorusu, “7 saat önce”); sayfa ~37.313 karakter, fark kenar çubuğu / göreli zaman. |
| E1 / E3 ChatGPT | curl (HTML içi akış JSON) | Değişmedi (541 / 46 mesaj, metin aynı). |
| E2 Claude v3 | — | Bu turda kontrol edilmedi (önceki turlarda değişmedi). |

**flame-sage Tur 17–26 (v1.20–v1.29, 6 Eki, Grok okuyucu, “kanon değildir”):**

- Tur 17 “İkinci paket”: Claude v2 bu sohbette 18/18; kira bitişte boş ama olay yazılmıyor; kopyada `family_verified` varsayılanı `True`; “Bu paket repodaki store.py değil”; ChatGPT ve Gemini’nin Faz 1 isteğine “Geçilmez”.
- Tur 18 “Elçi”: ad Suha; `0ddddfe` altındaki not bölümünü özetliyor; Claude depo iznini alamadı, yalnız tablo hücresini gördü; “Grok o release_lease’i yazmadı”; “Gemini Flash bağlanmaz”.
- Tur 19 “Düzeltme”: Claude v3 20/20 ama iki yeni test yazma yolunu kanıtlamıyor; kira hâlâ olay yazmıyor; 6 Ekim satırı `bb55155`, eski satır duruyor.
- Tur 20 “v4”: v4 21/21, kira artık `lease.acquire/release/expire` olayı yazıyor; `family_verified` hâlâ `True`; ChatGPT/Gemini/DeepSeek’in “20/20 mührü” bu düzeltmeden önce yazılmış; “Oy çokluğu mühür değil”.
- Tur 21 “v5”: v5 22/22, eksik `family_verified` artık `False`; aynı ailede `can_write_verified` hâlâ `True`; v5 `store.py` sha256 `51598b5f`.
- Tur 22 “Hash”: v6 23/23, kapı artık yalnız verified; dosyalar eşit değil (v6 `store.py` `80d23825`, 19.023 bayt; repo `906b9581`, 8.873 bayt).
- Tur 23 “Eşit değil”: dört dosyanın tam sha256’ları; hiçbiri v6 ile aynı değil; “Üzerine yazmak çekirdeği siler”.
- Tur 24 “İki program”: “Claude üzerine yazmayı geri çekti. Replace yok.”; ChatGPT’nin `292026c` / `80f8b172` değerleri git blob SHA-1, dosya sha256 değil.
- Tur 25 “Sayım”: test hash’i 64 karakter, 62 değil; “Claude bu tur tersine döndü”, ChatGPT/Gemini/DeepSeek üzerine yazmama diyor.
- Tur 26 “Kırık”: v6 `run_mission.py` main `store.py` ile koşunca ilk görevde kırıldı (`model_class` yok, çekirdekte `model_id`; `release_lease` yok); “Altı dosya eklenmedi”; Faz 0 kapanmadı.

**Repo kontrolü (main, bu tur):** Grok’un sayıları main ile tutuyor. `store.py` sha256 `906b9581…`, 8.873 bayt (git blob `292026c`, değişmedi); `test_faz0.py` sha256 `34b0a2c0…` (64 karakter), 15 test (blob `80f8b17`); `context_builder.py` sha256 `3ac9b248…`; `run_mission.py` 404. `store.py`’de `release_lease` metodu yok; `lease.acquire` / `lease.release` olayları var (`lease.release` `expire_leases` içinden); `family_verified` varsayılanı `False`; `can_write_verified` = `evaluate_verification(...) == "verified"`; ajan alanı `model_id`. Karar günlüğüne `bb55155` (2026-10-06T03:14Z) ile “2026-10-06 — Düzeltme” satırı eklendi; sahibi “Grok. Not a panel stamp.”; 3 Ekim satırı duruyor.

**Modeller arası ayrışma (gözlem):** Grok Tur 17–26’ya göre ChatGPT, Gemini ve DeepSeek Claude paketini 20/20 ile onaylamış, sonra üçü de üzerine yazmaya karşı çıkmış; Claude üzerine yazmayı önce geri çekmiş, Tur 25’e göre tekrar istemiş. Bu turlar A1/A3/A4 paylaşımlarına henüz yansımadı (o linkler değişmedi), yani yalnız Grok’un aktarımı.

**Bu turda radar notu:** Mimari karar listesi değişmedi. Doğrulanmış farklar: flame-sage Tur 17–26 yayında, karar günlüğüne `bb55155` ek satırı geldi. v2–v6 paketlerinin hiçbiri main’e yazılmadı. Yeni OSS adayı yok.

## Paylaşım güncellemesi — 2026-10-06 (öğleden sonra kontrol)

| Kaynak | Fetch | Özet farkı |
|--------|-------|------------|
| A1 ChatGPT `6ac43f6c-…` | curl (HTML içi akış JSON) | Değişmedi: 1.090 düğüm yolu, görünen 252 mesaj; kimlik + metin birebir aynı. |
| A2 Gemini `OfxANwjNxbQc` → `318c86ecfe20` | browser (alt ajan) | **Değişiklik (ilk içerik okuması):** aynı “agent world” sohbeti uzamış; yayın 2026-10-06 06:17 (önceki `ed8f…` 03:24); ~87.128 → ~89.900 karakter. “Faz 0 Başarıyla Kapatıldı, Faz 1 (Gerçek LLM Entegrasyonu) Başlıyor” turundan sonra tek yeni tur var (kullanıcı “Gel.son.modeller” dosyası + “Yeni dosya”). Sayfada görünen kısa link `tE7dlQK7I3vg` (kullanıcı vermedi; yalnız provenance). |
| A3 DeepSeek `nkfqofqcbfip0vlc94` | curl (`/api/v0/share/content`) | Değişmedi: 54 mesaj; fark yalnız imzalı dosya adreslerinde (`signed_path`). |
| A4 Grok `c2hhcmQtMg_e6ce9fde-…` | curl JSON uç noktası | Değişmedi: 62 yanıt, kimlik + metin aynı. Yalnız `modifyTime` (08:31Z) değişti. |
| A5 flame-sage | curl OK | **Değişiklik:** `/tur-27` açıldı (v1.30 “Koşu”, 6 Eki). `/tur-28`…`/tur-40` 404. |
| A6 Claude `1c1203ca-…` | browser (alt ajan) | Değişmedi: son mesaj aynı (`0ddddfe` sorusu, artık “14 saat önce”); ~37.300 karakter. |
| E1 / E3 ChatGPT | curl (HTML içi akış JSON) | Değişmedi (541 / 46 mesaj, metin aynı). |
| E2 Claude v3 | browser (alt ajan) | Değişmedi: 2 tur, ~4.000 karakter, son mesaj 12 Eyl (“Agent world v3 kanonik”). |

**Gemini yeni tur (Gemini iddiası, karar değildir):** “run_mission.py ile 18/18 test başarıyla geçildi … Faz 0 artık teknik olarak mühürlenmiştir.”; `0ddddfe` satırı için Claude ve DeepSeek’in “append-only” düzeltme önerisini destekliyor; Panel Elçisi için önerdiği mesajda “Grok/Gözcü Bot, DECISION-LOG.md dosyasına şu açıklayıcı satırı ‘append’ (ekle) olarak girsin: ‘2026-10-06 | Korunan Omurga Detayı | 6 İlke kilitlendi … (4) Lease+timeout (Heartbeat yok) … | Panel Onayı’” ve ardından Faz 1 (Model Router, LLM adaptörleri, Gemini Flash) diyor. Bir önceki turda model adlarının `store.agents → model_class`’tan okunduğunu ve `store.release_lease()` çağrıldığını söylüyor. Gözcü `decisions/`’a yazmaz; netleştirme panel notları madde 15’te.

**flame-sage Tur 27 “Koşu” (v1.30, 6 Eki, Grok okuyucu, “kanon değildir”):** “Ana dal 24/24 ve görev betiği çalışıyor. Zip’teki store ana dal değil. Yüzde 66,7 yer tutucu. Faz 1 yok.”; `run_mission.py` “4 doğrulanmış, 2 itiraz, 39 olay, zincir sağlam, kira sonunda boş”; “Commit e67424d. store.py hâlâ 906b9581, 8873 bayt. Bu tur ben yazmadım.”; zip `store.py` `ec9a398b`, 8.234 bayt, “Ana dal değil”; zip testi eski v6, “release_lease yok diye suite kırılıyor”; “İsim testi hâlâ metod adına bakıyor. 24/24 bunu kapatmaz.”

**Repo kontrolü (main `1724ddf`, bu tur):** Tur 27 sayıları main ile tutuyor: `store.py` sha256 `906b9581…`, 8.873 bayt, `release_lease` yok; `test_faz0.py` 24 test, yerel `python3 test_faz0.py` → “24/24 geçti”; `python3 run_mission.py` → 4 verified, 2 disputed, 39 olay, `verify_chain` SAĞLAM, 360 → 120 token (“66.7% düşüş”, sabit kodlu). Main’de `model_class` yok, alan `model_id`. Karar günlüğünde `bb55155` “2026-10-06 — Düzeltme” satırı duruyor (“Heartbeat is not implemented … Faz 0 is not closed”, sahibi “Grok. Not a panel stamp.”).

**Modeller arası ayrışma (gözlem):** Gemini (06:17 yayını) Faz 0’ı 18/18 ile “mühürlenmiş” sayıyor ve Faz 1’e geçmek istiyor; Grok Tur 27 main’de 24/24’ü doğruluyor ama Faz 0’ın kapanmadığını, %66,7’nin yer tutucu olduğunu söylüyor. Gemini’nin 18/18’i repo dışı paketten; main’de 24 test var. İkisi de heartbeat olmadığında ve `0ddddfe`’nin silinmeyip üstüne ek satır yazılmasında aynı yerde.

**Bu turda radar notu:** Mimari karar listesi değişmedi. Doğrulanmış farklar: Gemini kanonik linkinin ilk içerik okuması (bir yeni tur) ve flame-sage Tur 27. Yeni OSS adayı yok.

## Paylaşım güncellemesi — 2026-10-07 (gece kontrol)

| Kaynak | Fetch | Özet farkı |
|--------|-------|------------|
| A1 ChatGPT `6ac43f6c-…` | curl (HTML içi akış JSON) | Değişmedi: 1.090 mesaj, kimlik + metin aynı. |
| A2 Gemini `OfxANwjNxbQc` → `318c86ecfe20` | browser (alt ajan) | Değişmedi: yayın hâlâ 2026-10-06 06:17, son tur yine 18/18 “Faz 0 mühürlendi”; ~89.400 karakter. Sayfadaki kısa link bu kez `AI209QlOku6h` (önce `tE7dlQK7I3vg`, `bPeIBqWXSCpC`; kullanıcı vermedi, yalnız provenance). |
| A3 DeepSeek `nkfqofqcbfip0vlc94` | curl (`/api/v0/share/content`) | Değişmedi: 54 mesaj; fark yalnız `signed_path`. |
| A4 Grok `c2hhcmQtMg_e6ce9fde-…` | curl JSON uç noktası | Değişmedi: 62 yanıt; `modifyTime`/`previewUrl` dışında aynı. |
| A5 flame-sage | curl OK | **Değişiklik:** `/tur-28` açıldı (v1.31 “Ajan — Grok”, 6 Eki). `/tur-29`…`/tur-45` 404. |
| A6 Claude `1c1203ca-…` | browser (alt ajan) | Değişmedi: ~37.300 karakter, son mesaj yine `0ddddfe` sorusu. |
| E1 / E3 ChatGPT | curl (HTML içi akış JSON) | Değişmedi (541 / 46 mesaj, metin aynı). |
| E2 Claude v3 | browser (alt ajan) | Değişmedi: 2 tur, ~4.000 karakter. |

**flame-sage Tur 28 “Ajan” (v1.31, 6 Eki, Grok, “kanon değildir”):** Suha’nın “ajan bir dil modeline bağlı olmak zorunda mı” sorusuna cevap: “Ajan bir dil modeline bağlı olmak zorunda değil. Öğrenme henüz yok. Kapanış satırı yazılmadı. Faz 1 yok.”; “Model, çağrılabilen bir araçtır. Çağrılmayabilir.”; “Faz 0 zaten kural ajanıdır. Araştırmacı, eleştirmen ve doğrulayıcı bir dil modeline sormadan olay yazar.”; “Kendi kendini geliştirmek, ölçülen bir kuralın kalması ya da atılması demektir. Şu anki 360’tan 120’ye iniş bunu değildir. Bayrak elde açılmış bir yer tutucudur.”; “Ana dal duruyor. store.py 906b9581. Test 24/24. Görev betiği çalışıyor. … Kapanış satırı yazılmadı. Faz 1 açılmadı. Zip yazılmadı.”

**Repo kontrolü (main `3d3749f`, bu tur):** Tur 28 iddiaları main ile tutuyor: `store.py` sha256 `906b9581…`, 8.873 bayt, `release_lease` yok; yerel `python3 test_faz0.py` → “24/24 geçti. LLM yok. Postgres yok.”; `python3 run_mission.py` → 4 verified/verified-weak, 2 disputed, 39 olay, `verify_chain` SAĞLAM, 360 → 120 token (sabit kodlu “66.7% düşüş”). `decisions/DECISION-LOG.md`’de Faz 0 kapanış satırı yok; son satır hâlâ `bb55155` “2026-10-06 — Düzeltme” (“Faz 0 is not closed”). Ajanların LLM çağırmadığı doğru: `agents/` kural tabanlı.

**Modeller arası ayrışma (gözlem):** Değişmedi. Gemini (06:17) Faz 0’ı “mühürlenmiş” sayıp Faz 1’e (LLM adaptörleri) geçmek istiyor; Grok Tur 27–28 Faz 0’ın kapanmadığını, %66,7’nin yer tutucu olduğunu ve ajanın modele bağlı olmak zorunda olmadığını söylüyor. Tur 28’in “model bir araçtır” çerçevesi radardaki (1) deterministik çekirdek / (2) ajan çalışma zamanı ayrımıyla uyumlu (Policy→Action→Validation; LLM durumu yazmaz).

**Bu turda radar notu:** Mimari karar listesi değişmedi. Tek doğrulanmış fark flame-sage Tur 28. Yeni OSS adayı yok.

## Paylaşım güncellemesi — 2026-10-07 (öğleden sonra kontrol)

| Kaynak | Fetch | Özet farkı |
|--------|-------|------------|
| A1 ChatGPT `6ac43f6c-…` | curl (HTML içi akış JSON) | Değişmedi: 1.090 mesaj, kimlik + metin aynı. |
| A2 Gemini `OfxANwjNxbQc` → `318c86ecfe20` | browser (alt ajan) | Değişmedi: yayın hâlâ 2026-10-06 06:17, son tur yine 18/18 “Faz 0 mühürlendi” / “Panel Onayı” önerisi; ~91.000 karakter (fark yalnız sayfa altbilgisi). Sayfadaki kısa link bu kez `JqROle31UZhw` (kullanıcı vermedi, yalnız provenance). |
| A3 DeepSeek `nkfqofqcbfip0vlc94` | curl (`/api/v0/share/content`) | Değişmedi: 54 mesaj; fark yalnız `signed_path`. |
| A4 Grok `c2hhcmQtMg_e6ce9fde-…` | curl JSON uç noktası | Değişmedi: 62 yanıt; yalnız `modifyTime` (2026-10-07 12:26Z) değişti. |
| A5 flame-sage | curl OK | **Değişiklik:** `/tur-29` açıldı (v1.32 “Şart — Grok”, 7 Eki). `/tur-30`…`/tur-45` 404. `/tur-27`–`/tur-28` metni aynı (yalnız menü). |
| A6 Claude `1c1203ca-…` | browser (alt ajan) | Değişmedi: son mesaj yine `0ddddfe` / append önerisi (“2 gün önce”); ~38.000 karakter, fark kenar çubuğu. |
| E1 / E3 ChatGPT | curl (HTML içi akış JSON) | Değişmedi (541 / 46 mesaj, metin aynı). |
| E2 Claude v3 | browser (alt ajan) | Değişmedi: 2 tur, son mesaj 12 Eyl (“Agent world v3 kanonik”). |

**flame-sage Tur 29 “Şart” (v1.32, 7 Eki, Grok, “kanon değildir”):** “Kapanış yazıldı, kapı açılmadı”; “Faz 0 kural çekirdeği olarak kapandı. API yok. Faz 1a yazılmadı. Ad Suha.”; “Karar günlüğüne 7 Ekim satırı eklendi. Eski satırlar duruyor.”; “3 Ekim’deki 15/15 silinmedi. O gün doğruydu. README artık 24/24 der.”; “120 ve 40 sayısına yer tutucu yazıldı. Yüzde ölçülmüş token değildir.”; “store.py değişmedi.” Sonrası için: takılıp çıkarılan beyin, ilk beyin kural, testte sahte model; ücretsiz API sonra ve ayrı onayla (ana sağlayıcı Groq, yedek Gemini, tek rol, model dünyayı yazmaz, anahtar repoda yok, Gemini’ye gizli veri gitmez, ücretli API yeni onayla).

**Repo kontrolü (main `8922f6a`, bu tur):** Tur 29 iddiaları main ile tutuyor. 2026-10-07 12:25Z’de suhagocer dört commit attı: [`6878049`](https://github.com/suhagocer/agent-world/commit/6878049) (`agents/researcher.py`’ye “Yer tutucu. Ölçülmüş LLM token değildir.” yorumu), [`20d4a95`](https://github.com/suhagocer/agent-world/commit/20d4a95) (README “Beklenen: `24/24 geçti`”), [`98e4797`](https://github.com/suhagocer/agent-world/commit/98e4797) (`run_mission.py` çıktısı artık “yer tutucu, ölçülmüş LLM token değil” diyor), [`8922f6a`](https://github.com/suhagocer/agent-world/commit/8922f6a) (`decisions/DECISION-LOG.md`’ye “2026-10-07 | Faz 0 kapanışı” satırı ve notu; sahibi “Suha ordered. Grok wrote. Not a panel stamp.”; 3 Ekim ve 6 Ekim satırları duruyor). `store.py` değişmedi (sha256 `906b9581…`, son commit `a1f9ee7`). Yerel koşu: `python3 test_faz0.py` → “24/24 geçti. LLM yok. Postgres yok.”; `python3 run_mission.py` → 4 verified/verified-weak, 2 disputed, 39 olay, `verify_chain` SAĞLAM, 360 → 120 (“66.7% düşüş, yer tutucu, ölçülmüş LLM token değil”). Kayıtta Faz 1a yazılmadı, Faz 1b koşmuyor, API yok.

**Modeller arası ayrışma (gözlem):** Faz 0 kapanışı artık karar günlüğünde, ama Gemini’nin (06:17) önerdiği biçimde değil: Gemini “18/18 … mühürlendi”, “Panel Onayı” satırı ve hemen ardından Faz 1 (Model Router, LLM adaptörleri) istiyordu; yazılan satır 24/24’e dayanıyor, kendini “Not a panel stamp” diye işaretliyor ve “A line that opens Faz 1 Model Router immediately” seçeneğini reddediyor. ChatGPT/DeepSeek’in Faz 0 kapandı görüşüyle sonuçta aynı, ama gerekçe (main 24/24, %66,7 yer tutucu) Grok Tur 27–29 çizgisinde. Diğer panel paylaşımları (A1/A3/A4) bu satırdan önce kaldı; henüz kimse yorumlamadı. Tur 29’daki “takılıp çıkarılan beyin, ilk beyin kural” çerçevesi radardaki (1) deterministik çekirdek / (2) ajan çalışma zamanı ayrımıyla uyumlu (LLM durumu yazmaz).

**Bu turda radar notu:** Doğrulanmış farklar: flame-sage Tur 29 ve main’de Faz 0 kapanış satırı (`8922f6a`). Radardaki mimari karar listesi değişmedi. Yeni OSS adayı yok.

## Paylaşım güncellemesi — 2026-10-10 (gece kontrol)

| Kaynak | Fetch | Özet farkı |
|--------|-------|------------|
| A1 ChatGPT `6ac43f6c-…` | curl (HTML içi akış JSON) | Değişmedi: kimlik + metin aynı (1.090 mesaj). |
| A2 Gemini `OfxANwjNxbQc` → `318c86ecfe20` | browser (alt ajan) | Değişmedi: yayın hâlâ 2026-10-06 06:17, son tur yine “Yeni dosya” / 18/18 “Faz 0 mühürlendi” / “Panel Onayı” önerisi; ~86.000 karakter (fark sayfa etiketleri). Sayfadaki kısa link bu kez `o6PsvGshj8E7` (kullanıcı vermedi, yalnız provenance). |
| A3 DeepSeek `nkfqofqcbfip0vlc94` | curl (`/api/v0/share/content`) | Değişmedi: 54 mesaj; fark yalnız `signed_path`. |
| A4 Grok `c2hhcmQtMg_e6ce9fde-…` | curl JSON uç noktası | Değişmedi: 62 yanıt, metin aynı; yalnız `modifyTime` (2026-10-10 01:28Z) değişti. |
| A5 flame-sage | curl OK | **Değişiklik:** `/tur-30` (v1.33 “Dilim”) ve `/tur-31` (v1.34 “Koşu”) açıldı, ikisi de 10 Eki. `/tur-32`…`/tur-40` 404. `/tur-29` metni aynı (yalnız menü). |
| A6 Claude `1c1203ca-…` | browser (alt ajan) | Değişmedi: son mesaj yine `0ddddfe` / append önerisi (“4 gün önce”); ~33.400 karakter (kenar çubuğu hariç okundu). |
| E1 / E3 ChatGPT | curl (HTML içi akış JSON) | Değişmedi (541 / 46 mesaj, metin aynı). |
| E2 Claude v3 | browser (alt ajan) | Değişmedi: 2 tur, son mesaj 12 Eyl (“Sentezle” → kanonik v3). |

**flame-sage Tur 30 “Dilim” (v1.33, 10 Eki, Grok, “kanon değildir”):** “Dilim koştu, faz kapanmadı”; “Üç dosya ana dalda. 24/24 ve 10/10. Motor yalnız eleştirmende. API yok.”; “Commit 35b8b37. Günlük satırı d3c849b. Zip’in geri kalanı yazılmadı.”; “Araştırmacı ve doğrulayıcı motor almaz.”; “DISPUTE ile başlamayan cevap onay sayılır. Ayrıştırma kapalı değildir.”; “Ağ testi yalnız cognitive_engine.py dosyasına bakar.”; “Faz 1a bitmiş sayılmaz. Faz 1b açılmadı. Groq ve Gemini yok. Ücretli API yok.”

**flame-sage Tur 31 “Koşu” (v1.34, 10 Eki, Grok, “kanon değildir”):** “Ekleme yapılmıştı, açık kapatıldı”; “Bozuk cevap artık onay değil. Boş metin, gerekçesiz PASS ve DISCUSSION itirazdır.”; “test_faz0.py 24/24, test_faz1a.py 12/12.”; “Ağ testi ürün Python dosyalarına bakar. Deponun tamamına bakmaz. Commit baa145f.”; “Kod decide değil. evaluate bir cümle alır, bir hüküm döner. Onu yalnız eleştirmen çağırır.”; “Faz 1a kapanmış sayılmaz. Groq yok. Gemini yok.”

**Repo kontrolü (main `baa145f`, bu tur):** Tur 30 iddiaları [`35b8b37`](https://github.com/suhagocer/agent-world/commit/35b8b37) ağacında tutuyor: `cognitive_engine.py`, `test_faz1a.py` ve yeni `agents/critic.py` eklenmiş; o ağaçta `python3 test_faz1a.py` → “10/10 geçti”; karar günlüğü satırı [`d3c849b`](https://github.com/suhagocer/agent-world/commit/d3c849b) (“2026-10-10 | Faz 1a dosyaları … Not a phase seal … Non-DISPUTE replies pass. Faz 1b stays closed.”). Tur 30’daki “DISPUTE ile başlamayan cevap onay sayılır” ve “ağ testi yalnız cognitive_engine.py” cümleleri artık main’in son hâli değil: [`99a502e`](https://github.com/suhagocer/agent-world/commit/99a502e), [`07fcb04`](https://github.com/suhagocer/agent-world/commit/07fcb04), [`d24d8ca`](https://github.com/suhagocer/agent-world/commit/d24d8ca), [`1d241fe`](https://github.com/suhagocer/agent-world/commit/1d241fe) ile ayrıştırıcı yalnız `PASS: <sebep>` / `DISPUTE: <sebep>` kabul ediyor (`re.fullmatch`), [`baa145f`](https://github.com/suhagocer/agent-world/commit/baa145f) ile `test_no_network_module_exists` artık `cognitive_engine.py`, `store.py`, `context_builder.py`, `run_mission.py` ve `agents/*.py` dosyalarına bakıyor. Tur 31 iddiaları main `baa145f` ile tutuyor. Yerel koşu: `python3 test_faz0.py` → “24/24 geçti”; `python3 test_faz1a.py` → “12/12 geçti. LLM yok. Postgres yok. Ağ çağrısı yok.”; `python3 run_mission.py` → 4 verified/verified-weak, 2 disputed, 39 olay, `verify_chain` SAĞLAM. `store.py` değişmedi (sha256 `906b9581…`). Motoru yalnız `agents/critic.py` çağırıyor (araştırmacı/doğrulayıcı değişmedi). Groq/Gemini istemcisi yok (yalnız yorumlarda Faz 1b’ye atıf). Karar günlüğünde iki yeni 10 Ekim satırı var (“Faz 1a dosyaları”, “Faz 1a fail-closed düzeltmesi”); ikisi de “Not a panel stamp”, Faz 1a’yı kapatmıyor, Faz 1b kapalı.

**Modeller arası ayrışma (gözlem):** Faz 1a’nın ilk dilimi main’de; ayrıştırıcıyı ChatGPT yazmış, Grok koşmuş (günlük satırının sahibi: “ChatGPT wrote the parser. Grok ran it.”). Diğer panel paylaşımları (A1/A3/A4/A6) bu turlardan önce kalıyor; Faz 1a’yı henüz yorumlamadılar. Gemini’nin 6 Ekim’de istediği “hemen Model Router / LLM adaptörleri” yolu hâlâ açılmadı: motor yalnız eleştirmende, gerçek istemci yok. Bu ayrım radardaki (1) deterministik çekirdek / (2) takılıp çıkarılan bilişsel motor ayrımıyla uyumlu (model durumu yazmaz, yalnız bir hüküm döner).

**Bu turda radar notu:** Doğrulanmış farklar: flame-sage Tur 30–31 ve main’de Faz 1a ilk dilimi (`35b8b37` … `baa145f`). Radardaki mimari karar listesi değişmedi. Yeni OSS adayı yok.

## Paylaşım güncellemesi — 2026-10-10 (sabah kontrol)

| Kaynak | Fetch | Özet farkı |
|--------|-------|------------|
| A1 ChatGPT `6ac43f6c-…` | curl (HTML içi akış JSON) | Değişmedi: kimlik + metin aynı. |
| A2 Gemini `OfxANwjNxbQc` → `318c86ecfe20` | browser (alt ajan) | Değişmedi: yayın hâlâ 2026-10-06 06:17, son tur yine “Yeni dosya” / “Panel Elçisi” analizi ve “Panel Onayı” önerisi; ~93.500 karakter (PDF metni; fark sayfa başlıkları). Sayfadaki kısa link bu kez `STAKouqeYeoz` / `64gCxyaUAoEo` (kullanıcı vermedi, yalnız provenance). |
| A3 DeepSeek `nkfqofqcbfip0vlc94` | curl (`/api/v0/share/content`) | Değişmedi: yanıt bayt bayt aynı. |
| A4 Grok `c2hhcmQtMg_e6ce9fde-…` | curl JSON uç noktası | Değişmedi: metin aynı; yalnız `modifyTime` (2026-10-10 02:25Z) ve önizleme durumu değişti. |
| A5 flame-sage | curl OK | **Değişiklik:** `/tur-32` (v1.35 “Koşu”) ve `/tur-33` (v1.36 “Mühür yok”) açıldı, ikisi de 10 Eki. `/tur-34`…`/tur-45` 404. `/tur-31` metni aynı (yalnız menü). |
| A6 Claude `1c1203ca-…` | browser (alt ajan) | Değişmedi: son mesaj yine `0ddddfe` / append itirazı (“4 gün önce”); 12 kullanıcı mesajı. |
| E1 / E3 ChatGPT | curl (HTML içi akış JSON) | Değişmedi (metin aynı). |
| E2 Claude v3 | browser (alt ajan) | Değişmedi: 2 tur, son mesaj 12 Eyl (“Sentezle” → kanonik v3). |

**flame-sage Tur 32 “Koşu” (v1.35, 10 Eki, Grok, “kanon değildir”, kaynak main `fb2b5c4`):** “Koşu bitti, mühür yok”; “Ana dalda 24/24, 12/12 ve görev betiği geçti. Faz 1a kapanmadı. API yok.”; “Görev 4 doğrulanmış, 2 itiraz, 39 olay. store.py değişmedi. Kayıt 42d5f24.”; “Açık ayrıştırma ve tek dosyalık ağ testi artık güncel değil.”; “Faz 1a mührü yazılmadı. Groq yok. Gemini yok. Ücretli API yok.”

**flame-sage Tur 33 “Mühür yok” (v1.36, 10 Eki, Grok, “kanon değildir”, kaynak main `42d5f24`):** “Faz 1a mührü yok. Ağ testi deponun tamamı değil. API yok.”; “Faz 1a kapandı satırı yok. Panel kaşesi yok. Groq yok. Gemini yok. Kayıt 0fd02b0. Kod 42d5f24 ile aynı. 24 ve 12 ayrı koşucu.”; “Ağ testi beş ürün yoluna bakar. Depodaki her .py dosyasına bakmaz.”

**Repo kontrolü (main `0fd02b0`, bu tur):** İki yeni commit var, ikisi de yalnız `decisions/DECISION-LOG.md`: [`42d5f24`](https://github.com/suhagocer/agent-world/commit/42d5f24) (“Record the Faz 1a run. Do not seal the phase.”, 01:56Z; satır “2026-10-10 | Faz 1a koşu … Not a Faz 1a seal … Faz 1b does not start. | Grok ran it. Not a panel stamp.”) ve [`0fd02b0`](https://github.com/suhagocer/agent-world/commit/0fd02b0) (“Reject a Faz 1a seal. No API client.”, 02:25Z; satır “2026-10-10 | Mühür yok … | Grok. Not a panel stamp.”). Kod `baa145f`’ten beri değişmedi. Tur 32–33 iddiaları main ile tutuyor. Yerel koşu (main `0fd02b0`): `python3 test_faz0.py` → “24/24 geçti”; `python3 test_faz1a.py` → “12/12 geçti. LLM yok. Postgres yok. Ağ çağrısı yok.”; `python3 run_mission.py` → 4 verified/verified-weak, 2 disputed, 39 olay, `verify_chain` SAĞLAM; 360→120 token hâlâ “yer tutucu”. `store.py` sha256 `906b9581…`, değişmedi. `test_no_network_module_exists` tam olarak beş yola bakıyor: `cognitive_engine.py`, `store.py`, `context_builder.py`, `run_mission.py`, `agents/*.py` (kod yorumu: “Bu, deponun tamamı değildir.”). Groq/Gemini istemcisi yok.

**Modeller arası ayrışma (gözlem):** Günlük, Faz 1a’yı mühürleme isteğini açıkça reddediyor (“Rejected. A row that says Faz 1a is closed. A panel stamp. …”); 42d5f24 notuna göre tam koşuyu ChatGPT istemiş, Grok koşmuş. Gemini’nin 6 Ekim’deki “hemen Model Router / LLM adaptörleri” isteği hâlâ açılmadı; diğer panel paylaşımları (A1/A3/A4/A6) bu turlardan önce kalıyor.

**Bu turda radar notu:** Doğrulanmış farklar: flame-sage Tur 32–33 ve main’de iki günlük satırı (`42d5f24`, `0fd02b0`). Radardaki mimari karar listesi değişmedi. Yeni OSS adayı yok.

## Paylaşım güncellemesi — 2026-10-10 (öğleden sonra kontrol)

| Kaynak | Fetch | Özet farkı |
|--------|-------|------------|
| A1 ChatGPT `6ac43f6c-…` | curl (HTML içi akış JSON) | Değişmedi: kimlik + metin aynı. |
| A2 Gemini `OfxANwjNxbQc` → `318c86ecfe20` | browser (alt ajan) | Değişmedi: yayın hâlâ 2026-10-06 06:17, son tur yine “Yeni dosya” / “Panel Elçisi” analizi ve “Panel Onayı” önerisi; 33 kullanıcı turu. Sayfadaki kısa link bu kez `HhIPNmImuFB3` (kullanıcı vermedi, yalnız provenance). |
| A3 DeepSeek `nkfqofqcbfip0vlc94` | curl (`/api/v0/share/content`) | Değişmedi: 54 mesaj; fark yalnız `signed_path`. |
| A4 Grok `c2hhcmQtMg_e6ce9fde-…` | curl JSON uç noktası | Değişmedi: metin aynı; yalnız `workspacePreviewState` (served → gone) değişti. |
| A5 flame-sage | curl OK | **Değişiklik:** `/tur-34` (v1.37 “Devam”, 10 Eki) açıldı. `/tur-35`…`/tur-48` 404. `/tur-33` ve kök sayfa metni aynı (yalnız menüye v1.37 eklendi). |
| A6 Claude `1c1203ca-…` | browser (alt ajan) | Değişmedi: son mesaj yine `0ddddfe` / append itirazı (“5 gün önce”); 12 kullanıcı mesajı. |
| E1 / E3 ChatGPT | curl (HTML içi akış JSON) | Değişmedi (metin aynı). |
| E2 Claude v3 | browser (alt ajan) | Değişmedi: 2 tur, son mesaj 12 Eyl (“Sentezle” → kanonik v3). |

**flame-sage Tur 34 “Devam” (v1.37, 10 Eki, Grok, “kanon değildir”):** “Ortak kapanış yok. 24/24 ve 14/14. Doğrulayıcı dünya kapısı. API yok.”; “Bitmedi diyen var. Mühür yazılmadı.”; “Araştırmacı artık isteğe bağlı bir çıkarıcı alır. Varsayılan, eski FACT kuralıdır. Çıkarıcı store almaz. Doğrulayıcı dünya kapısıdır. Ona motor verilmedi.”; “Görev aynı: 4 doğrulanmış, 2 itiraz, 39 olay. Commit bd62ff9.”; “API istemcisi yok. Anahtar repoda yok. Faz 1b açılmadı.”

**Repo kontrolü (main `bd62ff9`, bu tur):** Yeni kod commit’i [`bd62ff9`](https://github.com/suhagocer/agent-world/commit/bd62ff9) (“Add an optional researcher extractor. Do not seal Faz 1a.”, 08:02Z): `agents/researcher.py` (+`FactExtractor` Protocol, varsayılan `RuleBasedFactExtractor` “rule-extract-v1”; `run_researcher(..., extractor=None)`), `test_faz1a.py` (+`test_default_extractor_matches_rule`, `test_extractor_cannot_write_store`) ve `decisions/DECISION-LOG.md` (satır “2026-10-10 | Devam | No joint close. … 24/24 and 14/14. No API. No key in the repo. | Suha: continue if not joint. Grok wrote. Not a panel stamp.”). Tur 34 iddiaları main ile tutuyor. Yerel koşu: `python3 test_faz0.py` → “24/24 geçti”; `python3 test_faz1a.py` → “14/14 geçti. LLM yok. Postgres yok. Ağ çağrısı yok.”; `python3 run_mission.py` → 4 verified/verified-weak, 2 disputed, 39 olay, `verify_chain` SAĞLAM; 360→120 token hâlâ “yer tutucu”. `store.py` sha256 `906b9581…`, değişmedi. `agents/verifier.py` motor almıyor. Beş ürün yolunda ağ/HTTP içe aktarması yok; Groq/Gemini istemcisi yok; depoda anahtar deseni bulunmadı.

**Modeller arası ayrışma (gözlem):** Günlüğe göre Suha “ortak değilse devam” dedi; Faz 1a mührü yine yazılmadı. Gemini’nin 6 Ekim’deki “hemen Model Router / LLM adaptörleri” isteği hâlâ açılmadı; diğer panel paylaşımları (A1/A3/A4/A6) bu turdan önce kalıyor.

**Bu turda radar notu:** Doğrulanmış farklar: flame-sage Tur 34 ve main’de `bd62ff9` (isteğe bağlı çıkarıcı + 2 test + günlük satırı). Radardaki mimari karar listesi değişmedi. Yeni OSS adayı yok.

## Günlük / dönemsel notlar

_(Repo Gözcüsü yeni taramaları buraya ekler.)_

- **2026-10-01:** Dosya oluşturuldu. ChatGPT paylaşım özeti ve 8 parçalı referans haritası seed olarak eklendi.
- **2026-10-01 (akşam):** Yetki genişletmesi onaylandı (yalnızca bu dosya). “Sonraki tarama hedefi” bölümü eklendi.
- **2026-10-02:** Sekiz AI sohbet özeti, ortak kararlar ve Faz 0 eşlemesi eklendi.
- **2026-10-02 (gece):** Tam URL’ler; Grok + araçlar + Gemini/DeepSeek/Claude browser doğrulandı; lisans tablosu.
- **2026-10-02 (gece++++):** Ana panel vs ekstra; Gemini `rbdXhpeLoM5J` (eskiyle aynı sohbet).
- **2026-10-02 (gece+++++):** Gemini kanonik kısa URL → `1tuZ3H4PH5af` / `d272dd7f8df1` (yine aynı sohbet).
- **2026-10-02 (öğle):** Paylaşım yeniden fetch. A1 tam metin OK; flame-sage tur 9–12 404; Gemini `TXv3…` aynı `d272dd…`. Mimari digest değişmedi.
- **2026-10-05 (gece):** Repo `0ddddfe`: korunan omurga `decisions/DECISION-LOG.md`’ye işlendi (karar kaydı orası, radar değil). flame-sage Tur 9–14 yeniden açık; özetleri eklendi. Diğer paylaşımlar değişmedi. Yeni OSS yok.
- **2026-10-05 (gece+):** Kullanıcı kuralı: yeni paylaşım URL’si içerik aynı olsa bile kanonik olur. A3 DeepSeek → `japybl2d3ejtr7ch0i` (eski `wcnvcw1…` değiştirildi).
- **2026-10-05 (gece++):** A3 DeepSeek kanonik URL → `ulwkayx5qsy0otx8vd` (önceki `japybl2d3ejtr7ch0i` değiştirildi). Paylaşım daha kısa; transkript aynı değil. Karar listesi değişmedi.
- **2026-10-05 (gece+++):** A3 DeepSeek kanonik URL → `wfbt7ngfw6r7f8whwq` (önceki `ulwkayx5qsy0otx8vd`; `japybl…` / `wcnvcw…` yalnızca provenance). İçerik `ulwkay…` ile aynı değil (heartbeat düzeltmesi iddiası). Karar listesi değişmedi.
- **2026-10-05 (akşam):** Tam paylaşım kontrolü. flame-sage `/tur-15` açıldı (v1.18 “Yan kopya”: Claude kopyası 16/16 ama fail-open farklar; `store.py` değişmez). Diğer tüm linkler değişmedi (Gemini/Claude browser ile doğrulandı). Karar listesi değişmedi. Yeni OSS yok.
- **2026-10-05/06 (gece):** Tam paylaşım kontrolü (Gemini browser üst ajan: değişmedi). flame-sage `/tur-16` açıldı (v1.19 “Aynı koşu”: 16/16 yeniden; heartbeat/günlük/store değişmez). Diğer curl linkleri değişmedi; Claude yalnızca kabuk. Karar listesi değişmedi. Yeni OSS yok.
- **2026-10-06:** Panel URL güncellemesi: A1 ChatGPT → `6ac43f6c-…` (eski `6aa7584b-…` silinmiş), A2 Gemini → `2e9F8…`/`ed8f5044c1cc`, A3 DeepSeek → `nkfqofqcbfip0vlc94`, A4 Grok → `c2hhcmQtMg_e6ce9fde-…`; dördü de aynı sohbetin uzamış hâli. A6 Claude aynı URL’de yeni turlar. Faz 0 kapanışı konusunda modeller ayrışıyor (gözlem); repo `main` 15 test, karar günlüğü `0ddddfe`. Karar listesi değişmedi. Yeni OSS yok.
- **2026-10-06 (sabah):** flame-sage `/tur-17`…`/tur-26` açıldı (v1.20–v1.29: Claude v2–v6 kopyaları 18/18…23/23, hiçbiri main değil; `run_mission.py` main’de kırılıyor; replace yok; Faz 0 açık). Karar günlüğü `bb55155` ek satırı. A1/A3/A4/E1/E3 değişmedi. Karar listesi değişmedi. Yeni OSS yok.
- **2026-10-06 (sabah+):** Kullanıcı A2 Gemini için yeni paylaşım linki verdi: `OfxANwjNxbQc` → `318c86ecfe20` (curl yönlendirmesi). Kalıcı kural gereği kanonik oldu; önceki `2e9F8NNsviiG` → `ed8f5044c1cc` yalnızca provenance. İçerik kontrolü bir sonraki browser okumasını bekliyor (curl gövdesi yalnızca kabuk). Panel Elçisi bildirimi (doğrulanmadı): Tur 18 aktarımı beş modele 03:10–03:20 UTC arasında gönderildi.
- **2026-10-06 (öğleden sonra):** A2 Gemini `OfxANwjNxbQc` → `318c86ecfe20` browser ile okundu: aynı sohbet, yayın 06:17, bir yeni tur (18/18 ile “Faz 0 mühürlendi”, Gözcü’ye DECISION-LOG append önerisi; panel notları madde 15). flame-sage `/tur-27` açıldı (v1.30: main 24/24, zip store ana dal değil, %66,7 yer tutucu, Faz 1 yok). A1/A3/A4/A6/E1/E2/E3 değişmedi. Karar listesi değişmedi. Yeni OSS yok.
- **2026-10-07 (gece):** flame-sage `/tur-28` açıldı (v1.31 “Ajan”: ajan modele bağlı olmak zorunda değil; main 24/24, `store.py` `906b9581`, kapanış satırı yok, Faz 1 yok; main ile doğrulandı). Gemini sayfa kısa linki `AI209QlOku6h` (yalnız provenance). A1/A2/A3/A4/A6/E1/E2/E3 içerik olarak değişmedi. Karar listesi değişmedi. Yeni OSS yok.
- **2026-10-07 (öğleden sonra):** flame-sage `/tur-29` açıldı (v1.32 “Şart”: Faz 0 kural çekirdeği olarak kapandı, API yok, Faz 1a yok). Main `8922f6a` ile doğrulandı: karar günlüğüne “2026-10-07 | Faz 0 kapanışı” satırı (sahibi “Suha ordered. Grok wrote. Not a panel stamp.”), README 24/24, %66,7 kodda “yer tutucu”; `store.py` değişmedi. Gemini sayfa kısa linki `JqROle31UZhw` (yalnız provenance). A1/A2/A3/A4/A6/E1/E2/E3 içerik olarak değişmedi. Karar listesi değişmedi. Yeni OSS yok.
- **2026-10-10 (gece):** flame-sage `/tur-30` (v1.33 “Dilim”) ve `/tur-31` (v1.34 “Koşu”) açıldı. Main `baa145f` ile doğrulandı: Faz 1a ilk dilimi (`35b8b37`: `cognitive_engine.py`, `test_faz1a.py`, `agents/critic.py`), fail-closed ayrıştırıcı (`99a502e`…`1d241fe`), ağ testi ürün dosyalarında (`baa145f`); 24/24 ve 12/12; `store.py` değişmedi; Groq/Gemini yok; günlükte iki 10 Ekim satırı (“Not a panel stamp”). Tur 30’daki fail-open cümlesi artık main’in son hâli değil. Gemini sayfa kısa linki `o6PsvGshj8E7` (yalnız provenance). A1/A2/A3/A4/A6/E1/E2/E3 içerik olarak değişmedi. Karar listesi değişmedi. Yeni OSS yok.
- **2026-10-10 (sabah):** flame-sage `/tur-32` (v1.35 “Koşu”) ve `/tur-33` (v1.36 “Mühür yok”) açıldı. Main `0fd02b0` ile doğrulandı: yalnız iki günlük satırı (`42d5f24` “Faz 1a koşu”, `0fd02b0` “Mühür yok”, ikisi de “Not a panel stamp”); kod `baa145f`’ten beri aynı; 24/24, 12/12, görev 4/2/39; `store.py` değişmedi; ağ testi beş ürün yolu; Groq/Gemini yok. Gemini sayfa kısa linkleri `STAKouqeYeoz` / `64gCxyaUAoEo` (yalnız provenance). A1/A2/A3/A4/A6/E1/E2/E3 içerik olarak değişmedi. Karar listesi değişmedi. Yeni OSS yok.
- **2026-10-10 (öğleden sonra):** flame-sage `/tur-34` (v1.37 “Devam”) açıldı. Main `bd62ff9` ile doğrulandı: araştırmacıya isteğe bağlı `FactExtractor` (varsayılan FACT kuralı, store almaz), `test_faz1a.py` 14/14, 24/24, görev 4/2/39; `store.py` değişmedi; doğrulayıcıya motor verilmedi; Groq/Gemini/anahtar yok; günlük satırı “Devam” (“Not a panel stamp”). Gemini sayfa kısa linki `HhIPNmImuFB3` (yalnız provenance). A1/A2/A3/A4/A6/E1/E2/E3 içerik olarak değişmedi. Karar listesi değişmedi. Yeni OSS yok.

## Kendi kodumuzla ajan sistemleri — araştırma (2026-10-10, karar değildir)

> Repo Gözcüsü araştırma notu. Kararlar yalnızca `decisions/DECISION-LOG.md`'de. Dayanak: main `2d8b222` (Faz 0 kural çekirdeği olarak kapandı, `8922f6a`: "Do not open an API."). Amaç: bağımlılık değil, **desen** almak. Faz 1 burada yalnızca seçenek olarak geçer.
> Tekrar etmemek için: LangGraph, AutoGen/AG2, CrewAI, OpenAI Agents SDK, smolagents, CAMEL, MetaGPT, Letta, Generative Agents, AgentVerse, ChatDev, Voyager, MCP, A2A, event sourcing, aktör modeli ve Gray & Cheriton lease → [`grok-bot-arastirma/2026-10-06_ajan-sistemleri.md`](grok-bot-arastirma/2026-10-06_ajan-sistemleri.md). BDI/HTN/utility, Contract Net, blackboard, itibar, Mesa/NetLogo/Repast, tick/ECS/tohumlu rastgelelik → [`grok-bot-arastirma/2026-10-06_llmsiz-otonom-ajanlar.md`](grok-bot-arastirma/2026-10-06_llmsiz-otonom-ajanlar.md). Aşağıda yalnızca eksik kalanlar var.
> Yıldız/lisans/son push: GitHub API, 2026-10-09 ~23:55 UTC. Makale başlıkları arxiv.org/abs üzerinden doğrulandı.

| # | Kaynak (doğrulandı) | Lisans · ★ · son push | Çekirdek desen | Kendimiz yazalım | Kaçınalım |
|---|---|---|---|---|---|
| 1a | Anthropic, "Building effective agents" (2024-12-19) + [claude-cookbooks/patterns/agents](https://github.com/anthropics/claude-cookbooks/tree/main/patterns/agents) | MIT · 53.3k · 2026-10-09 | Workflow (önceden yazılmış kod yolu) ≠ agent (model süreci yönetir). Beş iş akışı: prompt chaining (+ programatik "gate"), routing, parallelization, orchestrator-workers, evaluator-optimizer. "En basit çözümle başla; çerçeve yerine API'yi doğrudan kullan"; durma koşulu (maks. iterasyon) | Önce **workflow**: `run_mission.py` zaten sabit kod yolu. Gate = `append_event` öncesi kural kontrolü. Evaluator-optimizer = Researcher→Critic döngüsü, iterasyon tavanıyla | Model'e süreç kontrolü vermek (agent modu) Faz 1'in ilk adımı olmamalı |
| 1b | ReAct ([2210.03629](https://arxiv.org/abs/2210.03629), [ysymyth/ReAct](https://github.com/ysymyth/ReAct)) | MIT · 4.2k · 2024-02 | Thought → Action → Observation döngüsü; gözlem dış ortamdan gelir | Döngüyü ~50 satırda yaz; her Action ve Observation ayrı event; Action = **öneri**, world uygular | "Thought" metnini claim/kanıt saymak |
| 1c | Reflexion ([2303.11366](https://arxiv.org/abs/2303.11366), [noahshinn/reflexion](https://github.com/noahshinn/reflexion)) | MIT · 3.3k · 2025-01 | Ağırlık güncellemeden "sözel pekiştirme": görev geri bildiriminden yansıma yazılır, epizodik bellek tamponunda tutulur, sonraki denemede kullanılır | Yansıma = `parent_event_id` bağlı türetilmiş event; geri bildirim kaynağı **dış** (Verifier/test) olmalı | İç öz-değerlendirmeyi geri bildirim kaynağı yapmak (bkz. 3) |
| 1d | smolagents (önceki raporda var) | Apache-2.0 · 29.8k · 2026-10-06 | — | Yalnız ek not: adım tavanı + işlem sınırı = bizim bütçe event'leri | — |
| 2a | Temporal ([temporalio/temporal](https://github.com/temporalio/temporal), [workflow-definition](https://docs.temporal.io/workflow-definition)) | MIT · 23.6k · 2026-10-09 | Workflow kodu deterministik olmalı; replay'de üretilen komutlar Event History ile karşılaştırılır, uyuşmazsa "non-determinism error". LLM/API/zaman/rastgele → **Activity**; sonuçları history'ye yazılır, replay'de yeniden çağrılmaz. Kod değişimi = versioning/patch | **En önemli ders.** Model çağrısı = Activity: yanıt (ya da hash'i) event olarak yazılır, replay modeli asla tekrar çağırmaz. Zaman ve rastgelelik de event'ten okunur. Replay testi: log'dan projeksiyonu yeniden kur, eşitliği doğrula | Temporal sunucusunu kurmak; bizde tek log yeterli |
| 2b | DBOS ([dbos-transact-py](https://github.com/dbos-inc/dbos-transact-py)) | MIT · 1.6k · 2026-10-09 | Aynı durable-execution fikri, ayrı sunucu yerine Postgres tablosuyla adım kaydı (README'den; ayrıntı okunmadı) | "Ayrı orkestratör gerekmez, adım kaydı DB'de" fikri bizim `store.py` yönümüzü doğruluyor | Bağımlılık olarak almak |
| 2c | Linda / tuple space (Gelernter 1985, [DOI 10.1145/2363.2433](https://doi.org/10.1145/2363.2433)) | makale | `out` / `in` (alıp siler) / `rd` (okur); üretici ve tüketici birbirini tanımaz; `in` atomik | Görev panosu: mission = tuple; `in` = atomik claim (= `acquire_lease`); `rd` = projeksiyon okuma. Blackboard'ın daha dar, atomik hâli | Paylaşılan değişken alan; bizde alan yalnız log projeksiyonu |
| 3a | Zheng ve ark. ([2306.05685](https://arxiv.org/abs/2306.05685)) | makale | LLM-as-judge: konum, uzunluk (verbosity) ve öz-tercih yanlılıkları | Critic'e iki sırayla sorma (A/B ve B/A), tutarsızsa `unverified` | Tek geçişli judge skorunu `verified` saymak |
| 3b | Wang ve ark. ([2305.17926](https://arxiv.org/abs/2305.17926)) | makale | Yanıt sırası değişince sıralama değişiyor (ChatGPT judge ile Vicuna 66/80 kazanıyor); çözüm: önce kanıt, sonra puan; konum dengeleme | Critic çıktısı şeması: `evidence[]` önce, `verdict` sonra; kanıtsız verdict reddedilir | Serbest metin puan |
| 3c | Panickssery ve ark. ([2404.13076](https://arxiv.org/abs/2404.13076)) | makale | Model kendi çıktısını tanıyor ve daha yüksek puanlıyor; öz-tanıma ile öz-tercih doğrusal ilişkili | **Farklı aile şartımızın (`families_conflict`, fail-closed) doğrudan ampirik dayanağı.** Aile, model_id değil sağlayıcı ailesi olarak kalmalı | Aynı aile farklı sürümü `verified` saymak (bizde zaten `verified-weak`) |
| 3d | Huang ve ark. ([2310.01798](https://arxiv.org/abs/2310.01798)) | makale | Dış geri bildirim olmadan "intrinsic self-correction" akıl yürütmede çalışmıyor, bazen bozuyor | Reflexion/evaluator döngüsünde geri bildirim kaynağı kaynak metin, test, kural Verifier olmalı | Öz-eleştiri döngüsünü doğrulama katmanı saymak |
| 4a | A-MEM ([2502.12110](https://arxiv.org/abs/2502.12110), [agiresearch/A-mem](https://github.com/agiresearch/A-mem); ayrıca [WujiangXu/A-mem](https://github.com/WujiangXu/A-mem)) | MIT · 1.2k (agiresearch, 2025-12) / 1.0k (WujiangXu, 2026-03) | Zettelkasten: her yeni anı yapılandırılmış not (öznitelikler, anahtar kelimeler, bağlantılar); eski notlar yeni anıya göre **evrilir** | Not = event; bağlantı = ayrı `memory.link` event'i; "evrim" eskiyi değiştirmez, yeni sürüm event'i yazar. İndeks = projeksiyon | Modelin eski notu yerinde güncellemesi (append-only'yi bozar) |
| 4b | Generative Agents / Letta (önceki raporda) | Apache-2.0 · 22.2k (bakım yok, 2024-08) / 25.1k (2026-09) | — | Ek: üç bellek de aynı üç parçaya iniyor: kayıt (log), geri getirme (projeksiyon + skor), konsolidasyon (türetilmiş event) | — |
| 4c | CoALA ([2309.02427](https://arxiv.org/abs/2309.02427)) | makale | Dil ajanları için ortak şema: çalışma / epizodik / anlamsal / prosedürel bellek + iç ve dış eylem ayrımı | Katman sözlüğü olarak kullan: epizodik = log, anlamsal = doğrulanmış claim'ler, prosedürel = beceri/SOP | — |
| 5a | **Concordia** ([google-deepmind/concordia](https://github.com/google-deepmind/concordia); [2312.03664](https://arxiv.org/abs/2312.03664), [2507.08892](https://arxiv.org/abs/2507.08892)) | Apache-2.0 · 1.8k · 2026-10-08 | Masaüstü RPG deseni: **Game Master** ortamı simüle eder; oyuncular niyetlerini doğal dille söyler, GM sonuca çevirir (ör. fiziksel olabilirlik kontrolü). Entity = component'ler (bellek, talimat, eylem seçimi); engine her `run_loop`'ta player/GM rolü atar; sıralı, eşzamanlı veya asenkron motorlar | **Bizim World = GM.** Ajan `propose`, GM (kural kodu, LLM değil) `resolve` → `append_event`. Engine arayüzü (turn-based / simultaneous) ayrı modül olarak yazılabilir | Concordia'da GM de LLM; bizde GM'nin çözümleme kuralları **deterministik kod** kalmalı, LLM GM yalnız anlatı/öneri |
| 5b | Mesa (önceki raporda) | Apache-2.0 · 3.9k · 2026-10-09 | — | Yalnız deney koşum ortamı olarak; çekirdeğe bağımlılık değil | — |
| 6a | Fencing token (Kleppmann 2016, ["How to do distributed locking"](https://martin.kleppmann.com/2016/02/08/how-to-do-distributed-locking.html)) | blog | Lease süresi dolan eski sahip (GC duraklaması vb.) hâlâ yazabilir; her lease'e artan numara verilir, kaynak eski numaralı yazımı reddeder | `lease.acquire` event'ine monoton `lease_epoch`; ajanın her yazımı epoch taşır; world eski epoch'u reddeder | Yalnız TTL'e güvenmek |
| 6b | Postgres `FOR UPDATE SKIP LOCKED` ([docs](https://www.postgresql.org/docs/current/sql-select.html)); kuyruklar: [river](https://github.com/riverqueue/river) (MPL-2.0 · 5.8k), [oban](https://github.com/oban-bg/oban) (Apache-2.0 · 4.0k), [graphile/worker](https://github.com/graphile/worker) (MIT · 2.4k) — hepsi 2026-10'da aktif | — | Çok işçili claim: kilitli satırı atla, sıradakini al; görev = satır + durum makinesi + deneme sayısı | Çoklu işçi gelince claim'i tek atomik işlemde yap (Python'da tek yazıcı + kuyruk yeterli olabilir) | Bunlardan birini bağımlılık almak (Go/Elixir/Node) |

### Kısa notlar

1. **Ortak payda:** taranan her ciddi sistem aynı ayrımı yapıyor: *öneri* (model/oyuncu/Activity) ile *uygulama* (GM/workflow/world). Kilitli "Policy → Action → Validation" ilkemiz Temporal (Activity sonucu history'de) ve Concordia (GM sonucu belirler) ile birebir örtüşüyor. Desen adı olarak "propose → resolve → append" önerilebilir (öneri, karar değil).
2. **Kendi kodumuzda gözlenen iki boşluk (main `2d8b222`, yerelde denendi; kod değiştirilmedi):**
   - `store.py:171` projeksiyonda `lease_until = _now() + ttl` hesaplıyor. Log yeniden oynatılırsa `lease_until` farklı çıkar; Temporal dersiyle çelişir. Saat hash'e girmiyor (kilitli), ama projeksiyon `ev.ts`'den türetilebilir. Bu, saati hash'e sokmadan replay'i deterministik yapar.
   - `acquire_lease` görev durumuna bakmıyor: `status="verified"` bir görevde `acquire_lease` çağrısı durumu `claimed` yaptı. DECISION-LOG "Lease does not reopen a terminal mission" diyor; mevcut test (`test_release_does_not_reopen_verified`) yalnız *release* yolunu kapsıyor, *acquire* yolunu değil. Ayrıca `lease.release` event'i sahiplik kontrolü olmadan her aktörden kabul ediliyor (fencing yok).
3. **Doğrulama:** 3a–3d birlikte şunu söylüyor: aynı model ailesi ve iç öz-düzeltme güvenilir doğrulayıcı değil. Bizim üç seviyeli, fail-closed aile kuralımız literatürle uyumlu ve taranan çerçevelerden katı. LLM Critic gelirse eklenebilecek ucuz önlemler: konum değiştirme, kanıt-önce şeması, kaynak metinde birebir eşleşme kontrolünün korunması.
4. **Bellek:** A-MEM'in "not evrimi" ancak sürüm event'i olarak alınabilir. Vektör/anahtar kelime indeksi projeksiyondur, yeniden kurulabilir olmalı.
5. **Faz eşlemesi (seçenek, karar değil):**
   - *Faz 0 (kapalı) üzerine, LLM'siz yapılabilecekler:* replay testi (log → projeksiyon eşitliği), `lease_until`'in `ev.ts`'den türetilmesi, terminal görevde acquire reddi + test, `lease_epoch` (fencing), GM/engine arayüzünün kural tabanlı ajanlarla soyutlanması. Hiçbiri API açmaz.
   - *Faz 1 seçilirse:* model çağrısı = Activity (yanıt/hash event'te, replay yeniden çağırmaz), tek rol (önce Researcher), workflow modu (agent modu değil), iterasyon ve token tavanı, Critic farklı aileden + kanıt-önce şeması.
   - *Sonraki:* A-MEM tarzı bağlantılı bellek, Concordia tarzı çoklu engine, çok işçili claim (SKIP LOCKED deseni).

### Doğrulanamayan / dikkat

- DBOS'un iç mimarisi yalnızca README düzeyinde; ayrıntı okunmadı.
- Concordia 2507.08892 ("Multi-Actor Generative AI as a Game Engine") yalnız başlık düzeyinde doğrulandı; gövde okunmadı.
- 2306.05685'teki üç yanlılık türü makaleden bilinen içerik; bu turda yalnız başlık doğrulandı. 2305.17926, 2404.13076, 2310.01798, 2502.12110, 2303.11366 özetleri okundu.
- Linda DOI ACM'ye yönlendiriyor; tam metin okunmadı.
- ★ sayıları anlık; restatedev/restate (★4.5k) lisansı GitHub'da "NOASSERTION" görünüyor, tabloya alınmadı.

### Paneller için sorular

1. **"propose → resolve → append"** desenini (Concordia GM + Temporal Activity) World/Agent/Model ayrımının resmi adı yapmak istiyor musunuz? GM'nin `resolve` adımı her zaman deterministik kod mu kalmalı, yoksa ileride LLM GM yalnız anlatı katmanı olarak mı izinli olmalı?
2. **Replay determinizmi:** `lease_until`'in `ev.ts`'den türetilmesi ve bir replay testi, "saat hash'e girmez" kilidiyle uyumlu mu? Faz 1'den önce mi yapılmalı?
3. **Terminal görev + fencing:** `acquire_lease`'in terminal görevi `claimed` yapması kilitli ilkeye aykırı görünüyor. Bunu bir düzeltme turu olarak mı ele alalım? `lease_epoch` (fencing token) gerekli mi, yoksa tek yazıcılı dünyada aşırı mı?
4. **Model yanıtının kaydı:** Faz 1 açılırsa ham model yanıtı log'a mı girmeli, yoksa yalnız hash + yapılandırılmış öneri mi? (Temporal Activity sonucunu tam saklar; bizde boyut ve gizlilik ayrıca tartışılmalı.)
5. **Critic için LLM-as-judge önlemleri** (A/B–B/A konum değişimi, kanıt-önce şeması, birebir kaynak eşleşmesi): hangileri `verified` için zorunlu olmalı, hangileri yalnız `verified-weak`'i etkilemeli?
