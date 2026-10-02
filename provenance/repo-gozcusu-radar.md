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

## AI sohbet özetleri — 2026-10-02

Kaynaklar (tam paylaşım URL’leri). Diğer ajanlar buradan yararlanabilir; yazma yetkisi yalnızca Repo Gözcüsü’ndedir.

| # | Model | Kaynak |
|---|--------|--------|
| 1 | ChatGPT (kök fikir) | https://chatgpt.com/share/6aa7584b-0b3c-83eb-a3aa-6b16d096db46 |
| 2 | ChatGPT (GitHub tarama) | https://chatgpt.com/share/6abed9e1-42b4-83eb-916f-91866fbd5de2 |
| 3 | Gemini | https://share.gemini.google/9dPrAQyfprLI (redirect ≈ `gemini.google.com/share/956fff2b…`) |
| 4 | DeepSeek | https://chat.deepseek.com/share/wcnvcw1pdaacp6z5o2 |
| 5 | Grok | https://grok.com/share/c2hhcmQtMg_120d0cd7-772a-4041-b650-07d00ee5f6e1 |
| 6 | Claude | https://claude.ai/share/1c1203ca-4e67-455d-aabb-a6bbb8e28787 |
| 7 | Claude (v3 kanon) | https://claude.ai/share/1d8f6dac-fcff-4605-9d36-52ab61fceea1 |
| 8 | ChatGPT (araçlar) | https://chatgpt.com/share/6abf0d6a-6ed4-83eb-80ee-5fd27fecec24 |

### 1) ChatGPT — kök fikir

İnsan → ajan → dünya katmanı. Yetki seviyeleri; A2A; web MVP. Sonra: ajanların keşfedip girdiği dünya, resident ajanlar, Need Engine, multi-model, sandbox.

### 2) ChatGPT — GitHub tarama

Tek fork değil **parçalı mimari**. Referans: sendwealth/agent-world, AgentSociety (tsinghua), RUC-NLPIR/Agent-World, AgentArena, meleantonio/AgentSociety, Snowflake-Labs/agent-world-model, Qwen-AgentWorld, vb. (üstteki referans haritası).

### 3) Gemini

Event-sourced OS düşüncesi. Ünvanlı sohbet riski uyarısı. v3 omurga. Ollama/API tartışması. `family_verified` fail-closed.

### 4) DeepSeek

World loop; Chaos / zero-trust. Mission DNA (Grok reddetti). Faz 0 Researcher–Critic–Verifier. `verified-weak` kademesi.

### 5) Grok

Beş-model hakemlik. Event log + projeksiyon; lease. Faz 0 kodu (15/15) agent-world’te. DNA / token / Need erken reddedildi. flame-sage tur 9–12 notları ([flame-sage-sage-tundra.grok.me](https://flame-sage-sage-tundra.grok.me)).

### 6) Claude

Context builder golden-file kritik risk. Şema/test vurgusu. DeepSeek mühendis; Claude+Grok review. `verify_chain` sonrası geldi.

### 7) Claude — v3 kanon

Kalıcı çok-ajan OS; faz 0–5 yol haritası. Ertelenenler: DNA, token, 3D. İlke: kanıt + reuse.

### 8) ChatGPT — araçlar

Stitch → Antigravity → Jules zinciri. Ollama = Model Router katmanı (ürün değil). Mixboard/Pomelli ikincil (world-first, graphics later).

### Ortak kararlar

**Korunan**

- Kernel önce; LLM doğrudan state yazmaz
- Event log + hash zinciri + fail-closed doğrulama
- Üç kademeli doğrulama (`unverified` / `verified-weak` / `verified`); `_attested` yok sayılır
- Lease; verified görevleri rastgele yeniden açmama
- Parçalı açık kaynak referans (tek monorepo fork değil)
- Kanıt + reuse; erken DNA/token/Need/3D yok
- Beş-model hakemlik; kanon damgası tanı testinden gelir

**Reddedilen / ertelenen**

- Mission DNA (erken)
- Token ekonomisi / Need Engine (erken)
- 3D / Godot NPC runtime (şimdi değil)
- LLM’i ürün sanmak (Ollama = router katmanı)
- Tek modelin “kanon” sayılması; ünvanlı sohbet riski
- Antigravity/Jules’a mimari bağımlılık (geliştirme aracı, dünya runtime’ı değil)

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
| 1 | ChatGPT kök | WebFetch: kabuk (içerik boş/minimal) | Önceki kök özet korunuyor; sayfa snapshot zayıf |
| 2 | ChatGPT GitHub | WebFetch 500 | Önceki özet + referans haritası duruyor |
| 3 | Gemini | Browser turunda | Bekleniyor / 403 riski |
| 4 | DeepSeek | Browser turunda | Bekleniyor / 403 riski |
| 5 | Grok | WebFetch: uzun sohbet yüklendi | Önceki özet **doğrulandı**; flame-sage tur 9–12 + “Repo Gözcüsü izler, kod yazmaz” notu eklendi |
| 6–7 | Claude ×2 | WebFetch: yalnızca “Claude” kabuğu | Browser ile yeniden denenecek |
| 8 | ChatGPT araçlar | WebFetch: tam | Stitch→Antigravity→Jules + Ollama=router **doğrulandı**; Mixboard/Pomelli ikincil |

Yeni mimari karar yok (Grok/araçlar sayfaları mevcut digesti güçlendirdi). Claude/Gemini/DeepSeek browser sonuçları gelince bu bölüme eklenecek; değişiklik yoksa ekstra commit yok.

## Günlük / dönemsel notlar

_(Repo Gözcüsü yeni taramaları buraya ekler.)_

- **2026-10-01:** Dosya oluşturuldu. ChatGPT paylaşım özeti ve 8 parçalı referans haritası seed olarak eklendi.
- **2026-10-01 (akşam):** Yetki genişletmesi onaylandı (yalnızca bu dosya). “Sonraki tarama hedefi” bölümü eklendi.
- **2026-10-02:** Sekiz AI sohbet özeti, ortak kararlar ve Faz 0 eşlemesi eklendi.
- **2026-10-02 (gece):** Tam paylaşım URL’leri dolduruldu; yeniden fetch turu başladı (Grok + ChatGPT araçlar doğrulandı).
