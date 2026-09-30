-- AGENT WORLD — Faz 0 şema (çalışma kopyası, kanon değil)
-- Provenance:
--   Claude referans SQL (Tur 5)
--   Grok T-12 yaması (Tur 5/6)
--   DeepSeek: TIMESTAMPTZ, CHECK, idx_events_ts, model_id (kısmen alındı)
--
-- TEK YAZMA YOLU: appendEvent().
-- events = append-only log. Üç projeksiyon event'ten türer; birbirine FK YOK.
-- model_registry insan seed; family_verified DEFAULT false (fail-closed).
-- Faz 0 runtime bu şemayı Postgres'siz de çalıştırır (bkz. store.py).

CREATE TABLE events (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  ts TIMESTAMPTZ NOT NULL DEFAULT now(),
  actor_id TEXT NOT NULL,
  type TEXT NOT NULL,
  payload JSONB NOT NULL,
  mission_id UUID,
  parent_event_id UUID REFERENCES events(id),
  token_cost INT,
  tool TEXT,
  prev_hash TEXT NOT NULL DEFAULT '0000000000000000000000000000000000000000000000000000000000000000',
  hash TEXT NOT NULL
);
CREATE INDEX idx_events_mission ON events (mission_id);
CREATE INDEX idx_events_type ON events (type);
CREATE INDEX idx_events_ts ON events (ts);

CREATE TABLE model_registry (
  model_id TEXT PRIMARY KEY,
  provider TEXT NOT NULL,
  family TEXT NOT NULL,
  family_verified BOOLEAN NOT NULL DEFAULT false,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE agent_projection (
  agent_id TEXT PRIMARY KEY,
  capability TEXT NOT NULL DEFAULT 'producer',
  permissions JSONB NOT NULL DEFAULT '[]',
  model_id TEXT REFERENCES model_registry(model_id),
  status TEXT NOT NULL DEFAULT 'idle'
    CHECK (status IN ('active', 'idle', 'suspended')),
  last_seen_at TIMESTAMPTZ,
  updated_from_event UUID NOT NULL REFERENCES events(id)
);

CREATE TABLE mission_projection (
  id UUID PRIMARY KEY,
  objective TEXT NOT NULL,
  claim_type TEXT NOT NULL
    CHECK (claim_type IN ('factual', 'executable', 'judgmental', 'procedural')),
  evidence_contract JSONB NOT NULL DEFAULT '{}',
  lease_holder TEXT,
  lease_until TIMESTAMPTZ,
  budget_tokens INT NOT NULL,
  budget_time_seconds INT NOT NULL,
  status TEXT NOT NULL DEFAULT 'open'
    CHECK (status IN (
      'open', 'claimed', 'active', 'submitted',
      'evaluating', 'verified', 'rejected', 'failed', 'archived'
    )),
  updated_from_event UUID NOT NULL REFERENCES events(id),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE claim_projection (
  id UUID PRIMARY KEY,
  mission_id UUID NOT NULL,
  statement TEXT NOT NULL,
  source TEXT,
  evidence JSONB,
  claim_type TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'quarantined'
    CHECK (status IN (
      'quarantined', 'unverified', 'verified-weak', 'verified',
      'disputed', 'rejected', 'superseded'
    )),
  confidence REAL,
  contradicts UUID,
  ttl TIMESTAMPTZ,
  updated_from_event UUID NOT NULL REFERENCES events(id),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Seed yok. family_verified = false kalır; insan onaylamadan verified yazılmaz.
