"""
AGENT WORLD — Faz 1a: takılıp çıkarılabilir "beyin" (cognitive engine) arayüzü.

Suha'nın 7 Ekim 2026 şartlı onayı, madde 2 ve 5:
  - Faz 1a'da API kullanılmayacak.
  - Ajanın beyni takılıp çıkarılabilir bir yapıda olsun.
  - İlk beyin kural tabanlı olsun.
  - Testlerde gerçek model yerine sahte model kullanılsın.
  - (ChatGPT'nin önerisi, Suha tarafından onaylandı) Faz 1'in amacı
    ajanlara LLM bağlamak değil, düşünme katmanını soyutlamak olsun;
    ilk iki motor RuleBasedCognitiveEngine ve LLMCognitiveEngine olsun,
    ikisi de aynı protokole uysun; ileride Planner/Learning/Hybrid
    motorlar eklenebilsin.

Bu dosyada HİÇBİR ağ çağrısı yoktur ve olmayacaktır. LLMCognitiveEngine
kendisine dışarıdan verilen bir `model_client`'ı çağırır; o client'ın
gerçek bir API'ye mi yoksa sahte bir nesneye mi bağlı olduğu bu
dosyanın sorumluluğunda değildir. Faz 1a'da repoda yalnızca
FakeModelClient (testler için) vardır. Gerçek bir Groq/Gemini client'ı
Faz 1b'nin konusudur — ayrı bir modül, ayrı bir onay.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Protocol, runtime_checkable


@dataclass(frozen=True)
class Verdict:
    """Bir beynin bir iddia hakkındaki kararı."""
    verdict: str  # "pass" | "dispute" -- başka değer kabul edilmez
    reason: str
    engine: str  # hangi motorun karar verdiği; event log'a/denetime düşer

    def __post_init__(self) -> None:
        if self.verdict not in ("pass", "dispute"):
            raise ValueError(f"Verdict.verdict 'pass' ya da 'dispute' olmalı, geldi: {self.verdict!r}")


@runtime_checkable
class CognitiveEngine(Protocol):
    """Her ajan beyninin uyması gereken tek sözleşme.

    Önemli: Bir CognitiveEngine yalnızca İÇERİK hakkında (iddia makul
    mü?) karar verir. Provenance kontrolü (kaynak gerçekten böyle mi
    diyor?) bunun dışında, world-seviyesinde, hiçbir motor tarafından
    atlanamayan bir kapıdır — bkz. agents/critic.py."""

    name: str

    def evaluate(self, statement: str) -> Verdict: ...


class RuleBasedCognitiveEngine:
    """Faz 0'ın "bilinen-gerçekler" kuralının birebir taşınmış hali.
    Davranış DEĞİŞMEDİ — sadece pluggable bir arayüzün arkasına alındı.
    Bu, Suha'nın şartına göre Faz 1a'nın İLK ve TEK aktif beynidir."""

    name = "rule-based-v1"
    _KNOWN_CAPITALS = {"Türkiye": "Ankara"}
    _CAPITAL_CLAIM = re.compile(r"^(?P<subject>.+?),?\s*Türkiye'nin başkentidir\.?$")

    def evaluate(self, statement: str) -> Verdict:
        m = self._CAPITAL_CLAIM.match(statement)
        if m:
            subject = m.group("subject").strip()
            known = self._KNOWN_CAPITALS["Türkiye"]
            if subject != known:
                return Verdict(
                    verdict="dispute",
                    reason=(f"bilinen-gerçekler çelişkisi: Türkiye'nin başkenti "
                            f"'{known}'dır, '{subject}' değil."),
                    engine=self.name,
                )
        return Verdict(verdict="pass", reason="bilinen-gerçekler çelişkisi yok.", engine=self.name)


@runtime_checkable
class ModelClient(Protocol):
    """LLMCognitiveEngine'in ihtiyaç duyduğu minimum sözleşme.
    Faz 1a'da bunu yalnızca FakeModelClient (aşağıda) uygular. Faz
    1b'de gerçek bir Groq/Gemini sarmalayıcısı bu Protocol'ü uygulayacak
    — o kod bu dosyada değildir ve Faz 1a onayı bunu kapsamaz."""

    def complete(self, prompt: str) -> str: ...


class LLMCognitiveEngine:
    """Dış bir model_client'a yaslanan beyin. Kendisi hiçbir ağ çağrısı
    yapmaz — tüm iletişim constructor'da verilen model_client üzerinden
    geçer. Faz 1a'da repoda gerçek bir ağa çıkan model_client YOKTUR;
    yalnızca FakeModelClient testlerde kullanılır. Bu sınıfın var
    olması bile Faz 1a'da API açtığımız anlamına gelmez — somut, ağa
    çıkan bir client eklenmediği sürece hiçbir şey çağrılmaz."""

    def __init__(self, model_client: ModelClient, name: str = "llm-v1") -> None:
        self._client = model_client
        self.name = name

    def evaluate(self, statement: str) -> Verdict:
        raw = self._client.complete(
            "Bu ifade doğru mu, genel bilgiyle tutarlı mı? Yalnızca "
            "'PASS: <kısa sebep>' ya da 'DISPUTE: <kısa sebep>' "
            f"formatında tek satır cevap ver.\nİfade: {statement}"
        ).strip()
        is_dispute = raw.upper().startswith("DISPUTE")
        reason = raw.split(":", 1)[1].strip() if ":" in raw else (
            "model itiraz etti." if is_dispute else "model onayladı."
        )
        return Verdict(
            verdict="dispute" if is_dispute else "pass",
            reason=reason,
            engine=self.name,
        )


class FakeModelClient:
    """Faz 1a testleri için sahte model_client. Ağa ASLA çıkmaz; sabit,
    önceden tanımlı cevaplar döner. Suha'nın şartı: 'testlerde gerçek
    model yerine sahte model kullanılsın.' `calls` listesi, denetim
    için gönderilen her prompt'u saklar."""

    def __init__(
        self,
        canned: dict[str, str] | None = None,
        default: str = "PASS: sahte model, varsayılan onay.",
    ) -> None:
        self._canned = canned or {}
        self._default = default
        self.calls: list[str] = []

    def complete(self, prompt: str) -> str:
        self.calls.append(prompt)
        for key, response in self._canned.items():
            if key in prompt:
                return response
        return self._default
