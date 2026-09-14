# Adapter — aigovops-beacon (the signer)

**Today.** Beacon's `docs/RECEIPT_SCHEMA.md` describes an OVERT-envelope receipt per observed interaction: `id` (ULID), `ts_utc`, `user{sub, email, oidc_issuer}`, `vendor`, `model`, `version`, `prompt`/`prompt_hash`, `result`/`result_hash`, `event_type`, `environment`, `latency_ms`, `tokens_in/out`, `evidence_id`, `parent_receipt_id`, Ed25519 `signature`; append-only NDJSON; Merkle root anchored hourly; offline `VERIFY.md`. Wire-compatible with aigovops-Replay.

**Delta (0.3.0, behind `--one-receipt`).**

| Beacon field | One Receipt v0.2 | Change |
|---|---|---|
| `id` (ULID) | `receipt_id` = `urn:one-receipt:r:<ulid>` | prefix only |
| `ts_utc` | `started_at`, `ended_at`, `issued_at`; `clock_source: issuer` | split |
| `user.sub`, `user.email` | `identity.principal_ref` = per-session pseudonym; `principal_binding_mode: authenticated-ref` | **remove** the OIDC subject and e-mail from the receipt — v0.2 forbids stable personal identifiers; keep the mapping pseudonym→subject in Beacon's evidence store under access control |
| `vendor`, `model`, `version` | `identity.model.ref` = `<vendor>:<model>`, `identity.model.version` | rename |
| `prompt_hash`, `result_hash` (plain sha-256) | `runtime.input_commitment`, `runtime.output_commitment` with `scheme: salted-sha256` | **salt them**; store salts with `evidence_id`; plain hashes are rejected by the verifier |
| `prompt`, `result` (full text when capture is on) | never in the receipt | keep in the evidence store only; `runtime.content_included: false` |
| `event_type` | `transaction_type` (`inference.observed` → `inference`; `gate.evaluated` → `policy-decision`; `discovery.*` → `extensions.aigovops.beacon.event_type`) | map |
| `environment`, `latency_ms`, `tokens_*` | `runtime.environment.region` / `attestation: none`, `runtime.counts` | rename |
| `parent_receipt_id` | `parent_receipt_ids[]`, `root_receipt_id`, `transaction_id` | Beacon opens a transaction per session and chains |
| hourly Merkle root | `witness.log_operator{id: beacon-self, kind: merkle-append-only}`, `log_checkpoint`, `inclusion_proof` | OR-2 with Beacon as its own log; OR-3 needs an external log (log-lab or a SCITT service) and a witness |
| OVERT envelope | `extensions.glacis.overt` (whole envelope) | kept verbatim until the OVERT profile is registered |
| checklist packs (NIST, EU Art. 13, ISO 42001, Human Flourishing Gate) | `policy.controls[]` with `vocabulary` | the gate's control ids ride on the `policy-decision` receipt |

New on every consequential receipt: `contestability` (Beacon's `/studio` shows the notice and the challenge route; `human_review.reviewer_authority` comes from the gate's escalation rule). New on every receipt: `privacy_profile`, `predicate_manifest`, `limitations`.

**Tests.** Beacon's CI runs `one-receipt vectors` and verifies its own emitted receipts with the reference verifier; the verified level must equal the claimed level on every Beacon receipt or the build fails.
