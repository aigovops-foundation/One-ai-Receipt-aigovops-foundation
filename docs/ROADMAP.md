# Roadmap — eighteen months

Gates G0–G7 are defined in `governance/RELEASE-GATES.md`. Dates assume decision 2 (adopt v0.2) is taken in September 2026. Every phase ends with something a stranger can run.

| Phase | Months | Deliverables | Gate |
|---|---|---|---|
| **0 · Seed** (this repository) | Sept–Oct 2026 | v0.2 spec, schemas, reference signer/verifier, twelve corpus vectors, TypeScript contract, governance drafts, delta matrix, adoption plan for the Foundation projects; Beacon emits `one-receipt` behind a flag; Lantern reads it; the café shows a receipt id | **G0** seed complete · **G1** Foundation projects emit + read |
| **1 · Founding cohort** | Nov 2026–Mar 2027 | Listening sessions in the playbook's outreach order; charter, CoI register, funding policy published; Public Interest Council seated and paid; two independent implementations; `one-receipt-log-lab` with witnesses; first public interop event; SCITT Internet-Draft -00 | **G2** governance live · **G3** interop event held |
| **2 · Pilots** | Apr–Sept 2027 | Three pilots (one public sector, one Global South) with pre-registered evaluations; procurement and evidence-rights clauses; regulator-view evidence package; ten-language receipt view; OTel mapping PR; C2PA assertion proposal; AP2 vectors; v0.3 with the RFC 8785 canonicaliser and CBOR-CDE profile | **G4** pilots running · **G5** v0.3 candidate |
| **3 · Assurance** | Oct 2027–Mar 2028 | Assessor eligibility and methodology; first OR-4 records with at least one published negative finding; anti-equivocation drills; legal-evidence profiles reviewed by specialists; registry stewardship transfer plan; v1.0 candidate | **G6** OR-4 operating · **G7** v1.0 ratified by the Incubator with Public Interest Council sign-off |

## The ninety days for the Foundation (Phase 0 detail)

- **Weeks 1–3** — decisions 1–3, 8, 10 taken; this repository public; Beacon branch `one-receipt` emits v0.2 envelopes from its existing Ed25519/JCS signer; the ten chosen corpus cases become the canonical vectors.
- **Weeks 4–6** — Lantern's verify page runs the reference verifier in the browser and shows claimed vs verified level; the café's Wren Card carries a receipt id; the 200 worksheet emits a receipt from CI; the 400 worksheet verifies a stranger's receipt offline.
- **Weeks 7–9** — the Glacis note goes with the delta matrix; SCITT editors approached with the -00 outline; the NIST use case submitted; a Thursday devoted to a stranger verifying a receipt.
- **Weeks 10–13** — first external verification by a 400; the joint story; v0.2.1 with what broke; the playbook's first listening invitations out in the prescribed order.

## What is deliberately not on the roadmap

A certification mark; an insurance product; a hosted "One Receipt Cloud"; a Foundation-run sole registry; zkML proof-of-inference per request (not viable at frontier scale in 2026); any claim about model truthfulness.
