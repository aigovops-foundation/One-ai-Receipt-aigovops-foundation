# Adoption plan — every Foundation open-source project

One envelope, adopted where each project already touches evidence. The rule from the practice repo stands: **Beacon signs. Lantern reads. Umbrella declares.** One Receipt changes the shape of what is signed, read and declared — not who does it. Per-project deltas are in `adapters/`.

| Project | Today | Delta to One Receipt v0.2 | Version it lands in | Adapter |
|---|---|---|---|---|
| **aigovops-beacon** | Emits an OVERT-envelope "Replay-style receipt" per observed interaction: ULID, `user{sub,email,oidc_issuer}`, vendor/model/version, `prompt`/`prompt_hash`, `result`/`result_hash`, `event_type`, Ed25519, append-only NDJSON, hourly Merkle root | Emit the v0.2 envelope behind `--one-receipt`; map `event_type` → `transaction_type`; replace the OIDC subject and e-mail with a per-session pseudonym; replace plain `prompt_hash`/`result_hash` with salted commitments (salts stay in Beacon's evidence store); the hourly Merkle root becomes the `witness.log_checkpoint`; keep the OVERT envelope as `extensions.glacis.overt` | 0.3.0 (Fall release) | `adapters/beacon.md` |
| **umbrella-govops** | Compiles NIST AI RMF / EU AI Act to YAML policy and CI/CD checks with UCIDs and signed evidence bundles | Emit a `policy-decision` receipt per gate evaluation with `controls[].vocabulary: ucid`; the bundle's signature becomes a countersignature; UCID is registered as a control vocabulary | 0.1.0 (first PyPI) | `adapters/umbrella.md` |
| **aigovops-lantern** | Human-carried reader: verifies Beacon receipts and the log offline | Run the reference verifier; show **claimed vs verified level**, limitations, the graph, and the contestability routes as buttons a person can press; become the Foundation's reference verifier UI | 0.2.0 | `adapters/lantern.md` |
| **aigovops** (Jeeves) | Orchestrates Beacon, Lantern and Umbrella | Owns the transaction graph: assigns `transaction_id`/`root_receipt_id`, emits `agent-delegation` receipts per hand-off, closes streams with `aggregate` | 4.1 | `adapters/aigovops.md` |
| **aigovops-Replay** | Cryptographically signed receipt system; Beacon is wire-compatible with it | Replay's verifier accepts v0.2 envelopes and runs `testkit/vectors`; Replay's schema is frozen as the v0.1-era legacy profile and documented in the delta matrix | next tag | `adapters/replay.md` |
| **aigovops-prompt-studio** | Prompt-level audit with immutable logging, version control, 2FA | Every prompt version, run and approval emits a receipt (`inference`, `human-review`) with `identity.model` and a `policy_commitment`; the audit log registers with a log; the 2FA approval becomes `human_in_loop: approved` on the receipt | next tag | `adapters/prompt-studio.md` |
| **practice** (the café) | Levels 100–400 on corpus cases; Wren Card; Thursday marks | OR-100…OR-400 steps added to the existing worksheets; the Wren Card carries a receipt id; the ten chosen corpus cases are the canonical vectors; the Thursday mark line gains the receipt id | 1.0.0 → 1.1.0 | `adapters/practice.md` |
| **aigovops-library** / Omni | Governed multi-agent core; Gate Check; `decide.html` decision receipts (SHA-256) | `decide.html` emits a v0.2 `policy-decision` receipt at OR-0 (unsigned export) in the browser and OR-1 when the practitioner holds a key; the Library's T10 JCS canonicaliser ticket becomes the v0.3 canonicaliser shared with this repo | 4.1 | `adapters/omni-library.md` |
| **aigovops-vendor-rfi** | Vendor RFI + audit-training (Beacon × Umbrella) | RFI questions ask for the OR level and the interface profile; answers are receipts, not prose | alpha | `adapters/vendor-rfi.md` |

## Order of work

1. This repository public; decision 8 picks the ten vectors.
2. Beacon `--one-receipt` flag (the only new signer); Lantern reads it. Everything else consumes what Beacon emits.
3. Umbrella's gate receipts; Jeeves's graph.
4. practice worksheets; the café shows a receipt.
5. Replay and prompt-studio verifiers pass the vectors.
6. Omni `decide.html` and the RFI.

## What no project does

No project certifies, grades its own receipts, or claims an OR level above what an independent verifier reports. No project describes receipts as anonymous. The Foundation's projects are the first implementers; they are not the standard.
