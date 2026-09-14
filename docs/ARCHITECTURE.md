# Architecture

## Components

| # | Component | Responsibility | In this repo |
|---|---|---|---|
| 1 | Schemas | Envelope and ten predicate schemas; registries | `spec/schema/` |
| 2 | Canonicaliser + signer | Deterministic bytes; Ed25519 now, ES256 / ML-DSA-65 / hybrid via the algorithm registry | `src/one_receipt/core.py` (`canonical_bytes`, `sign`) |
| 3 | Key discovery + rotation | `issuer.key_discovery`; revocation records with the registry steward | reference: PEM files; production: did-web / jwks |
| 4 | Policy gate adapter | Turns a gate decision into the `policy` predicate; control ids from UCID / OVERT / AIUC-1 / AICM | `adapters/umbrella.md`, `adapters/beacon.md` |
| 5 | Commitment service | Salted / keyed commitments; salts held by the operator; authorised opening produces a `review` receipt | `commit`, `open_commitment` |
| 6 | Log client | Register the envelope; fetch checkpoint, inclusion and consistency proofs (SCITT / Rekor / Merkle) | `witness` predicate; `one-receipt-log-lab` (planned) |
| 7 | Witness client + equivocation monitor | Compare checkpoints across witnesses; set `equivocation_status`; emit `incident` receipts | planned; freeze rule implemented in the verifier |
| 8 | Verifier | Single receipt and graph; computes the verified level; always returns limitations | `verify_receipt`, `verify_graph`, CLI |
| 9 | Contestability router | Notice, explanation, challenge, review, remedy as receipts in the same graph | `contestability` predicate; `challenge` / `review` / `remedy` types |
| 10 | Evidence exporter | Legal-evidence profile; export manifest; chain of custody | `legal-evidence` predicate; exporter planned |
| 11 | Registry client | Assessor, public-interest review and key records for OR-4 / OR-5 | `registry` argument to the verifier; JSON stub |
| 12 | Conformance test-kit | Vectors and the runner; interop harness | `testkit/` |

## Trust boundaries

```
 principal ──mandate──▶ operator ──receipt──▶ log operator ◀──co-sign── witnesses
                          │  keeps salts            │ checkpoints
                          │                         ▼
                          └──authorised opening──▶ reviewer / assessor ──record──▶ registry steward
                                                                                     ▲
                                                                     verifier (anyone) ┘ reads keys, assessor + review records
```

- Content and salts stay inside the operator boundary; only commitments cross it.
- Above OR-2 the log operator is outside the operator's trust boundary; above OR-3 so are the witnesses; at OR-4 the assessor; at OR-5 the review panel.
- The verifier trusts nothing it cannot check: the signature, the proofs, the witnessed checkpoint, and the registry record it fetched itself.

## Data flow for one chat turn (OR-2)

1. **Declare** — the gate loads policy `cafe-100` v3, the principal's pseudonym for this session, the plain-words mandate.
2. **Gate** — pre-action decision `allow`; controls `UCID-12` pass. A `policy-decision` receipt is emitted as the root.
3. **Prove** — inference runs; the operator commits to input and output with fresh salts; an `inference` receipt names the root as parent and carries `runtime`, `provenance-disclosure`, `contestability`.
4. **Register** — both receipts go to the log; the `witness` predicate is filled from the inclusion proof; the receipt id is returned in the `AI-Receipt` header and shown under the answer.
5. **Verify** — a stranger with the public key verifies both, checks the graph (one root, parents present), fetches a checkpoint, and reports "verified OR-2; claimed OR-2; limitations: …".
6. **Contest** — the person challenges; a `challenge` receipt names the inference receipt; a reviewer with `override` authority issues a `review` receipt; a `remedy` receipt records the correction. Same graph.

## Security design

Threats and controls: key compromise (rotation records, short key lifetimes, countersignatures by the log); replay (unique `receipt_id`, `event_id`, sequence checks); tampering (signature over canonical bytes; inclusion proofs); equivocation (witnesses; freeze); downgrade (algorithm registry; verifier refuses unknowns); confused deputy across delegation (mandate inheritance by reference; scope never widens); metadata leakage (privacy profile; bucketing; risk assessment); social engineering of "human review" (reviewer authority and independence are fields verifiers read).

## Performance envelope

OR-1 emission is one canonicalisation and one Ed25519 signature — sub-millisecond in the reference implementation; no network. OR-2 adds one log write, done asynchronously with backfill semantics. Receipts are typically 2–8 KB. Streams batch by profile; they never receipt per token.
