# Agent World — Faz 0 çekirdek

Çalışan kod köktedir. Kanon değildir.

```bash
python3 test_faz0.py
```

Python 3.10+. PostgreSQL yok. LLM API yok. Beklenen: `12/12 geçti`.

Dosyalar: `schema.sql`, `store.py`, `context_builder.py`, `test_faz0.py`.

`verified` yazmak için kaynak (`source`) ve iki doğrulanmış, farklı aile gerekir. Zincir `verify_chain()` ile kontrol edilir. Süre dolunca doğrulanmış görev yeniden açılmaz.

`architecture/`, `decisions/`, `docs/`, `experiments/`, `model-analysis/`, `provenance/`, `research/`, `src/`, `tests/` ve `COLLABORATION.md` boş iskelettir. Kod orada değil. Rol listesi kilit değildir.

Yok: LLM çağrısı, 6 isimli ajan, itibar, domain, API anahtarı, model_registry seed, üç kademeli verified-weak.
