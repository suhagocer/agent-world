> Grok Bot araştırma notu; karar değildir. Kararlar yalnızca decisions/DECISION-LOG.md'de.

# LLM'siz Otonom Ajan Sistemleri: Araştırma ve Veri Analizi

**Tarih:** 2026-10-06 · **Kapsam:** Dışa dönük literatür ve ekosistem taraması (proje kodu incelenmedi) · **Statü:** Beş modelli panel için *girdi*. Burada hiçbir şey karara bağlanmış değildir; bütün öneriler seçenek olarak sunulmaktadır.

## 0. Öne çıkan bulgular

1. **Doğrulama sinyali olmadan itibar öğrenilemez.** Oyuncak simülasyonumuzda (§5.1) doğrulama yokken Beta itibarı hiç güncellenmedi; hata oranı itibarsız durumla aynı kaldı (%10,1).
2. **BOINC tarzı uyarlamalı replikasyon ucuz ama sızdırıyor.** Yürütme/görev 2,02'den 1,20'ye indi; ancak nadiren hile yapanlara (p=0,1) karşı kabul edilen hata %0,05'ten %0,75'e çıktı. BOINC'e göre sabit replikasyon en az %50 CPU yükü getirir, uyarlamalı mod %5–10 hedefler [51].
3. **Tohumsuz EigenTrust ele geçiriliyor, tohumlu olanı tekelleşiyor.** Tohumsuzken işbirlikçi kötü grup görevlerin %94'ünü aldı; tohumla hata sıfırlandı ama yükün ≈%100'ü ajanların %10'unda toplandı. Simetrik itibar fonksiyonları sybil-geçirmez olamaz [49].
4. **Piyasa yapısı zekânın bir kısmının yerini tutar.** Sıfır-zekâ (ZI) tüccarlar bütçe kısıtıyla çift müzayedede verimliliği %100'e yaklaştırdı [58]; ekonomi ölçümleri için doğal boş model.
5. **Oyun-YZ yığınları ucuz ve açıklanabilir.** Ölçtük: utility kararı ≈3,6 µs, py_trees tick ≈17 µs, 4 adımlı GTPyhop planı ≈170 µs (§7.1). Binlerce ajana tek Python süreci yetebilir (spekülatif).
6. **Determinizm bir mühendislik disiplinidir.** Python yalnızca `random()` dizisini uyumlu tohumla garanti eder [66]; PyTorch sürüm/platform arası tam tekrar üretilebilirlik vaat etmez [31]. Derin RL'yi denetlenebilir çekirdeğe koymak zor.
7. **"Reklam + şüphe" kalıbı dünyaya doğrudan uyuyor.** Sims'te nesneler ihtiyaç karşılamayı "reklam eder"; Forbus ve Wright vaatlerin sonradan doğrulanıp reklamların ölçeklenmesini ("Skeptical Sims") önerir [13]. Bu, beyan edilen yetenek → doğrulanmış itibar zincirinin karşılığı.
8. **Python ekosisteminde olgunluk farkı büyük.** py_trees, GTPyhop, PettingZoo, eventsourcing son 2 ayda sürüm çıkardı; experta (2019) ve durable_rules (2020) durgun, experta'da Python 3.10+ içe aktarma hatası bildirilmiş [19]. GOAP ve Utility AI için olgun kütüphane yok, ekip yazar.

## 1. Yöntem

- Sürüm/lisans verisi 2026-10-06'da PyPI JSON API, GitHub sürüm sayfaları ve LICENSE dosyalarından çekildi. Bakım: *aktif* ≤12 ay, *yavaş* 1–3 yıl, *durgun* >3 yıl.
- 1–5 puanlar yazarın yargısıdır (ölçüm değil); rubrik §8'de.
- Deneyler: `/workspace/exp/rep_sim.py`, `bench.py` (Python 3.13.5, 8 vCPU Xeon); oyuncak modeldir.
- Açk. = açıklanabilirlik; ✅ uyar, ◐ kısmen, ❌ uymaz.

## 2. Karar mimarileri

| Yöntem | Ne | Python (lisans, son sürüm) | Güçlü / zayıf | Maliyet | Açk. | Uyum |
|---|---|---|---|---|---|---|
| BDI | İnanç–arzu–niyet; niyet = taahhüt [1] | spade 4.1.4 (MIT, 2026-05) + spade_bdi 0.3.3 (MIT, 2026-07) [4][5]; Jason 3.3.0 / JaCaMo 1.3.1 Java, LGPL-3 [2][3] | + Görev = niyet; iptal/yeniden planlama doğal. − Python ekosistemi ince | Düşük–orta | Yüksek | ✅ Taahhüt üzerinden denetlenebilir görev alma |
| GOAP | STRIPS benzeri eylemlerle A*; F.E.A.R.'ın FSM'i yalnız 3 durumlu [6] | Olgun kütüphane yok | + Hedef/eylem ayrımı, eylem maliyeti. − Ajan başına arama | Orta | Yüksek (plan izi) | ✅ Esnek görev icrası |
| HTN | Görevi yöntemlerle alt görevlere ayırır (SHOP2) [7] | GTPyhop 2.0.2 (Clear BSD, 2026-08) [8] | + Çok adımlı görevlere doğal. − Yöntemleri tasarımcı yazar; genel HTN karar verilemez [9] | Düşük (≈170 µs) | Çok yüksek | ✅ Görev ayrıştırma |
| Davranış ağacı | Tick'li seçici/sıralayıcı ağaç [11] | py_trees 2.6.0 (BSD-3, 2026-09) [10] | + Modüler. − Hedef seçimi zayıf | Düşük (≈17 µs) | Çok yüksek | ◐ Yürütme katmanı |
| Utility AI | Normalize girdileri tepki eğrileriyle puanlayıp çarpar (IAUS) [12]; Sims ihtiyaç reklamları [13] | Olgun kütüphane yok | + Bağlama duyarlı görev/fiyat seçimi. − Eğri ayarı emek ister | Çok düşük (≈3,6 µs) | Orta–yüksek (skor dökümü) | ✅ Görev ve teklif seçimi |
| FSM / HFSM | Durum-geçiş; statechart'ta iç içe/paralel durum [14] | transitions 0.9.3 (MIT, 2025-07); python-statemachine 3.2.1 (MIT, 2026-08) [15] | + Yaşam döngüsü/protokol için ideal. − Karar vermez | Çok düşük | Çok yüksek | ◐ Yaşam döngüsü |
| Üretim kuralları | Rete ile ileri zincirleme; kısmi eşleşmeleri bellekte tutar [16] | clipspy 1.0.6 (BSD, 2025-10; CLIPS 6.4.2 MIT-0) [17]; durable_rules 2.0.28 (MIT, 2020) [18]; experta 1.9.4 (LGPL-3, 2019) [19]; Drools 10.2.0 (Apache-2.0, Java) [20] | + Norm ve doğrulama politikası. − Kural etkileşimi sürprizleri | Orta | Yüksek | ◐ Norm katmanı |
| Klasik planlama | STRIPS/PDDL [21][22]; önermesel STRIPS PSPACE-tam [23] | unified-planning 1.3.0 (Apache-2.0, 2025-12); pyperplan 2.1 (GPL-3+, 2022); Fast Downward 26.6 (GPL-3, 2026-09) [24][25] | + Genel, optimal. − Modelleme maliyeti, GPL | Yüksek | Çok yüksek | ◐ Nadir karmaşık görevler |
| Subsumption | Katmanlı reaktif davranış [26] | Yok | + Sağlam refleks. − Uzun vadeli hedef yok | Çok düşük | Orta | ❌ Ana mimari olarak (güvenlik katmanı olabilir) |
| SOAR | Kural tabanlı bilişsel mimari; chunking, RL [27] | soar-sml 9.6.5 (BSD, 2026-05) | + Sembolik + öğrenme. − Ağır, dik öğrenme eğrisi | Orta–yüksek | Yüksek | ❌ Araştırma referansı |
| ACT-R | İnsan biliş modeli [28] | pyactr 0.3.2 (GPL-3, 2024-02) | + Psikolojik gerçekçilik. − Amaç dışı | Yüksek | Yüksek | ❌ |

## 3. LLM'siz öğrenme

| Yöntem | Ne | Python | Güçlü / zayıf | Maliyet | Açk. | Uyum |
|---|---|---|---|---|---|---|
| RL / MARL | Ödülden politika; PettingZoo AEC ve Parallel API [29], RLlib dağıtık eğitim [30] | gymnasium 1.4.0, pettingzoo 1.27.0 (MIT); ray 2.59.0 (Apache-2.0, 2026-10) | + Strateji keşfi, kırmızı takım. − Ödül hackleme, tekrar üretilebilirlik [31] | Yüksek | Düşük | ◐ Çevrimdışı/donmuş ya da saldırgan üretici |
| Evrimsel/GA | Popülasyon, seçilim, mutasyon | DEAP 1.4.4 (LGPL), PyGAD 3.7.0 (BSD-3) | + Utility ağırlıklarını çevrimdışı ayarlar. − Uygunluk kandırılabilir | Orta | Orta | ✅ Parametre ayarı |
| NEAT | Topoloji + ağırlık evrimi [32] | neat-python 2.0.0 (BSD-3 tarzı, 2026-03) | + Küçük ağlar. − Opak | Orta | Düşük | ◐ |
| LCS (XCS) | Doğruluk tabanlı kural popülasyonu [33] | xcsf 1.5.0 (GPL-3, 2026-08) | + Okunabilir kurallar öğrenir. − Niş, GPL | Orta | Yüksek | ◐ |
| Bandit | UCB/Thompson keşif–sömürü [34] | MABWiser 2.7.4 (Apache-2.0, 2024-08); vowpalwabbit 9.11.9 (BSD-3, 2026-09) | + Ortak/doğrulayıcı/fiyat seçimi; tohumla deterministik. − Durağan olmayan ortam | Çok düşük | Yüksek | ✅ |
| Küçük klasik ML | Karar ağacı, lojistik, çevrimiçi | scikit-learn 1.9.1, river 0.26.1 (BSD-3) | + Hile/anomali skoru. − Yardımcı, karar verici değil | Düşük | Yüksek | ◐ |
| CBR | Geri getir–yeniden kullan–gözden geçir–sakla [35] | CBRkit 1.7.0 (MIT, 2026-10) | + Emsalle açıklama. − Benzerlik ölçüsü tasarımı | Düşük–orta | Çok yüksek | ✅ |

## 4. Çok ajanlı koordinasyon

| Yöntem | Ne | Python | Güçlü / zayıf | Açk. | Uyum |
|---|---|---|---|---|---|
| Contract Net / müzayede | İlan (CFP) → teklif → ödül [36]; FIPA cfp/propose/accept/reject | Kendi kodu; SPADE FIPA metadata destekler | + Dağıtık tahsis, kayda uygun. − Teklif şişirme, kazanıp terk | Çok yüksek | ✅ |
| Piyasa tabanlı | Fiyatla tahsis [38]; çoklu görev için CBBA [39] | OR-Tools 9.15 (Apache-2.0) | + Ölçekli; ZI ile bile verimli [58]. − Likidite, spekülasyon | Yüksek | ✅ |
| Blackboard | Ortak çalışma alanı (Hearsay-II) [40] | Kendi kodu | + Görev panosu. − Merkezî darboğaz | Yüksek | ◐ |
| Stigmerji | Ortam izleriyle dolaylı koordinasyon [41] | Kendi kodu | + Mesajsız ölçek. − Ayarı deneysel | Orta | ◐ Talep ısı haritası |
| FIPA ACL | Performatifli mesaj; yalnız `performative` zorunlu [37] | SPADE (XMPP) | + Ortak söz varlığı, denetim kaydı. − Tam yığın ağır | Çok yüksek | ◐ Sözlük olarak |
| Uzlaşma | Raft; PBFT 3f+1 ile Bizans toleransı [42] | pysyncobj 0.3.17 (MIT) | + Dağıtık tutarlılık. − Tek otoriteli dünyada gereksiz | Yüksek | ◐ |
| Mekanizma tasarımı | Teşvik uyumu (Vickrey, VCG) [43] | Kendi kodu; pygambit 16.7.0 (GPL-2+) | + Dürüst teklif/rapor. − Myerson–Satterthwaite: ikili ticarette verimlilik, teşvik uyumu, gönüllü katılım ve bütçe dengesi birlikte sağlanamaz [43] | Orta–yüksek | ✅ |

## 5. İtibar, güven ve doğrulama

| Yöntem | Ne | Python | Güçlü / zayıf | Açk. | Uyum |
|---|---|---|---|---|---|
| EigenTrust | Normalize yerel güven yayılımı; ön-güvenilir eşler, işbirlikçi grup önlemi [44] | networkx 3.7 (BSD-3) / numpy | + Küresel skor. − Tohum şart, tekelleşme (§5.1) | Orta | ✅ (tohum + keşif kotası) |
| PageRank/TrustRank | Tohumdan yayılan güven [45] | networkx | + Hazır. − Simetrik varyant sybil-geçirmez değil [49] | Orta | ✅ |
| Beta itibar | α/(α+β) [46] | ~10 satır | + En açıklanabilir. − Bağlamsız; unutma eklenmeli | Çok yüksek | ✅ |
| FIRE | Etkileşim + tanık + rol + sertifikalı itibar [47] | Kendi kodu | + Yeni gelene sertifika. − Çok parametre | Yüksek | ◐ |
| Elo/Glicko/OpenSkill/TrueSkill | Beceri derecelendirme [48] | openskill 6.2.0 (MIT); glicko2 2.1.0 (MIT); trueskill 0.4.5 (BSD, 2018) | + Görev türü başına beceri. − Dürüstlüğü ölçmez; TrueSkill markası yalnız Xbox Live/ticari olmayan projelere izinli [48] | Yüksek | ◐ |
| Sybil direnci | Ucuz kimlik saldırısı [49] | Yok | + Kimlik maliyeti, asimetrik/akış tabanlı itibar. − Tam çözüm yok | Orta | ✅ Zorunlu |
| Peer prediction / BTS | Zemin gerçeksiz dürüstlük teşviki [50] | Yok | + Öznel görevler. − Açıklaması zor | Düşük | ◐ |
| Uygun skorlama | Brier/log; dürüst olasılık beklenen skoru maksimize eder [50] | Kendi kodu | + Doğrulayıcı güven beyanı. − Sonuçta zemin gerçeği gerekir | Yüksek | ✅ |
| BOINC quorum | N kopya, M≤N tamamlanınca kanonik sonuç; kullanıcıya aynı işten en fazla bir kopya. Uyarlamalı: CV<10 güvenme, yoksa 1−1/CV olasılıkla güven [51] | Kendi kodu (BOINC C++, LGPL-3) | + Kanıtlanmış, basit. − Gizli anlaşma, düşük oranlı hile | Çok yüksek | ✅ |

### 5.1 Oyuncak simülasyon (rep_sim.py; 20 tohum, 100 ajan, 5000 görev; ortalama)

Varsayımlar: kötüler p olasılıkla yanlış döndürür; iki yanlış birbiriyle eşleşir (en kötü durum); anlaşmazlıkta üçüncü hakem; EigenTrust'ta kötü grup birbirini şişirir.

| Senaryo (kötü oranı, p) | Politika | Kabul edilen hata | Yürütme/görev | Kötülere ilk atama | Üst %10 yük payı |
|---|---|---|---|---|---|
| %20, 0,5 | Doğrulama yok | 0,1008 | 1,00 | 0,20 | 0,13 |
| %20, 0,5 | Beta + 2'li quorum | 0,0004 | 2,02 | 0,02 | 0,15 |
| %20, 0,5 | Beta + uyarlamalı | 0,0005 | 1,20 | 0,02 | 0,16 |
| %20, 0,5 | EigenTrust tohumsuz | 0,4630 | 2,48 | 0,94 | 0,49 |
| %20, 0,5 | EigenTrust 5 tohum | 0,0000 | 2,00 | 0,00 | 1,00 |
| %40, 0,5 | Beta + uyarlamalı | 0,0041 | 1,25 | 0,07 | 0,20 |
| %20, 0,1 | Beta + 2'li quorum | 0,0005 | 2,03 | 0,13 | 0,14 |
| %20, 0,1 | Beta + uyarlamalı | 0,0075 | 1,23 | 0,15 | 0,15 |

Gerçek görev doğrulamasını (kısmi doğruluk, öznel çıktı) temsil etmez; yön gösterir, büyüklük değil.

## 6. Ekonomiler ve simülasyonlar

| Konu | Öz ve araç | Ders | Uyum |
|---|---|---|---|
| Mesa | Python ABM, `rng` ile tekrar üretilebilir; 3.5.1 (Apache-2.0, 2026-03) [52] | Deney koşum ortamı | ✅ |
| NetLogo | Kendi dili; 7.0.4 (GPL-2+, 2026-05) [53] | Öğretim/keşif | ❌ |
| MASON | Java, AFL-3.0; GitHub son etiket v20 (2019) [54] | Dil uyumsuz | ❌ |
| Repast4Py | MPI dağıtık ABM; 1.3.0 (BSD-3, 2026-10) [55] | Çok büyük ölçekte | ◐ |
| JADE | FIPA uyumlu Java; 4.6.0 (LGPL-2, 2022) [56] | FIPA referansı | ❌ |
| Sugarscape | İhtiyaç, metabolizma, ticaret [57]; Mesa'da sugarscape_g1mt [52] | Taban ekonomi | ✅ |
| TAC / ZI | Ticaret ajanı yarışması ve ZI tüccarlar [58] | "Akıllı" ajanı ZI'ye karşı ölç | ✅ |
| EVE Online | Musluk/lavabo ve para hızı (MV=PQ) izleme; aylık raporlar ham CSV ile [59] | Her para giriş/çıkışını olay olarak sınıfla | ✅ |
| DF / RimWorld | DF: karşılanmayan ihtiyaç odağı ve iş kalitesini düşürür; RimWorld: zenginliğe bağlı tehdit puanı; L4D "AI Director" tempo yönetir [60] | İhtiyaç → utility; anlatıcı → görev üreteci | ✅ |
| LLM'siz Smallville | Smallville LLM'lidir [61]; LLM'siz: Prom Week/CiF (3500+ sosyokültürel değerlendirme), Talk of the Town (yanlış hatırlayan, yalan söyleyen NPC) [61], Sims reklamları [13] | Sosyal dinamik sembolik kurulabilir; dil yüzeyi sınırlı | ◐ |

## 7. Deterministik ve denetlenebilir otonomi kalıpları

| Kalıp | Öz | Python | Uyum |
|---|---|---|---|
| Event sourcing | Tam yeniden kurulum, zamansal sorgu, olay tekrarı [62] | eventsourcing 9.5.5 (BSD-3, 2026-08) | ✅ Denetim izi |
| Aktör modeli | Yalıtılmış, mesajlaşan aktörler [63]; mesaj sırası determinizmi bozar | Pykka 4.4.2 (Apache-2.0), Thespian 4.0.1 (MIT) | ◐ Tick sınırında sırala |
| Tick tabanlı | Sabit adım [64] | Kendi kodu; SimPy 4.1.2 (MIT) | ✅ |
| ECS | Veri odaklı bileşenler; Overwatch'ta kullanıldı [65] | esper 3.9 (MIT, 2026-09) | ◐ Python'da kazanç belirsiz (spekülatif) |
| Deterministik tekrar / lockstep | Aynı başlangıç ve girdi → bit-aynı sonuç; kayan nokta tehlikeli; AoE lockstep [64] | Kendi kodu | ✅ Tick başına durum hash'i |
| Tohumlu rastgelelik | stdlib garantisi sınırlı; NumPy SeedSequence bağımsız akış; PYTHONHASHSEED str/bytes hash'ini sabitler [66] | random, numpy | ✅ Ajan başına akış |

**Mikro ölçüm (bench.py, medyan µs):** utility kararı (8×4) 3,6 · transitions 4 geçiş 18,1 · py_trees 7 düğüm 16,7 · GTPyhop 4 adım 167,8 (stdout yönlendirmesi dahil). Aynı tohumla 1000 ajan × 100 tick karar hash'i aynı, farklı tohumla farklı.

## 8. Karşılaştırma tablosu

**Rubrik (1–5, yüksek = iyi):** *Özerklik* 1 = her tepkiyi tasarımcı yazar, 5 = kendi hedef/planını üretir. *Açıklanabilirlik* 5 = her karar açık kural/plan/skora izlenir. *Determinizm* 5 = aynı girdi+tohum kolayca bit-aynı. *Öğrenme* 1 = yok, 5 = deneyimden politika. *Uygulama kolaylığı* 5 = en az emek. *Ölçek* 5 = Python'da tick başına binlerce ajan ucuz. Ajan dışı satırlarda özerklik/öğrenme "NA". 51 satır CSV'de; seçki:

| Yöntem | Özr. | Açk. | Det. | Öğr. | Kolay. | Ölçek |
|---|---|---|---|---|---|---|
| BDI | 4 | 4 | 4 | 1 | 2 | 3 |
| HTN | 3 | 5 | 5 | 1 | 3 | 3 |
| Utility AI | 3 | 4 | 5 | 2 | 5 | 5 |
| Davranış ağacı | 2 | 5 | 5 | 1 | 4 | 4 |
| Klasik planlama | 4 | 5 | 4 | 1 | 2 | 2 |
| MARL | 4 | 1 | 2 | 5 | 1 | 2 |
| Bandit | 3 | 4 | 4 | 4 | 5 | 5 |
| CBR | 3 | 5 | 5 | 3 | 4 | 3 |

CSV'den kategori ortalamaları: karar mimarileri açıklanabilirlik 4,36 / öğrenme 1,45; öğrenme yöntemleri 3,12 / 4,12 → **açıklanabilirlik–öğrenme takası belirgin.** Sayım: 25 ✅, 20 ◐, 6 ❌.

## 9. Sentez

- Pratik tek mimari değil, katmanlar öneriyor: seçim (utility/BDI) → ayrıştırma (HTN/GOAP) → yürütme (BT/FSM) → dünya kuralları → denetim (event log).
- Öğrenme kenarlarda daha güvenli görünüyor: bandit ve GA gibi düşük boyutlu, tohumlanabilir öğrenme çekirdekte; derin RL çevrimdışı/donmuş ya da saldırgan üretici olarak (yargı).
- Dünyanın sağlığı itibar formülünden çok doğrulama ekonomisine (kopya sayısı, rastgele doğrulayıcı ataması) ve kimlik maliyetine bağlı görünüyor [49][51]; simülasyon destekliyor, kanıtlamıyor.
- EVE musluk/lavabo disiplini ve ZI boş modeli soruyu "ajanlar akıllı mı?"dan "kurallar verimli mi?"ye kaydırıyor [58][59].

## 10. Aday LLM'siz yığınlar (panel için seçenekler)

### A) Oyun-YZ çekirdeği: Utility + HTN + FSM · Contract Net · Beta + uyarlamalı quorum · tick + event log

```python
def agent_tick(a, view, rng):                # salt-okunur görünüm, ajana özel tohumlu rng
    a.needs.decay()                          # DF/Sims tarzı ihtiyaçlar
    if a.fsm.state == "idle":
        cands = [(utility(a, t), -t.id, t) for t in view.open_tasks]  # IAUS skoru
        if cands and max(cands)[0] > a.threshold:
            u, _, t = max(cands)             # eşitlikte id ile deterministik
            return Bid(a.id, t.id, price=a.price(t, u))
    elif a.fsm.state == "working":
        step = a.plan.pop(0) if a.plan else None             # GTPyhop planı
        return Act(a.id, step) if step else Submit(a.id, a.task)
    elif a.fsm.state == "verifying":
        return Verdict(a.id, a.job, a.check(a.job))
# Dünya: eylemleri id sırasıyla uygular, olayları loglar; replicate = cv<10 or rng.random()<1/cv
```

Yapabilir: ucuz, açıklanabilir (skor dökümü, plan izi), tekrar üretilebilir görev alma/doğrulama. Yapamaz: yeni strateji keşfi, öngörülmemiş görev türü. Riskler: eğri ayarı emeği; uyarlamalı replikasyonun düşük oranlı hileye açıklığı (§5.1). CSV ortalaması: Açk. 4,67, Det. 5,0, Öğr. 1,25.

### B) Taahhüt ve norm: BDI + CLIPS kuralları + FIPA performatifleri + tohumlu EigenTrust + uygun skorlama

```python
def bdi_step(a, percepts, rng):
    a.beliefs.revise(percepts)
    options = a.norms.filter(a.desires.generate(a.beliefs))  # CLIPS: yasak/zorunlu
    if a.reconsider(options):                                # taahhüt stratejisi
        a.intention = min(options, key=lambda o: (-o.priority, o.id))
    act = a.intention.next_action(a.beliefs)                 # plan kütüphanesi
    return Msg(act.performative, a.id, act.to, act.content)  # cfp/propose/inform/failure
```

Yapabilir: "ne söz verdi, neyi neden bozdu" denetimi; normları kodsuz değiştirme. Yapamaz: öğrenme (yalnız itibar). Riskler: ince Python BDI ekosistemi; CLIPS ayrı dil; EigenTrust tekelleşmesi keşif kotası gerektirir.

### C) Öğrenen pazar: Utility tabanı + tohumlu bandit + çift müzayede (ZI taban) + OpenSkill + çevrimdışı GA/MARL kırmızı takım + ECS + event log

```python
def decide(a, ctx, rng):
    if ctx.kind == "partner":
        return a.bandit.thompson(ctx.arms, rng)    # Beta posteriorları
    if ctx.kind == "quote":
        return a.zi_c_quote(ctx, rng) + a.margin   # ZI-C tabanı + öğrenen marj
    return utility_choice(a, ctx)
def learn(a, outcome):                             # yalnız DOĞRULANMIŞ ödülle
    a.bandit.update(outcome.arm, outcome.verified_value)
```

Yapabilir: ortama göre ortak/fiyat uyarlama; verimliliği boş modele karşı ölçme. Yapamaz: tam açıklanabilirlik. Riskler: ödül hackleme, durağan olmama, çevrimdışı/çevrimiçi dağılım farkı. CSV ortalaması: Öğr. 3,25, Açk. 3,89.

## 11. Fikirler ve deneyler (değer/emek; değerlendirmeler yargıdır)

| # | Deney | Değer | Emek |
|---|---|---|---|
| 1 | Tohumlu tick + event log tekrar testi (tick başına durum hash'i) | Yüksek | Düşük |
| 2 | rep_sim genişletme: düşük oranlı hileye karşı rastgele denetim oranı ve CV eşiği taraması | Yüksek | Düşük |
| 3 | ZI taban çizgisiyle ekonomi metrikleri (verimlilik, Gini) | Yüksek | Düşük |
| 4 | EVE tarzı musluk/lavabo sınıflaması + aylık rapor | Yüksek | Düşük |
| 5 | "Şüpheci reklam": beyan/doğrulanan oranıyla teklif ölçekleme [13] | Yüksek | Düşük |
| 6 | Tohumlu EigenTrust + yeni gelen keşif kotası; tekelleşme–hata ölçümü | Yüksek | Orta |
| 7 | Sybil: stake/kimlik bedeli vs akış tabanlı itibar [49] | Yüksek | Orta |
| 8 | Birinci fiyat vs Vickrey görev müzayedesi | Orta | Düşük |
| 9 | Utility ağırlıklarının GA ile çevrimdışı ayarı (uygunluk: doğrulanmış kazanç) | Orta | Orta |
| 10 | Bandit ile doğrulayıcı seçimi | Orta | Düşük |
| 11 | RimWorld tarzı anlatıcı ile görev üretimi/tempo | Orta | Orta |
| 12 | Öznel görevlerde peer prediction pilotu | Orta | Yüksek |
| 13 | MARL kırmızı takım | Orta–yüksek | Yüksek |
| 14 | SOAR/ACT-R prototipi | Düşük | Yüksek |

## 12. Doğrulanamayanlar ve spekülasyon

- fipa.org Cloudflare ile engellendi (içerik arama özetleriyle teyit); JADE sitesi zaman aşımı (4.6.0 arama özetinden); MASON güncel sürümü bilinmiyor (GitHub v20, 2019); CLIPS 6.4.2 tarihi/MIT-0 arama özetinden.
- 403 dönen DOI'ler (Hearsay-II, Nii, Urbanowicz, Prelec, Douceur, TrueSkill MSR): künye doğru kabul edildi, içerik açılmadı.
- IAUS "7 dakikada davranış paketi" satıcı beyanı; GOAP "~200 satır" ve ECS kazancı spekülatif; tüm puanlar yargı; simülasyon ve ölçümler oyuncak.

## Kaynaklar

[1] https://cdn.aaai.org/ICMAS/1995/ICMAS95-042.pdf · [2] https://jason-lang.github.io/ ; https://github.com/jason-lang/jason/releases/tag/v3.3.0 · [3] https://jacamo-lang.github.io/ ; https://github.com/jacamo-lang/jacamo/releases/tag/v1.3.1 · [4] https://spade-mas.readthedocs.io/en/latest/ ; https://pypi.org/project/spade/ · [5] https://github.com/javipalanca/spade_bdi · [6] https://www.gamedevs.org/uploads/three-states-plan-ai-of-fear.pdf · [7] https://www.jair.org/index.php/jair/article/view/10362 · [8] https://github.com/dananau/GTPyhop · [9] https://doi.org/10.1007/BF02136175 · [10] https://py-trees.readthedocs.io/en/devel/ · [11] https://arxiv.org/abs/1709.00084 · [12] https://www.gdcvault.com/play/1021848/Building-a-Better-Centaur-AI ; https://www.gameai.com/iaus.php · [13] https://www.qrg.northwestern.edu/papers/Files/Programming_Objects_in_The_Sims.pdf · [14] https://doi.org/10.1016/0167-6423(87)90035-9 · [15] https://github.com/pytransitions/transitions ; https://python-statemachine.readthedocs.io/en/latest/ · [16] https://doi.org/10.1016/0004-3702(82)90020-0 · [17] https://www.clipsrules.net/ ; https://pypi.org/project/clipspy/ · [18] https://github.com/jruizgit/rules · [19] https://github.com/nilp0inter/experta ; https://github.com/nilp0inter/experta/issues/34 · [20] https://www.drools.org/ ; https://repo1.maven.org/maven2/org/drools/drools-core/maven-metadata.xml · [21] https://ai.stanford.edu/~nilsson/OnlinePubs-Nils/PublishedPapers/strips.pdf · [22] https://planning.wiki/ref/pddl · [23] https://doi.org/10.1016/0004-3702(94)90081-7 · [24] https://www.jair.org/index.php/jair/article/view/10457 ; https://www.fast-downward.org/latest/releases/26.6/ · [25] https://github.com/aibasel/pyperplan ; https://github.com/aiplan4eu/unified-planning · [26] https://people.csail.mit.edu/brooks/papers/AIM-864.pdf · [27] https://arxiv.org/abs/2205.03854 ; https://soar.eecs.umich.edu/ · [28] http://act-r.psy.cmu.edu/ ; https://github.com/jakdot/pyactr · [29] https://pettingzoo.farama.org/ ; https://arxiv.org/abs/2009.14471 · [30] https://docs.ray.io/en/latest/rllib/index.html · [31] https://docs.pytorch.org/docs/2.14/notes/randomness.html · [32] https://nn.cs.utexas.edu/downloads/papers/stanley.ec02.pdf ; https://neat-python.readthedocs.io/ · [33] https://doi.org/10.1162/evco.1995.3.2.149 ; https://doi.org/10.1155/2009/736398 ; https://github.com/xcsf-dev/xcsf · [34] https://tor-lattimore.com/downloads/book/book.pdf ; https://doi.org/10.1023/A:1013689704352 ; https://github.com/fidelity/mabwiser · [35] https://www.iiia.csic.es/~enric/papers/AICom.pdf ; https://github.com/wi2trier/cbrkit · [36] https://doi.org/10.1109/TC.1980.1675516 ; http://www.fipa.org/specs/fipa00029/SC00029H.html · [37] http://www.fipa.org/specs/fipa00061/SC00061G.html · [38] https://doi.org/10.1109/JPROC.2006.876939 ; https://www.jair.org/index.php/jair/article/view/10106 · [39] https://doi.org/10.1109/TRO.2009.2022423 · [40] https://doi.org/10.1145/356810.356816 ; https://doi.org/10.1609/aimag.v7i2.537 · [41] https://doi.org/10.1162/106454699568700 · [42] https://raft.github.io/raft.pdf ; https://www.usenix.org/conference/osdi-99/practical-byzantine-fault-tolerance · [43] https://www.cs.cmu.edu/~sandholm/cs15-892F13/algorithmic-game-theory.pdf ; https://doi.org/10.1016/0022-0531(83)90048-0 · [44] https://nlp.stanford.edu/pubs/eigentrust.pdf · [45] http://ilpubs.stanford.edu:8090/422/ ; https://www.vldb.org/conf/2004/RS15P3.PDF · [46] https://aisel.aisnet.org/bled2002/41/ · [47] https://doi.org/10.1007/s10458-005-6825-4 · [48] https://handbook.fide.com/chapter/B022024 ; http://www.glicko.net/glicko/glicko2.pdf ; https://jmlr.org/papers/v12/weng11a.html ; https://trueskill.org/ · [49] https://www.microsoft.com/en-us/research/publication/the-sybil-attack/ ; http://netecon.seas.harvard.edu/P2PEcon05.html/Papers/Cheng_05.pdf · [50] https://doi.org/10.1287/mnsc.1050.0379 ; https://doi.org/10.1126/science.1102081 ; https://doi.org/10.1198/016214506000001437 · [51] https://boinc.berkeley.edu/grid_paper_04.pdf ; https://github.com/BOINC/boinc/wiki/Adaptive-Replication ; https://github.com/BOINC/boinc/wiki/JobIn · [52] https://mesa.readthedocs.io/latest/apis/model.html ; https://mesa.readthedocs.io/latest/examples/advanced/sugarscape_g1mt.html · [53] https://ccl.northwestern.edu/netlogo/ ; https://ccl.northwestern.edu/netlogo/docs/copyright.html · [54] https://github.com/eclab/mason · [55] https://repast.github.io/repast4py.site/ · [56] https://jade.tilab.com/ · [57] https://www.brookings.edu/books/growing-artificial-societies/ · [58] https://doi.org/10.1109/4236.914648 ; https://doi.org/10.1086/261868 · [59] https://cdn1.eveonline.com/community/QEN/QEN_Q4-2010.pdf ; https://www.eveonline.com/news/view/monthly-economic-report-august-2026 · [60] https://dwarffortresswiki.org/index.php/Needs ; https://rimworldwiki.com/wiki/AI_Storytellers ; https://rimworldwiki.com/wiki/Raid_points ; https://steamcdn-a.akamaihd.net/apps/valve/2009/ai_systems_of_l4d_mike_booth.pdf · [61] https://arxiv.org/abs/2304.03442 ; http://www.ben-samuel.com/wp-content/uploads/2015/09/FDG-2011-Prom-Week-Social-Physics-as-Gameplay.pdf ; https://ojs.aaai.org/index.php/AIIDE/article/view/12825 · [62] https://martinfowler.com/eaaDev/EventSourcing.html ; https://github.com/pyeventsourcing/eventsourcing · [63] https://www.ijcai.org/Proceedings/73/Papers/027B.pdf ; https://pykka.readthedocs.io/ · [64] https://gafferongames.com/post/fix_your_timestep/ ; https://gafferongames.com/post/deterministic_lockstep/ ; https://www.gamedeveloper.com/programming/1500-archers-on-a-28-8-network-programming-in-age-of-empires-and-beyond · [65] https://github.com/benmoran56/esper ; https://www.gdcvault.com/play/1024001/-Overwatch-Gameplay-Architecture-and · [66] https://docs.python.org/3/library/random.html ; https://docs.python.org/3/using/cmdline.html#envvar-PYTHONHASHSEED ; https://numpy.org/doc/stable/reference/random/parallel.html · Sürüm verisi: https://pypi.org/pypi/{paket}/json (2026-10-06 itibarıyla)
