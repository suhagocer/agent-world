> Grok Bot araştırma notu; karar değildir. Kararlar yalnızca decisions/DECISION-LOG.md'de.

# grok-bot-arastirma

Bu klasör, Grok Bot'un beş modelli panel için yaptığı dışa dönük araştırmaları tutar. Karar veya kod içermez.

## Dosyalar

- [2026-10-06_ajan-sistemleri.md](2026-10-06_ajan-sistemleri.md): ajan sistemleri taraması (çerçeveler, protokoller, desenler).
- [2026-10-06_llmsiz-otonom-ajanlar.md](2026-10-06_llmsiz-otonom-ajanlar.md): LLM'siz otonom ajan sistemleri araştırması (karar mimarileri, öğrenme, koordinasyon, itibar/doğrulama, aday yığınlar).
- [2026-10-06_llmsiz-karsilastirma.csv](2026-10-06_llmsiz-karsilastirma.csv): raporun 51 satırlık yöntem karşılaştırma tablosu (puanlar yazar yargısıdır).
- [deney/rep_sim.py](deney/rep_sim.py): doğrulama + itibar politikalarını karşılaştıran oyuncak görev pazarı simülasyonu (tohumlu).
- [deney/bench.py](deney/bench.py): utility, FSM, davranış ağacı ve HTN kararları için mikro ölçüm ve determinizm kontrolü.
- [deney/rep_sim_results.json](deney/rep_sim_results.json): rep_sim.py çıktısı (20 tohumun ortalaması ve standart sapması).

`deney/` klasöründeki betikler proje kodu değildir; raporun atıf yaptığı oyuncak deneylerdir. Sayılar yalnızca yön gösterir, büyüklük değil.
