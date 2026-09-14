# Changelog

## 0.2.0 — 2026-09-14 (seed, gate G0)

Built from the v0.1 starter, the v0.2 recommended amendments, the coalition invitation and funding playbook, and the complete product plan.

- **Spec v0.2-draft** (`spec/ONE-RECEIPT-SPEC.md`): bounded-claims section; transaction graph (`event_id`, `root_receipt_id`, `transaction_type`, `sequence`, `boundary`, `started_at`/`ended_at`, `clock_source`); streaming/voice batching profile; delegation rules; ten versioned predicates with manifest and omission reasons; privacy profile and threat model (no plain hashes, no stable identifiers in logs, content-free ≠ anonymous); witness predicate with equivocation freeze; contestability object replacing `complaint_ref`; legal-evidence profile; community-authority extension; OR-0…OR-5 computed by the verifier; four roles with must-nots; interface profiles; algorithm agility and countersignatures; three conformance layers; registries; delta matrix.
- **Schemas**: envelope `0.2-draft` plus ten predicate schemas.
- **Reference implementation**: `emit_receipt` with graph fields; `verify_receipt` reports claimed vs verified level, manifest, graph, time, privacy and ladder checks; `verify_graph`; salted/HMAC commitments; CLI `keygen · emit · verify · graph · commit · vectors`.
- **Test kit**: twelve vectors from corpus cases with required verdicts; `testkit/make_vectors.py` regenerates them; 17 tests.
- **TypeScript**: v0.2 contract.
- **Docs**: whitepaper v0.2; master plan with twelve decisions; framework; architecture; roadmap and gates; practitioner program OR-100…OR-600; adoption plan and nine adapters.
- **Governance**: charter with seven bodies; conflict-of-interest; funding and independence (caps, protected lines, transparency report); release gates G0–G7; the coalition playbook (eleven partner groups, funding asks/offers, cohort, outreach order, templates, launch criteria); LOI template.
- **Removed or softened** (per the amendments): "nothing exists" claims; insurance-premium claims; "anonymous"; AAL borrowing; explanation-ref as proof; the Foundation as sole editor, registry or trust root.

## 0.1.0 — starter

Incubation starter: envelope `0.1-draft`, Python signer/verifier, TypeScript types, four tests, 360 requirements, governance stubs.
