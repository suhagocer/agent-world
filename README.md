# Agent World — Faz 0 çekirdek

Çalışan kod köktedir. Kanon değildir.

```bash
python3 test_faz0.py
```

Python 3.10+. PostgreSQL yok. LLM API yok. Beklenen: `24/24 geçti`.

Dosyalar: `schema.sql`, `store.py`, `context_builder.py`, `test_faz0.py`.

`verified` isteği yeniden hesaplanır. Kaynak yoksa veya aile doğrulanmamışsa sonuç `unverified` olur. Aynı aile, farklı model: `verified-weak`. Farklı aile: `verified`. `_attested` bayrağı yok sayılır.

Zincir `verify_chain()` ile kontrol edilir. Saat hash'e girmez. Süre dolunca yalnız `claimed` / `active` görev açılır.

`architecture/`, `decisions/`, `docs/`, `experiments/`, `model-analysis/`, `provenance/`, `research/`, `src/`, `tests/` ve `COLLABORATION.md` boş iskelettir. Rol listesi kilit değildir.

Yok: LLM çağrısı, 6 isimli ajan, itibar, domain, API anahtarı, model_registry seed.
