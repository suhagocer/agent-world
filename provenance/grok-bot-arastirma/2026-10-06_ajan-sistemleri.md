> Grok Bot araştırma notu; karar değildir. Kararlar yalnızca decisions/DECISION-LOG.md'de.

# Ajan sistemleri taraması: kendi ajan kodumuzu yazarken neleri ödünç alırız?

Tarih: 2026-10-06 · Hazırlayan: Grok Bot (yürütücü) · Durum: **beş modelli panele girdi. Karar değildir.**
Dayanak: `suhagocer/agent-world` @ `90e8c99` (store.py, agents/, run_mission.py, DECISION-LOG). `test_faz0.py` yerelde 24/24 geçti. README hâlâ "15/15" diyor.

## Ölçüt: kilitli omurga (2026-10-03)

World / Agent / Model ayrı. Tek append-only, hash zincirli log. Verified claim için provenance zorunlu. Lease terminal görevi yeniden açmaz, heartbeat yok. Üç seviyeli doğrulama: unverified / verified-weak / verified. Model dünya durumuna yazmaz. Aşağıdaki "çatışma" maddeleri bu cümlelere göre yazıldı.

## Çerçeveler ve mimariler

**LangGraph** (MIT). Durum makinesi/graf tabanlı, düşük seviyeli orkestrasyon. Pregel'den esinlenir. Checkpointer ile kalıcı yürütme ve `interrupt` ile insan onayı sunar. *Ödünç:* adım adım checkpoint ve kesintiden devam; insan onayı noktası. *Çatışma:* düğümler paylaşılan state'i doğrudan reducer'larla değiştirir. Checkpoint log değil, anlık görüntüdür. → **Fikrini al, kütüphaneyi alma.** [README](https://github.com/langchain-ai/langgraph) · [persistence](https://docs.langchain.com/oss/python/langgraph/durable-execution) · [interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts)

**AutoGen / AG2.** AutoGen'de kod MIT, dokümanlar CC-BY-4.0. Repo artık **bakım modunda**, halefi Microsoft Agent Framework (MIT). AG2 (Apache-2.0) topluluk çatalı. v1.0'da klasik `ConversableAgent`/`GroupChat` ayrı repoya taşındı. *Ödünç:* konuşma desenleri (iki ajan, grup sohbeti, insan proxy'si). *Çatışma:* koordinasyon sohbet geçmişi üzerinden yürür. Sohbet = durum yaklaşımı tek log + projeksiyon modeline uymaz. API çok hızlı değişiyor. → **Kaçın. Desen kataloğu olarak oku.** [AutoGen](https://github.com/microsoft/autogen) · [AG2](https://github.com/ag2ai/ag2) · [makale](https://arxiv.org/abs/2308.08155)

**CrewAI** (MIT). Rol/hedef tabanlı "Crews" (özerk) ve olay güdümlü "Flows" (deterministik). *Ödünç:* özerk ekip ile deterministik akışın ayrılması. Bizde Flow karşılığı world tarafındaki görev durum makinesi olabilir. *Çatışma:* bellek ve görev durumu çerçevenin içinde tutulur. "Unified Control Plane" ticari ürünle iç içe. → **Kaçın.** Crews/Flows ayrımı tartışmaya değer. [README](https://github.com/crewAIInc/crewAI) · [docs](https://docs.crewai.com/)

**OpenAI Agents SDK** (MIT). Az primitif var: Agent, handoff / agent-as-tool, guardrail, session, tracing, sandbox agent. Dokümanı açıkça şunu söylüyor: "döngüyü, araç dağıtımını ve durumu kendin yönetmek istiyorsan doğrudan Responses API kullan." *Ödünç:* paralel çalışan girdi/çıktı guardrail'leri, `max_turns` sınırı, trace kavramı. *Çatışma:* session belleği SDK'nın içinde. Varsayılan olarak tek sağlayıcıya yöneliyor. → **Desenleri al: guardrail ve adım sınırı.** [docs](https://openai.github.io/openai-agents-python/) · [guardrails](https://openai.github.io/openai-agents-python/guardrails/)

**smolagents** (Apache-2.0). Ajan mantığı yaklaşık 1.000 satır, model-agnostik. `CodeAgent` eylemleri Python kodu olarak yazar. Yerel AST yorumlayıcı importları beyaz listeyle sınırlar ve işlem sayısına üst sınır koyar. E2B, Docker, Modal ve Blaxel ile sandbox desteği var. *Ödünç:* küçük, okunabilir döngü; sandbox katmanları; işlem/adım tavanı. *Çatışma:* kod-eylem modelin yan etki üretmesi demek. "Model dünyaya yazmaz" kuralıyla ancak sandbox + öneri→doğrulama ile bağdaşır. → **Döngü boyutunu ve sandbox yaklaşımını örnek al.** [README](https://github.com/huggingface/smolagents) · [güvenli yürütme](https://huggingface.co/docs/smolagents/tutorials/secure_code_execution) · [CodeAct](https://arxiv.org/abs/2402.01030)

**CAMEL** (Apache-2.0). Rol yapma ve "inception prompting" ile iki ajanın özerk işbirliği. Topluluk "ajan ölçekleme yasaları" peşinde. *Ödünç:* rol tanımını prompt'ta sabitleme, toplu simülasyon fikri. *Çatışma:* doğrulama ya da provenance kavramı yok. → **Araştırma referansı olarak kullan.** [repo](https://github.com/camel-ai/camel) · [makale](https://arxiv.org/abs/2303.17760)

**MetaGPT** (MIT). `Code = SOP(Team)`. Standart işletim prosedürleri prompt dizilerine kodlanır. Ara çıktılar yapılandırılmıştır ve sonraki rol bunları doğrular. *Ödünç:* SOP = görev tipi başına sabit adım dizisi. Ara çıktıyı şemalı artefakt olarak kaydetme (bizde event). *Çatışma:* aynı modelin rolleri birbirini doğrulayabilir. Bizde bu en iyi ihtimalle verified-weak sayılır. → **SOP fikrini al.** [repo](https://github.com/FoundationAgents/MetaGPT) · [makale](https://arxiv.org/abs/2308.00352)

**Letta / MemGPT** (Apache-2.0). İşletim sistemi esinli katmanlı bellek. Bağlamda her zaman duran "memory block"lar (label, description, value, limit) ve arşiv belleği var. Ajan kendi belleğini araçlarla düzenler. *Ödünç:* sınırlı, etiketli, salt-okunur seçeneği olan bağlam blokları. Bu `context_builder.py` için iyi bir model. *Çatışma:* öz-düzenleyen bellek modelin durumu doğrudan yazması demek. Dokümana göre eşzamanlı yazımda "son yazan kazanır". → **Blok yapısını al, öz-düzenlemeden kaçın.** Bellek değişikliği event olmalı. [docs](https://docs.letta.com/guides/agents/memory-blocks) · [repo](https://github.com/letta-ai/letta) · [makale](https://arxiv.org/abs/2310.08560)

**Generative Agents ("Smallville")** (Apache-2.0). Doğal dilde tam deneyim kaydı (memory stream). Yansıma ile üst düzey çıkarım ve geri getirme ile planlama yapar. Geri getirme yakınlık, önem ve ilgi puanlarıyla yapılır. *Ödünç:* memory stream bizim event log'umuzla birebir örtüşüyor. Yansıma `parent_event_id` bağlı türetilmiş event olabilir. *Çatışma:* araştırma kodu, bakım yok. Yansımalar doğrulanmamış çıkarımdır, claim sayılmamalı. → **Mimariyi al, kodu alma.** [makale](https://arxiv.org/abs/2304.03442) · [repo](https://github.com/joonspk-research/generative_agents)

**AgentVerse** (Apache-2.0). İnsan grup dinamiğinden esinlenir. Ekip bileşimi göreve göre dinamik değişir. Makale olumlu/olumsuz sosyal davranışların ortaya çıktığını raporluyor. *Ödünç:* göreve göre uzman "işe alma". Bu, ileride itibar tabanlı görev atamasına bağlanabilir. *Çatışma:* itibar/doğrulama kalıcı değil, oturum içi. → **Fikir kaynağı.** [repo](https://github.com/OpenBMB/AgentVerse) · [makale](https://arxiv.org/abs/2308.10848)

**ChatDev** (Apache-2.0). Şelale aşamalarında "chat chain" ve "communicative dehallucination" (belirsizlikte karşı tarafa soru sorma). 2.0 sürümü "DevAll" adında sıfır-kodlu platform. *Ödünç:* üreticinin eleştirmene netleştirme sorusu sorması. *Çatışma:* ürün yönü değişti (platform). → **Fikri al, kaçın.** [repo](https://github.com/OpenBMB/ChatDev) · [makale](https://arxiv.org/abs/2307.07924)

**Voyager** (MIT). Otomatik müfredat, çalıştırılabilir kod olarak büyüyen beceri kütüphanesi, çevre geri bildirimi ve öz-doğrulama ile yinelemeli prompting. *Ödünç:* beceri kütüphanesi. Faz 0'daki `skill_reused` maliyet düşüşü bunun ilkel hâli. Beceri = provenance'lı, sürümlü artefakt. *Çatışma:* öz-doğrulama aynı model demek, bizde `unverified`. → **Beceri kütüphanesini al, öz-doğrulamayı yeterli sayma.** [makale](https://arxiv.org/abs/2305.16291) · [repo](https://github.com/MineDojo/Voyager)

## Protokoller

**MCP.** Lisans MIT'ten Apache-2.0'a geçiş sürecinde (yeni katkılar Apache-2.0). JSON-RPC 2.0 kullanır. Host / client / server rolleri var. Sunucular araç, kaynak ve prompt sunar. Opsiyonel "Tasks" uzantısı uzun işler için. Spesifikasyon araç açıklamalarını güvenilmez sayar. *Ödünç:* araç erişimini MCP ile standartlaştırmak. Araç çağrısı sonucu event olur, kaynak URI'si provenance olur. *Çatışma:* yok, sınırda kalırsa. MCP sunucusu dünya durumuna yazan bir yol olmamalı. → **Faz 1+ araç sınırı için güçlü aday.** [spec](https://modelcontextprotocol.io/specification/latest) · [lisans](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/LICENSE)

**A2A** (Apache-2.0, sürüm 1.0.0). Ajan Kartı (yetenekler, beceriler, güvenlik şemaları, opsiyonel JWS imzası). Task yaşam döngüsü: submitted, working, input-required, completed, failed, canceled, rejected, auth-required. Terminal görev yeni mesaj kabul etmez. "Opak yürütme" ilkesi var. *Ödünç:* terminal durum semantiği bizim "lease terminal görevi açmaz" kuralıyla örtüşüyor. Ajan Kartı imzası kimlik için kullanılabilir. *Çatışma:* A2A'da görev durumunu uzak ajan yönetir. Bizde durum world'ün log'unda olmalı. Kartın imzası itibar sağlamaz. → **Dış ajanlarla konuşmak için sonraki faz; iç çekirdeğe sokma.** [spec](https://a2a-protocol.org/latest/specification/) · [repo](https://github.com/a2aproject/A2A)

## Desenler

**Event sourcing.** Durum, olayların sırayla uygulanmasından türetilir ve yeniden oynatılabilir. Bu bizim omurgamız. *Ödünç:* replay testleri; projeksiyon yeniden kurulumu; snapshot'ı yalnızca optimizasyon olarak kullanmak. → **Zaten bizde. Snapshot hash'e girmemeli.** [Fowler](https://martinfowler.com/eaaDev/EventSourcing.html)

**Actor modeli / Erlang-OTP / Orleans.** Paylaşımsız durum, mesajla iletişim, gözetmen ağaçları ("let it crash"), sanal aktörler (grain). *Ödünç:* her ajan bir aktör. Çöken ajan dünya durumunu bozamaz. Gözetmen = lease süresi dolunca `expire_leases`. *Çatışma:* aktörler kendi durumunu tutar. Bizde kalıcı durum yalnız log'da. Aktör durumu önbellek sayılmalı. → **Hata izolasyonunu al.** [OTP](https://www.erlang.org/doc/system/design_principles.html) · [Orleans](https://learn.microsoft.com/en-us/dotnet/orleans/overview)

**Lease (Gray & Cheriton, 1989).** Süreli yetki. Sahip ölürse yetki kendiliğinden düşer. Heartbeat yerine TTL'li yenileme bizim Faz 0 tercihimizle uyumlu. → **Teorik dayanak.** [DOI](https://doi.org/10.1145/74850.74870)

## Sentez: Faz 1'de LLM eklenince (panel için sorular)

1. **Model adaptörü sınırı.** Hiçbir çerçeve "model dünyaya yazmaz" kuralını garanti etmiyor. Tartışılacak desen: adaptör yalnız `propose(context) -> Proposal` döndürür (şemalı JSON; token, model_id ve maliyetle birlikte). Proposal'ı ajan kodu doğrular ve `append_event` ile world yazar. OpenAI SDK'nın "döngüyü kendin yönet" yolu ve smolagents'ın model-agnostik arayüzü bu sınıra örnek. Açık soru: ham model yanıtı log'a girsin mi, yoksa yalnız hash'i mi?
2. **Bellek.** Generative Agents'ın memory stream'i ve Letta blokları birlikte düşünülebilir. Log tek gerçek kaynak. Bağlam blokları `context_builder` tarafından projeksiyondan türetilen salt-okunur görünümler olur. Yansıma/özet event olarak yazılır ve claim değildir. Açık soru: vektör indeksi projeksiyon mu sayılır?
3. **Doğrulama.** Voyager, MetaGPT ve ChatDev'in öz-/rol-doğrulaması bizim kuralımıza göre en fazla `verified-weak` olur. Bizim farklı aile şartı taranan sistemlerin hepsinden katı. Guardrail'ler (OpenAI SDK) `append_event` öncesi doğrulayıcı olarak eklenebilir. Rapor edilmesi gereken bir şey: Faz 0'da Critic doğrulaması kural tabanlı. LLM gelince "kaynakta birebir geçiyor" kontrolü korunmalı mı?
4. **Maliyet.** `Mission.budget_tokens` zaten var. Her model çağrısı token/maliyet event'i yazabilir. Bütçe aşımı lease bırakma ile sonuçlanabilir. Adım tavanı (`max_turns`, smolagents işlem sınırı) ve beceri yeniden kullanımı (Voyager) maliyet kolu olarak masada.
5. **Kendimiz yazmamız muhtemel olanlar:** event log ve projeksiyonlar, lease, üç seviyeli doğrulama, itibar (taranan hiçbir çerçevede kalıcı ve doğrulamaya bağlı itibar yok), model adaptörü, bağlam kurucu, bütçe muhasebesi.
   **Hazır alınabilecekler:** sağlayıcı istemcileri, MCP (araç sınırı), sandbox (Docker/E2B), ileride A2A (dış ajanlar).
6. **Faz notu:** DECISION-LOG'a göre Faz 1 başlamadı. Bu rapor Faz 1'i başlatma önerisi değildir.

## Doğrulanamayan / dikkat

- Gray & Cheriton DOI sayfası otomatik erişimi engelledi (403). Atıf bilinen kaynaktan yapıldı.
- Generative Agents'ın üç puanlı geri getirmesi makale gövdesinden; yalnız özet okundu.
- AgentVerse'ün dört aşamalı döngüsü bu turda doğrulanmadığı için yazılmadı.
