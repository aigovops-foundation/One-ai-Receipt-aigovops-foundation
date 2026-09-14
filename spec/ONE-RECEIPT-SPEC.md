# One Receipt — Core Specification

**Version:** 0.2-draft · **Status:** incubation draft, not a standard · **Editor of record:** AiGovOps Foundation Technical Incubator (neutral convener; not the long-term sole editor, registry, assessor qualifier or trust root) · **Licence:** CC BY 4.0 (text), Apache-2.0 (schemas and code)

The key words MUST, MUST NOT, SHOULD, SHOULD NOT and MAY are to be read as in RFC 2119 / RFC 8174.

---

## 0. Scope and bounded claims

One Receipt defines one signed, content-free statement — a **receipt** — about one **bounded AI transaction event**, and the rules by which a stranger can verify it offline, chain it to the other events of the same transaction, register it with an independent log, and use it to notice, understand, challenge and remedy the outcome.

A verified receipt proves exactly this:

> An identified issuer signed the declared claims, bound them to identifiers and time, and supplied the evidence the claimed assurance level requires.

It does **not** prove that the AI output was true, fair, safe, lawful, accurate, unbiased or harmless; that human review was meaningful; that a policy was well-designed; that a system is certified; that evidence is admissible; or that any insurance, regulatory or contractual consequence follows. Every receipt carries a non-empty `limitations` array and every verifier result repeats it. Text that claims otherwise is non-conformant marketing, not a receipt.

One Receipt does not replace existing standards. It profiles and connects them: transparency registration follows IETF SCITT (RFC 9943, RFC 9942); decision evidence maps to OVERT; telemetry names map to OpenTelemetry GenAI conventions; asset provenance maps to C2PA; commerce mandates are accepted unchanged from AP2 and Mastercard Verifiable Intent; control identifiers may come from UCID, OVERT, AIUC-1, CSA AICM, ISO/IEC 42001 or NIST AI RMF. Section 14 and `spec/delta-matrix.md` hold the mappings; none is normative for the other body until that body accepts it.

## 1. Terms

- **Transaction** — a run of related events with one `transaction_id`: a chat turn and its tool calls, an agent task and its delegations, a batch decision run, a challenge and its review.
- **Event** — one bounded observation inside a transaction (an inference, a tool call, a delegation hop, a human review, an output delivery, a policy decision, a challenge, a review, a remedy, an incident, or an aggregate of segments). One event may be described by several receipts from different issuers; they share `event_id`.
- **Receipt** — one signed envelope about one event, from one issuer, at one assurance level.
- **Predicate** — a versioned, typed group of claims inside a receipt. Ten are defined here; others may be registered.
- **Issuer** — the party whose key signs the receipt, acting in one **role** (§9).
- **Log operator** — the party that registers receipts in an append-only, verifiable log and publishes checkpoints.
- **Witness** — an independent party that co-signs log checkpoints so equivocation (showing different logs to different verifiers) can be detected.
- **Assessor** — an independent party that samples and verifies receipts and the controls behind them, without content access.
- **Registry steward** — the party that publishes key discovery, profile, assessor and public-interest review records a receipt points to.
- **Verifier** — anyone holding a receipt, a public key and, above OR-1, log access. No account, no network and no operator cooperation is required at OR-1.
- **Commitment** — a salted or keyed digest of content the receipt never carries. A plain hash of guessable content is not a commitment (§5).

## 2. The envelope

The normative schema is `spec/schema/one-receipt-envelope.schema.json`; predicates live under `spec/schema/predicates/`. The JSON form below is the reference serialisation; a CBOR form using the same field names is permitted when `signature.canonicalization` is `CBOR-CDE`.

| Field | Type | Rule |
|---|---|---|
| `spec_version` | const `"0.2-draft"` | Verifiers MUST reject unknown versions rather than guess. |
| `receipt_id` | URN `urn:one-receipt:…` | Unique per receipt. |
| `transaction_id` | URN | Shared by every event of one transaction. |
| `event_id` | URN | Shared by every receipt about the same observed event. |
| `parent_receipt_ids` | URN[] | Zero for a root; one or more otherwise. A receipt MUST NOT list itself. |
| `root_receipt_id` | URN | Equals `receipt_id` when `parent_receipt_ids` is empty. |
| `transaction_type` | enum | `inference`, `tool-call`, `agent-delegation`, `human-review`, `output-delivery`, `policy-decision`, `challenge`, `review`, `remedy`, `incident`, `aggregate`. |
| `sequence` | integer ≥ 0 | Position among receipts of the same issuer role within one transaction. |
| `boundary` | enum | `request-response`, `streaming-segment`, `agent-action`, `batch`, `aggregate` (§3). |
| `started_at` / `ended_at` / `issued_at` | RFC 3339 | `started_at ≤ ended_at ≤ issued_at` MUST hold. |
| `clock_source` | enum | `issuer`, `trusted-time-authority`, `qualified-time-stamp`. Issuer clocks are unverified assertions. |
| `issuer` | object | `id`, `key_id`, `role` (§9), optional `key_discovery`. |
| `assurance_level` | `OR-0`…`OR-5` | The **claimed** level. Verifiers compute the **verified** level (§8) and MUST report both. |
| `privacy_profile` | object | §5. Required on every receipt. |
| `predicate_manifest` | array | Every predicate present MUST be declared; every declared predicate absent MUST carry an `omission_reason` (§4.1). |
| `predicates` | object | Keyed by registered predicate name. |
| `limitations` | string[] ≥ 1 | The bounded-claims text. Verifiers MUST surface it. |
| `extensions` | object | Namespaced (`vendor.name`), non-normative. Verifiers MUST ignore what they do not understand and MUST NOT change validity on it. |
| `signature` | object | `algorithm`, `canonicalization`, `key_id`, `value` (base64url, no padding), optional `countersignatures[]` (§12). |

The signature covers the canonical bytes of the whole envelope with `signature.value` set to the empty string and `signature.countersignatures` removed. Countersignatures cover the same bytes and are appended by log operators, witnesses, time authorities, reviewers or assessors.

## 3. The transaction graph and event boundaries

A transaction is a directed acyclic graph of receipts. Verifiers of a graph MUST check that every parent named is present (or declared external), that all receipts name one root, that every receipt is individually valid, and MUST report the **weakest verified level in the graph** as the level of the transaction. A chain is only as strong as its least-witnessed link.

### 3.1 Boundary rules

| `boundary` | The event is… | Rule |
|---|---|---|
| `request-response` | one request and the response it produced | Default for chat, API and IDE. |
| `agent-action` | one tool call, delegation hop or side-effecting action | One receipt per action; `runtime.child_receipt_ids` on the parent names them. |
| `streaming-segment` | one segment of a stream (voice, token stream, live agent) | `transaction.segment` carries `index`, `of` when known, the `batching_profile` and `window_ms`. A stream MUST close with an `aggregate` receipt. |
| `batch` | one item of a batch run | `sequence` is the item index. A batch MUST close with an `aggregate`. |
| `aggregate` | a roll-up of segments or items | MUST name every aggregated receipt in `parent_receipt_ids` or declare `transaction.dropped_events_declared: true` with the count in `extensions`. |

### 3.2 Streaming and voice batching profile

Voice and streaming interfaces MUST NOT emit one receipt per token. They MUST choose one `batching_profile` — `per-turn`, `per-utterance`, `time-window` (with `window_ms`), `token-window` or `per-action` — declare it in every segment, keep the same profile for the whole stream, and emit a closing `aggregate` receipt whose `ended_at` is the stream's end. The user-facing receipt identifier for a voice interaction is the aggregate's `receipt_id`, spoken or written on request (§10).

### 3.3 Delegation

An agent that delegates to another agent emits an `agent-delegation` receipt naming the delegate in `identity.agent` and increments `transaction.delegation_depth`. The delegate's receipts name the delegation receipt as parent. The human principal's mandate (§4.4) is inherited by reference (`mandate.mandate_ref`) down the chain and MUST NOT widen at any hop; a receipt at depth *n* with a broader scope than its parent is valid syntax but a policy failure the verifier SHOULD flag.

## 4. Predicates

Each predicate is versioned independently (`type` + `version` in the manifest). Verifiers MUST accept any registered minor version and MUST reject a critical predicate at an unknown major version.

### 4.1 The manifest and omission reasons

The four **critical** predicates are `transaction`, `policy`, `runtime` and `contestability`. A receipt that omits any of them MUST say why with an `omission_reason` (`not-applicable`, `not-collected`, `withheld-privacy`, `withheld-legal`, `withheld-security`, `unavailable-outage`, `deferred-to-parent`, `deferred-to-aggregate`). Such a receipt is still valid but the verified level is capped at OR-1: signed, not complete. A predicate present but undeclared, or declared-absent without a reason, makes the receipt invalid.

### 4.2 `transaction` 1.0 — how the event was cut
`interface` (required; §10), `boundary_rule`, `segment`, `id_carrier`, `delegation_depth`, `dropped_events_declared`.

### 4.3 `identity` 1.0 — who acted, on whose behalf, with what
`principal_binding_mode` (required: `none`, `pseudonymous`, `authenticated-ref`, `collective`), `principal_ref` (a pseudonym or pointer — never a stable user id, e-mail, IP address, exact location or capability token; the reference verifier rejects values that look like one), `operator_id`, `agent{id, card_ref, workload_identity}`, `model{ref, version, bom_ref, weights_commitment}`, `tool_ids[]`. This is the one place human, workload, agent and model are bound to the same event.

### 4.4 `mandate` 1.0 — what was authorised
`scheme` (required: `plain-words-rule`, `ap2-intent`, `ap2-cart`, `mastercard-verifiable-intent`, `visa-tap`, `acp-allowance`, `oidc-consent`, `none`), `within_mandate` (required: `yes`, `no`, `not-assessed`), `scope`, `limits`, `expiry`, `mandate_commitment`, `mandate_ref`, `community_authority_ref`. External signed mandates are referenced or committed to, never copied. `within_mandate: no` is an honest receipt of a breach, not an invalid receipt.

### 4.5 `policy` 1.0 — which gate ran and what it decided
`policy_id`, `version`, `decision` (`allow`, `constrain`, `hold`, `escalate`, `deny`), `enforcement_point` (`pre-action`, `in-flight`, `post-action`, `review`) — all required; `policy_commitment`, `tier`, `controls[]{id, vocabulary, outcome, evidence_ref}`, `human_in_loop`, `risk_class`, `jurisdiction_refs[]`. A control listed with `outcome: pass` is a claim that it executed with that outcome — it says nothing about whether the control is adequate.

### 4.6 `runtime` 1.0 — what was computed, where
`content_included` MUST be `false`. `input_commitment`, `output_commitment` (§5), `counts{input_tokens, output_tokens, tool_calls, latency_ms}`, `environment{attestation, attestation_ref, region}`, `otel{trace_id, span_id}`, `child_receipt_ids[]`. Attestation is environment-level evidence (which binary, which enclave); it never says what was answered.

### 4.7 `provenance-disclosure` 1.0 — what left, how it was marked
`ai_disclosed`, `output_kind` (required), `disclosure_channel`, `manifest{scheme (c2pa | iptc | china-reference-number | none), manifest_commitment, reference_number}`, `accessibility{languages, formats}`. Text, code and voice — most of what generative AI emits — carry no asset manifest; the receipt is their provenance.

### 4.8 `witness` 1.0 — independent registration
Required above OR-2 (§6): `log_operator{id, kind, service_ref}`, `log_checkpoint{tree_size, root_hash, checkpoint_signature}`, `inclusion_proof{leaf_index, hashes, format}`, `consistency_proof`, `witnesses[]{id, observed_at, cosignature}`, `cross_log_anchor`, `observed_at`, `equivocation_status` (required: `not-observed`, `suspected`, `confirmed`).

### 4.9 `contestability` 1.0 — notice, explanation, challenge, review, remedy
Replaces the v0.1 `complaint_ref` pointer with an object a person can act on: `notice{given, channel, languages, accessible_formats}`, `explanation{available, ref, kind, legal_basis}`, `challenge{available, route_ref, deadline, cost, representative_allowed}`, `human_review{available, reviewer_authority (override | recommend | none), reviewer_independent, sla_hours}`, `remedy{types[], collective_redress, escalation_ref}`, `case_id`, `outcome_receipt_ids[]`. Challenge, review and remedy are themselves receipts (`transaction_type` `challenge`, `review`, `remedy`) that name the contested receipt as parent, so the whole life of a dispute is one graph. Human review "available" with `reviewer_authority: none` is reported by verifiers as a warning: a reviewer who cannot change the outcome is not review.

### 4.10 `legal-evidence` 1.0 — travelling as evidence (optional profile)
`jurisdiction_profile` (`EU-eIDAS-QTSA`, `US-FRE-901`, `CN-online-litigation`, `UK-CPR-PD57AD`, `generic`), `collection_method`, `collector_identity`, `timestamp_assurance` — all required when present; `chain_of_custody[]`, `verifier_version`, `evidence_export_manifest`, `retention_until`. The profile says what was done, never what a court will accept. It is not legal advice and a receipt carrying it MUST add that to `limitations`.

### 4.11 `community-authority` 1.0 — collective authority (extension)
`authority_ref`, `consent_basis` (`fpic`, `community-protocol`, `delegated`, `not-applicable`), `use_restrictions[]`, `stewardship_contact_ref`, `review_required_before_disclosure`. Drafted under the CARE principles with — and only with — the Indigenous and community partners named in `governance/COALITION-PLAYBOOK.md`; nothing here ever puts traditional knowledge, sacred material or community governance records in a public log.

## 5. Privacy profile and threat model

Every receipt carries `privacy_profile{profile, commitment_scheme, linkability_scope, metadata_minimization, reidentification_risk_assessment_ref, disclosure_authority[]}`.

Rules:

1. **Content-free by construction.** No predicate carries prompts, outputs, weights, personal data or free text about a person. `runtime.content_included` is a schema constant `false`.
2. **No plain hashes.** Every commitment uses `salted-sha256`, `hmac-sha256` or `pedersen`. The salt or key never enters the receipt or the log; it is delivered out of band to whoever `disclosure_authority` names. A plain hash of a short prompt, an e-mail address or a menu option is guessable and is therefore forbidden; a receipt containing one is invalid.
3. **Public logs hold no stable identifiers.** Nothing registered with a log operator may contain a stable user id, IP address, exact location, device identifier or capability token. `identity.principal_ref` is a per-transaction or per-session pseudonym at most (`linkability_scope`).
4. **Metadata is minimised.** Counts, latencies and regions are rounded or bucketed where the reidentification risk assessment says so; `reidentification_risk_assessment_ref` points to that assessment for OR-3 and above.
5. **Content-free is not anonymous.** Graph shape, timing and counts leak. Operators MUST say so in `limitations` and MUST NOT describe receipts as anonymous.
6. **Disclosure is authorised, not implied.** `disclosure_authority` names roles or authorities, never persons. Opening a commitment for a regulator, a court, a reviewer or the principal is a separate act that SHOULD itself produce a `review` receipt.

The threat model considered: linkage across transactions by a log reader; dictionary attacks on commitments; timing correlation between logs; an operator equivocating between the log shown to users and the log shown to auditors (§6); a delegate widening a mandate; a reviewer without authority laundering a decision as "human-reviewed"; and a registry steward or assessor with a commercial interest in the outcome (§9).

## 6. Witnessing, logs and equivocation

- **OR-2** requires registration in an append-only Merkle log with a checkpoint and an inclusion proof (RFC 6962 style, or an RFC 9942 COSE receipt). The log MAY be operated by the issuer.
- **OR-3** requires a log operator that is **not** the issuer, and at least one independent witness co-signing checkpoints. Verifiers SHOULD fetch a fresh checkpoint and a consistency proof from the witnessed size.
- **Equivocation** — two checkpoints of the same log at the same size with different roots, or an inclusion proof that fails against a witnessed checkpoint — sets `equivocation_status` to `suspected` (one observer) or `confirmed` (two independent observers). A receipt whose log is under suspected or confirmed equivocation is **frozen at OR-2** for every verifier until the log operator publishes an `incident` receipt and the witnesses re-sign. Verifiers MUST NOT report OR-3 or higher on a frozen log.
- **No single route.** At OR-3 and above no one vendor may be the only permitted log, witness, verifier, time service or key-discovery route. Profiles that name a vendor are non-conformant.
- **Backfill.** Receipts registered late (outage) keep `issued_at` as signed and carry the log's `observed_at`; the gap is visible, not hidden.

## 7. Contestability

A receipt that records a consequential decision (`transaction_type` `policy-decision`, `output-delivery` or `human-review` with a `policy.risk_class`) at OR-2 or above MUST carry a `contestability` predicate in which notice was given, an explanation is available, a challenge route exists, and human review — where offered — names a reviewer with `override` or `recommend` authority. Remedies MUST be named from the registered list; `compensation-referral` means a referral exists, not that compensation is owed. `collective_redress: true` means a representative may challenge on behalf of a class of affected people. The Public Interest Council (governance) owns this predicate's evolution; technical bodies may not narrow it.

## 8. Assurance levels

The issuer **claims** a level. The verifier **computes** the level the evidence supports and MUST report both. The reference verifier's rules:

| Level | Name | What must be true | Verifier caps to the level below when… |
|---|---|---|---|
| **OR-0** | Unverified export | Well-formed envelope; signature absent or unverified | — |
| **OR-1** | Issuer signed | Signature verifies against a discoverable key; all four critical predicates present | a critical predicate is omitted (with reason) |
| **OR-2** | Operator logged | OR-1 + `witness` with checkpoint and inclusion proof (issuer-run log allowed) | no inclusion proof |
| **OR-3** | Independently logged | OR-2 + log operator ≠ issuer + ≥ 1 independent witness + no equivocation | operator runs the log; no witness; equivocation suspected or confirmed (frozen at OR-2) |
| **OR-4** | Independently assessed | OR-3 + an assessor (≠ issuer, ≠ log operator) with a current assessment on a public registry | no registry record, or assessor is the issuer |
| **OR-5** | Public-interest accountable | OR-4 + a Public Interest Review Panel record covering this system and profile | no review record |

OR-4 and OR-5 cannot be established from the receipt alone; they require a registry lookup the verifier performs or is handed. A verifier without registry access MUST report OR-3 at most and say why. OR levels describe the **evidence chain**, never the AI system's quality; they are deliberately not OVERT AAL levels and are not borrowed from any certification.

## 9. Roles and separation

| Role | Does | Must not | Must disclose |
|---|---|---|---|
| **Operator** | Emits receipts for systems it runs; keeps salts; answers challenges | Operate the sole log or act as assessor for its own systems above OR-2; describe receipts as certification | Beneficial ownership; commercial ties to log, assessor, insurer |
| **Log operator** | Registers receipts; publishes checkpoints; supports witnesses and consistency proofs | Alter or reorder entries; be the issuer's affiliate at OR-3+; be the only route | Availability and consistency metrics; incidents; ownership |
| **Assessor** | Samples receipts and controls without content access; publishes methodology and negative findings | Assess its own technology, related log, controlled operator or underwriting client; be qualified by a sponsor | Methodology; conflicts; abstentions |
| **Registry steward** | Publishes keys, profiles, assessor and review records | Sell trust status; hold a commercial interest in an issuer it lists; be the sole steward long-term | Funding; governance; change log |
| **Reviewer / remediator** | Issues `review` and `remedy` receipts | Claim authority it lacks (`reviewer_authority`) | Independence from the operator |
| **Verifier** | Anyone | — | — |

The AiGovOps Foundation may act as convener, reference implementer and initial registry steward. It MUST NOT be the sole long-term registry steward, assessor qualifier, notary operator or assurance issuer, and it never grades its own receipts.

## 10. Interface profiles

Same envelope, same predicates; what changes is how the id is carried and how the person sees it.

| Interface | `id_carrier` | The person sees | Boundary |
|---|---|---|---|
| Chat / web | `response-header` + visible affordance | a receipt link under every answer | request-response |
| API | `AI-Receipt` response header; request may carry `AI-Mandate` | the SDK prints it; maps 1:1 to an OTel span | request-response |
| Voice | `spoken` on request; `transcript` | "say 'receipt'" → the aggregate id | streaming-segment + aggregate |
| Agent-to-agent | `message-metadata`; nested receipts per hop | the root receipt for the human principal | agent-action |
| IDE / coding agent | `git-trailer` (`One-Receipt: <id>`) | in the commit | agent-action |
| Browser extension | `message-metadata` | the extension's panel | request-response |
| Embedded / on-device | `device-store`; uploads when online | Settings → receipts | request-response |
| Commerce | `cart-mandate` (AP2 / Verifiable Intent hash in `mandate`) | the merchant receipt cites it | agent-action |
| Batch | `none` (aggregate id in the run record) | the aggregate | batch + aggregate |

## 11. Legal-evidence profile

Optional. Adds `legal-evidence` (§4.10) and requires `clock_source` other than `issuer`, a `chain_of_custody` starting at the operator, and an `evidence_export_manifest` listing every receipt, key, checkpoint and proof in the export with the `verifier_version` used. Jurisdiction profiles are maintained by legal-evidence specialists in the coalition and are descriptive. Nothing in this profile is legal advice; `limitations` MUST say so.

## 12. Canonicalisation, signatures and algorithm agility

- Canonical bytes: JSON with sorted keys, no insignificant whitespace, UTF-8, no floating-point numbers (the v0.2 profile); a full RFC 8785 (JCS) canonicaliser and a CBOR-CDE profile are v0.3 gates and MUST produce byte-identical signatures across implementations before either is normative.
- Algorithms: `Ed25519` (default), `ES256`, `ML-DSA-65`, and hybrid `Ed25519+ML-DSA-65`. Verifiers MUST refuse algorithms not in the registry and MUST NOT downgrade.
- Key discovery: `did-web`, `did-key`, `jwks`, `x509`, `scitt-issuer`, `out-of-band`. Key rotation and revocation records live with the registry steward; a receipt signed after its key's revocation time is invalid.
- Countersignatures append; they never replace the issuer's signature.

## 13. Conformance layers

1. **Syntax** — emits and verifies envelopes that pass the schema, the reference verifier and every vector in `testkit/vectors` with identical verdicts.
2. **Interoperability** — verifies receipts emitted by at least one other independent implementation, and registers with at least one log it does not operate, at a public interoperability event.
3. **Accountability outcomes** — a pilot reports, against pre-registered metrics, whether receipts shortened time-to-answer for audits, incidents, disputes and vendor transitions, whether people could exercise a challenge, and what it cost a small implementer. Layer-3 results, including negative ones, are published.

An implementation may claim "One Receipt v0.2 syntax-conformant" only after layer 1 and never "certified". No conformance layer says anything about the AI system.

## 14. Registries and extensions

Registered here and maintained by the registry steward: predicate types and versions; `transaction_type`; `boundary`; `omission_reason`; signature algorithms; `key_discovery`; `id_carrier`; mandate schemes; control vocabularies; jurisdiction profiles; remedy types. Extensions use `extensions.<namespace>.<name>` with a registered namespace (`aigovops`, `glacis`, `scitt`, …) and never affect validity.

The delta matrix in `spec/delta-matrix.md` records, field by field, what One Receipt takes from and gives to SCITT, OVERT, OpenTelemetry GenAI, C2PA, AP2 / Verifiable Intent, AIUC-1, W3C VC / DID, and the EU AI Act logging standard prEN 18229-1. Mappings remain non-normative until accepted by the relevant body.

## 15. What changed from v0.1

- Scope and bounded-claims section leads; the "nothing exists" framing, insurance-premium claims, "anonymous", AAL borrowing and "explanation-ref as proof" are gone.
- Transaction graph: `event_id`, `root_receipt_id`, `transaction_type`, `sequence`, `boundary`, `started_at`/`ended_at`, `clock_source`; streaming/voice batching profile; delegation rules.
- Ten versioned predicates with a manifest and omission reasons; `witness`, `contestability`, `legal-evidence`, `community-authority` are new; `complaint_ref` is replaced by the contestability object.
- Privacy profile with a threat model; plain hashes and stable identifiers are rejected by the verifier.
- Assurance OR-0…OR-5 with verifier-computed levels and the equivocation freeze.
- Four separated roles with must-nots and disclosures; the Foundation's own limits stated.
- Algorithm agility and countersignatures; conformance in three layers; registries.
