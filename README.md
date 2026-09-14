# One Receipt — AiGovOps Foundation

**One signed, content-free receipt per AI transaction that a stranger can verify offline, a person can challenge, and a regulator can inspect without trade secrets.** Spec v0.2-draft · incubation, not a standard · Apache-2.0 code, CC BY 4.0 text.

A verified receipt proves that an identified issuer signed the declared claims, bound them to identifiers and time, and supplied the evidence the claimed assurance level requires. It does **not** prove that an AI output was true, fair, safe, lawful, accurate or harmless, that a system is certified, or that any evidence is admissible. Every receipt says so; so does every verifier result.

## Try it in two minutes

```bash
pip install -e '.[dev]'
one-receipt emit examples/minimal-payload.json examples/private-key.pem > receipt.json
one-receipt verify receipt.json --public examples/public-key.pem     # claimed OR-1, verified OR-1
one-receipt verify receipt.json                                       # no key → verified OR-0, and it tells you why
one-receipt vectors                                                   # twelve corpus cases, twelve verdicts
pytest
```

The demonstration keys in `examples/` are for the vectors only. Production deployments need real key discovery, rotation and revocation, an independent log and witnesses above OR-2, salts kept out of band, and a privacy risk assessment — the spec says where.

## What is here

| Path | What |
|---|---|
| `spec/ONE-RECEIPT-SPEC.md` | The core specification: bounded claims, envelope, transaction graph, ten predicates, privacy threat model, witnessing and equivocation, contestability, OR-0…OR-5 computed by the verifier, four separated roles, interface profiles, legal-evidence profile, conformance layers |
| `spec/schema/` | JSON Schema 2020-12 for the envelope and every predicate |
| `spec/delta-matrix.md` | What One Receipt takes from, adds to, and leaves alone in SCITT, OVERT, OpenTelemetry, C2PA, AP2, AIUC-1, VC/DID, the EU AI Act and the Foundation's own projects |
| `src/one_receipt/` | Reference signer, verifier (single receipt and graph), commitments, CLI, vector runner |
| `packages/typescript/` | The TypeScript contract (types); an SDK follows once it passes the vectors |
| `testkit/vectors/` | Twelve test vectors from the Foundation's corpus cases (Air Canada, Knight Capital, Robodebt, Cigna, Horizon, Arup, the $1 Tahoe) with the verdict a conformant verifier must reach |
| `docs/WHITEPAPER.md` | The whitepaper review draft, v0.2 |
| `docs/MASTER-PLAN.md` | Product, standards, open-source and coalition plan, with the twelve decisions |
| `docs/FRAMEWORK.md` · `docs/ARCHITECTURE.md` · `docs/ROADMAP.md` · `docs/PRACTITIONER-PROGRAM.md` | The framework (principles, personas, lifecycle, maturity), the twelve components, eighteen months and gates, OR-100…OR-600 |
| `docs/ADOPTION.md` + `adapters/` | How Beacon, Lantern, Umbrella, aigovops (Jeeves), Replay, prompt-studio, practice, Omni/Library and the vendor RFI adopt it, field by field |
| `governance/` | Charter, conflict-of-interest, funding and independence, release gates G0–G7, the coalition invitation and funding playbook, the LOI template, contributing, code of conduct, IP, security |
| `requirements/requirements.csv` | 360 traceable requirements, 18 domains × 20 |

## Who this is for

Operators who must prove controls ran without exposing prompts or weights; buyers who want evidence that follows the vendor relationship; people who want to know whether it was AI, what they authorised, and how to challenge; regulators who want to inspect without trade secrets; civil society that wants an independent party to verify a sample; auditors, insurers and researchers who need an evidence format that says exactly what it proves.

## Governance in one line

The AiGovOps Foundation convenes, implements first and teaches. It issues no standard, grades no receipts, and is not the long-term sole registry steward, assessor qualifier, notary operator or assurance issuer. Public-interest participants are paid and can bind. No contributor above 15% of funding. Details in `governance/`.

## Proposed inaugural contributors

Glacis and the OVERT community are proposed inaugural technical contributors, subject to written acceptance, contribution and IP terms, conflict disclosure and independent governance. Participation confers no unilateral control, certification authority, exclusive service rights or the ability to assess one's own systems.

## Status

Seed release (gate G0). CI runs lint, tests, the vectors, schema meta-validation, TypeScript, the 360-requirement check and links. Contributions: `governance/CONTRIBUTING.md`. Security: `governance/SECURITY.md`. Owners: Bob Rapp and Ken Johnston.
