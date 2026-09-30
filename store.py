"""In-memory event log + projections. No LLM. No Postgres."""

from __future__ import annotations

import hashlib
import json
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Any


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _dumps(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _hash(prev: str, actor_id: str, typ: str, payload: dict) -> str:
    raw = f"{prev}|{actor_id}|{typ}|{_dumps(payload)}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


GENESIS = "0" * 64


@dataclass
class Event:
    id: str
    ts: datetime
    actor_id: str
    type: str
    payload: dict
    mission_id: str | None
    parent_event_id: str | None
    prev_hash: str
    hash: str


@dataclass
class Agent:
    agent_id: str
    capability: str = "producer"
    model_id: str | None = None
    status: str = "idle"
    updated_from_event: str = ""


@dataclass
class Mission:
    id: str
    objective: str
    claim_type: str = "factual"
    lease_holder: str | None = None
    lease_until: datetime | None = None
    budget_tokens: int = 8000
    budget_time_seconds: int = 3600
    status: str = "open"
    updated_from_event: str = ""


@dataclass
class Claim:
    id: str
    mission_id: str
    statement: str
    status: str = "quarantined"
    tokens: int = 100
    contradicts: str | None = None
    updated_from_event: str = ""


@dataclass
class Model:
    model_id: str
    provider: str
    family: str
    family_verified: bool = False


@dataclass
class Store:
    events: list[Event] = field(default_factory=list)
    agents: dict[str, Agent] = field(default_factory=dict)
    missions: dict[str, Mission] = field(default_factory=dict)
    claims: dict[str, Claim] = field(default_factory=dict)
    models: dict[str, Model] = field(default_factory=dict)

    def append_event(
        self,
        actor_id: str,
        typ: str,
        payload: dict,
        mission_id: str | None = None,
        parent_event_id: str | None = None,
    ) -> Event:
        prev = self.events[-1].hash if self.events else GENESIS
        eid = str(uuid.uuid4())
        h = _hash(prev, actor_id, typ, payload)
        ev = Event(
            id=eid,
            ts=_now(),
            actor_id=actor_id,
            type=typ,
            payload=payload,
            mission_id=mission_id,
            parent_event_id=parent_event_id,
            prev_hash=prev,
            hash=h,
        )
        self.events.append(ev)
        self._project(ev)
        return ev

    def _project(self, ev: Event) -> None:
        p = ev.payload
        if ev.type == "agent.upsert":
            a = self.agents.get(p["agent_id"]) or Agent(agent_id=p["agent_id"])
            a.capability = p.get("capability", a.capability)
            a.model_id = p.get("model_id", a.model_id)
            a.status = p.get("status", a.status)
            a.updated_from_event = ev.id
            self.agents[a.agent_id] = a
        elif ev.type == "mission.upsert":
            m = self.missions.get(p["id"]) or Mission(id=p["id"], objective=p.get("objective", ""))
            for k in ("objective", "claim_type", "budget_tokens", "budget_time_seconds", "status"):
                if k in p:
                    setattr(m, k, p[k])
            m.updated_from_event = ev.id
            self.missions[m.id] = m
        elif ev.type == "claim.upsert":
            c = self.claims.get(p["id"]) or Claim(
                id=p["id"], mission_id=p["mission_id"], statement=p.get("statement", "")
            )
            for k in ("statement", "status", "tokens", "contradicts", "mission_id"):
                if k in p:
                    setattr(c, k, p[k])
            c.updated_from_event = ev.id
            self.claims[c.id] = c
        elif ev.type == "model.upsert":
            self.models[p["model_id"]] = Model(
                model_id=p["model_id"],
                provider=p["provider"],
                family=p["family"],
                family_verified=bool(p.get("family_verified", False)),
            )
        elif ev.type == "lease.acquire":
            m = self.missions[p["mission_id"]]
            m.lease_holder = p["agent_id"]
            m.lease_until = _now() + timedelta(seconds=int(p.get("ttl", m.budget_time_seconds)))
            m.status = "claimed"
            m.updated_from_event = ev.id
        elif ev.type == "lease.release":
            m = self.missions[p["mission_id"]]
            m.lease_holder = None
            m.lease_until = None
            m.status = "open"
            m.updated_from_event = ev.id

    def acquire_lease(self, mission_id: str, agent_id: str, ttl: int = 3600) -> Event:
        m = self.missions[mission_id]
        if m.lease_holder and m.lease_until and m.lease_until > _now() and m.lease_holder != agent_id:
            raise PermissionError("lease held")
        return self.append_event(
            actor_id=agent_id,
            typ="lease.acquire",
            payload={"mission_id": mission_id, "agent_id": agent_id, "ttl": ttl},
            mission_id=mission_id,
        )

    def expire_leases(self, now: datetime | None = None) -> int:
        now = now or _now()
        n = 0
        for m in list(self.missions.values()):
            if m.lease_holder and m.lease_until and m.lease_until <= now:
                self.append_event(
                    actor_id="world",
                    typ="lease.release",
                    payload={"mission_id": m.id, "reason": "timeout"},
                    mission_id=m.id,
                )
                n += 1
        return n

    def families_conflict(self, producer_model: str, critic_model: str) -> bool:
        """Fail-closed: unknown or unverified family counts as the same family."""
        a = self.models.get(producer_model)
        b = self.models.get(critic_model)
        if a is None or b is None or not a.family_verified or not b.family_verified:
            return True
        return a.family == b.family

    def can_write_verified(self, producer_model: str, critic_model: str) -> bool:
        return not self.families_conflict(producer_model, critic_model)
