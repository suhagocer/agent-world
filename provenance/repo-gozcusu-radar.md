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
| A1 | ChatGPT (kök fikir) | https://chatgpt.com/share/6aa7584b-0b3c-83eb-a3aa-6b16d096db46 |
| A2 | Gemini | https://share.gemini.google/1tuZ3H4PH5af → https://gemini.google.com/share/d272dd7f8df1 (önceki `rbdXh…`/`9dPr…`; UI kısa link `TXv3jkvZV7w3` de aynı `d272dd…`; **aynı sohbet**) |
| A3 | DeepSeek | https://chat.deepseek.com/share/wfbt7ngfw6r7f8whwq (önceki `ulwkayx5qsy0otx8vd`; daha eski `japybl2d3ejtr7ch0i` / `wcnvcw1pdaacp6z5o2`) |
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

Event-sourced, provenance-first multi-agent OS (chat/3D değil). Agent Engine vs World Engine; LLM değiştirilebilir biliş sağlayıcısı; Multi-Model Router (görev/maliyet/gecikme). Append-only log → projeksiyonlar; lease + heartbeat + timeout. Kanıt sözleşmesi (factual/executable/judgmental/procedural); karantina retrieval’a girmez. Model çeşitliliği (producer ≠ critic ailesi). Maliyet merdiveni + mission bütçesi. Need Engine eşikli. Chaos Agent → Critic. Dış: World Card / A2A / MCP. Ana tehlike: ünvanlı sohbet odası. Operasyonel: Faz 0 dogfood; golden Context Builder; `agent_projection` + `model_registry`; bilinmeyen aile → `unverified`; altıncı model yok. Link zinciri: `9dPr…` → `rbdXh…` → **`1tuZ3…`** / `TXv3…` (aynı içerik, son yayın ~05:13).

### A3) DeepSeek (kanonik `wfbt7ngfw6r7f8whwq`; önceki `ulwkayx5qsy0otx8vd`)

World ≠ Environment ≠ Agent ≠ Model. Tek event log + projeksiyon. Provenance, Failure Memory, çelişki grafı, TTL. Üç kademe verify. Faz 0 döngü + Context Builder tavanı. Mission DNA sonra veya parent/retry. Minimal event log eğilimi.

2026-10-05 kanonik paylaşım `wfbt7ngfw6r7f8whwq` (mesaj 54–55, ebeveyn 53; curl `/api/v0/share/content` ham JSON 7768 bayt; görünen istek+yanıt 4123 karakter). Önceki `ulwkayx5qsy0otx8vd` (mesaj 52–53; ham 26752 bayt; görünen 4057 karakter) ile **aynı değil** — yeni tur. DeepSeek iddiası (karar değil): önerdiği 6 maddelik `DECISION-LOG` maddesinde “heartbeat” yazmış; Faz 0’da heartbeat yok, yalnızca lease + timeout; madde 4’ü “Lease + timeout” diye düzeltiyor (heartbeat Faz 1). Test referanslı 6 madde önerisi ve Anayasa (15) / DECISION-LOG (6) ayrımı DeepSeek’e ait; panele işlenmedi. Önceki `ulwkay…` turundaki `run_mission.py` / Faz 0 kapandı / Faz 1 notu da DeepSeek iddiasıydı; karar sayılmaz.

### A4–A5) Grok + flame-sage

Beş-model hakemlik. Event log + projeksiyon; lease. Faz 0 kodu (15/15). DNA / token / Need erken red. flame-sage canlı: **Tur 14’e kadar** (v1.0–v1.17; [flame-sage-sage-tundra.grok.me](https://flame-sage-sage-tundra.grok.me)). 2026-10-05 itibarıyla `/tur-9`…`/tur-14` yeniden açık; `/tur-15` 404.

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

**Mimari haritadaki yeri:** (1) projenin deterministik dünya çekirdeği katmanının kuralları artık karar kaydında yazılı. Yeni kod yok; boşluk kapatmıyor, mevcut çekirdeği kayda geçiriyor. Runtime, env/verifier, world-model, bellek ve gerçek zamanlı katmanlar hâlâ bilinçli olarak yok. Radardaki “Ortak kararlar / Korunan” listesi bu günlükle uyumlu; çelişki yok.

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
