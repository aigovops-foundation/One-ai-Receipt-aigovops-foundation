# One Receipt — Master Plan

Complete product, standards, open-source and global-coalition plan. Version 0.2, 14 September 2026. Owners: Bob Rapp and Ken Johnston, AiGovOps Foundation. Status: **for decision** (the twelve decisions at the end).

This plan folds three inputs into one place: the v0.1 whitepaper review (`docs/WHITEPAPER.md`), the v0.2 recommended amendments (now the spec, `spec/ONE-RECEIPT-SPEC.md`), and the coalition invitation and funding playbook (`governance/COALITION-PLAYBOOK.md`).

## 1. Executive summary

Every AI standard in the field holds one piece of the evidence problem — the organisation, the quarterly certificate, the per-decision control, the file's provenance, the shopping mandate, the log, the legal duty — and none joins them into one verifiable record of one transaction that a stranger can check, a person can challenge, and a regulator can inspect without trade secrets. One Receipt is that record: a content-free, signed, chained envelope with ten versioned predicates, six assurance levels the verifier computes rather than trusts, four separated roles, and a governance model in which public-interest participants are paid and can bind.

The program is built to avoid two predictable failures: **vendor capture** (no operator, log provider, assessor or insurer buys control of the protocol, the assurance ladder, the registry or the conflict process) and **unfunded participation** (civil society, affected communities, accessibility specialists, Global South and Indigenous partners are compensated, not invited to donate the labour that gives the coalition legitimacy).

The Foundation's role is convener, first implementer and teacher. It issues no standard, grades no receipts, and is not the long-term sole registry steward, assessor qualifier, notary operator or assurance issuer.

## 2. Strategic thesis

1. **Procurement, not goodwill, drives adoption.** Buyers who can specify "portable evidence at OR-2 with contestability" in a contract turn a protocol into a market requirement. The plan leads with three buyers in the founding cohort.
2. **Insurance and certification need per-call evidence they cannot produce themselves.** AIUC-1 says an agent passed last quarter; a receipt says control A006 ran on this call. The program offers that link and makes no premium claims.
3. **The standards bodies want mappings and running code, not a rival stack.** The SCITT statement profile, the OTel mapping table, the C2PA assertion and the AP2 test vectors are the contributions; the delta matrix is the first thing liaisons see.
4. **Legitimacy precedes vendors.** Public-interest, regional and Indigenous partners are seated and paid before the first commercial sponsor is announced.
5. **The small implementer is the test.** If OR-1 takes more than an afternoon for a two-person team, the core is too big.

## 3. The framework

Principles, personas, lifecycle (Declare · Gate · Prove · Verify · Contest · Improve), eighteen domains, capabilities and the five-level maturity model are in `docs/FRAMEWORK.md`.

## 4. Business plan and funding safeguards

**Eighteen-month budget target:** $3.0M–$5.0M, deliberately diversified. Allocation: open technical core and security 25%; public-interest participation 20% minimum (protected line); independent research and evaluation 20%; pilots and adoption 15%; governance, legal and registry operations 10%; reserves and incident response 10%.

**Revenue guardrails (binding):** no single contributor above 15% of annual unrestricted revenue; no commercial sector above 35%; at least 20% ring-fenced for compensated public-interest participation; at least 20% for independent evaluation and security/privacy research; every contribution above $10,000 publicly disclosed with range, restrictions and conflicts; restricted funding never determines a technical conclusion, assessor qualification, conformance outcome, public-interest decision or publication; an annual transparency report with revenues, expenses, in-kind, participation, conflicts, outcomes and unresolved dissent.

**Funding requests by partner group** (cash asks for commercial parties, funding *offers* for public-interest parties) are in the playbook: large AI providers $250k–$750k; cloud/security platforms $250k–$500k; buyers $100k–$300k; assurance firms $75k–$250k; insurers $100k–$300k; standards bodies no cash ask; civil-society council members $25k–$75k grants; Indigenous governance bodies $50k–$150k partnership grants; universities $50k–$250k project grants; Global South research leads $75k–$300k; small implementers no fee plus $5k–$25k microgrants.

## 5. Three-year outcomes

| Horizon | Outcome |
|---|---|
| **Year 1** | v1.0 core spec ratified by the Technical Incubator with Public Interest Council sign-off; Python and TypeScript SDKs; offline verifier; two independent implementations and two independent log/witness paths at a public interop event; three pilots (one public sector) with pre-registered evaluations; the SCITT Internet-Draft adopted for discussion; the Foundation's own projects emitting and reading receipts |
| **Year 2** | OR-4 assessor pool with public methodology and at least one negative finding published; procurement clauses used in one real contract; regional chapters in three regions with ten languages; the OTel mapping and C2PA assertion accepted or formally declined with reasons |
| **Year 3** | Registry stewardship transferred out of the Foundation to a multi-party steward; OR-5 public-interest review operating; layer-3 outcome evidence published for every pilot; the coalition's annual transparency report in its third edition |

## 6. Governance

Bodies, decision rules and founding roles are in `governance/CHARTER.md`: a Governing Board (mission, fiduciary, host relationship; cannot approve a member's conformance claim), a Technical Steering Committee / Technical Incubator (rough consensus, no member veto), a Public Interest Council (binding review over privacy, accessibility, contestability, affected-community rights, data sovereignty, conflicts), an Adoption Council / Adoption and Pilot Network (recommends, never certifies its own pilots), an Independent Appeals Panel, and a Standards Liaison Forum. Conflict rules are in `governance/CONFLICT-OF-INTEREST.md`; funding rules in `governance/FUNDING-AND-INDEPENDENCE.md`.

## 7. Product requirements (PRD)

**Functional.** Emit, sign, chain, register, verify, export; verify a graph; compute the verified level; produce the plain-language receipt view in ten languages; route challenge, review and remedy as receipts; run the conformance vectors; adapters for SCITT, OVERT, OTel, C2PA, AP2 and the Foundation projects.

**Non-functional.** OR-1 emission adds < 5 ms p50 and no network call; verifier runs offline; receipts ≤ 8 KB typical; no content, no stable identifiers; every result carries limitations; algorithm agility; twelve-month deprecation for any breaking change; accessibility (WCAG 2.2 AA) for every user-facing view.

**Success metrics.** Time-to-answer for audit, incident, dispute and vendor-transition questions in pilots (pre-registered baseline vs. with receipts); share of consequential decisions with a contestability predicate; challenge completion rate and time to human review; small-implementer cost to OR-1 in person-hours; number of independent implementations passing the vectors; number of independent log/witness paths; published negative findings.

**FAQ (the honest answers).** *Does a receipt prove the AI was right?* No. *Is it anonymous?* No — content-free, with a threat model. *Is it a certification?* No. *Does it lower my premium?* Nobody may say so without independent evidence. *Is it admissible?* The legal-evidence profile says what was done; a court decides. *Who grades the Foundation's receipts?* Not the Foundation.

## 8. Technical architecture

Twelve components: (1) envelope and predicate schemas; (2) canonicaliser and signer; (3) key discovery and rotation; (4) policy gate adapter; (5) commitment service (salts out of band); (6) log client (SCITT / Rekor / Merkle); (7) witness client and equivocation monitor; (8) verifier (single and graph); (9) contestability router; (10) evidence exporter (legal-evidence profile); (11) registry client (assessor, review, key records); (12) conformance test-kit. Trust boundaries: operator ↔ log operator ↔ witness ↔ assessor ↔ registry steward; salts never cross the operator boundary except by authorised disclosure. Detail in `docs/ARCHITECTURE.md` and the spec.

## 9. Open-source design

**Repository portfolio** (this repository seeds them; split when a second maintainer exists): `one-receipt-spec` (this spec, schemas, registries, delta matrix), `one-receipt-sdk-python`, `one-receipt-sdk-ts`, `one-receipt-verifier` (offline CLI and web verifier), `one-receipt-testkit` (vectors, interop harness), `one-receipt-log-lab` (a small SCITT-style log with witnesses for pilots and anti-equivocation drills), `one-receipt-adapters` (SCITT, OVERT, OTel, C2PA, AP2, Foundation projects), `one-receipt-governance`, `one-receipt-learning`, `one-receipt-pilots`.

**Licensing.** Apache-2.0 code; CC BY 4.0 specifications and documents; DCO sign-off; royalty-free patent commitments from contributing organisations for normative text; trademarks separately governed (`governance/IP-POLICY.md`).

**Engineering standards.** Public issues and PRs; two non-author approvals for normative changes; security review for cryptographic changes; Public Interest Council review for privacy and contestability changes; 30-day RFC for breaking changes; CI runs lint, tests, vectors, schema meta-validation, TypeScript, the 360-requirement check and links.

## 10. Development plan, test plan and PMO

Phases are in `docs/ROADMAP.md` with gates G0–G7 in `governance/RELEASE-GATES.md`. The test plan has three layers matching conformance: syntax (schema + vectors), interoperability (cross-implementation, cross-log), and accountability outcomes (pre-registered pilot metrics). The PMO runs a fortnightly public status, a public risk register, and the annual transparency report.

## 11. Global rollout

Phase 0 (now): the Foundation's own projects emit and read receipts; the café teaches it. Phase 1 (months 1–6): founding cohort of 18–24 balanced parties; two independent implementations; the first interop event. Phase 2 (months 7–12): three pilots across sectors and regions; procurement language in use; regional co-chairs; ten languages. Phase 3 (months 13–18): assessor pool; registry stewardship transfer plan; OR-5 review operating. At least half of non-vendor seats outside North America and the EU.

## 12. Standards strategy

Order of outreach: existing adjacent standards and open-source communities first (reconcile, do not duplicate), then public-interest and regional partners, then implementers and log witnesses, then buyers, then researchers, then auditors/insurers/regulators, then additional sponsors. Contributions: the SCITT statement profile draft; the OVERT profile; the OTel mapping table; the C2PA assertion; AP2 test vectors; the NIST AI Agent Standards Initiative and ITU FG-TIDA use cases; comments on prEN 18229-1. No claim of endorsement, adoption or standards status without a written decision.

## 13. Marketing and education

The story is told from the café: a person asks for a receipt and gets one. Never a logo wall; never "certified"; never "anonymous"; never a premium claim. The practitioner program (`docs/PRACTITIONER-PROGRAM.md`) is the education plan — OR-100 to OR-600, each level one hour of practice that returns the practitioner to the community.

## 14. Risks

Vendor capture (mitigated by caps, seats and conflict rules); audit-washing (bounded claims in every artefact; negative findings published); privacy leakage through metadata (threat model, risk assessment above OR-2); equivocation and log outages (witnesses, freeze, backfill rules); complexity creep (the small-implementer test at every gate); standards rejection (mappings are non-normative, contributions are narrow); legal-evidence over-claiming (profile is descriptive; limitations mandatory); Foundation over-reach (its must-nots are in the spec).

## 15. Launch blockers

The coalition launches only when: a published charter, contribution policy, IP policy, conflict register, code of conduct and decision process exist; paid public-interest and regional participants are in the first cohort before the announcement; no commercial contributor above 15%; two independent implementations and two independent log/witness paths committed to the first interop event; one buyer with a real procurement or audit-evidence use case; one research partner with a pre-registered evaluation; the public delta matrix published; and launch language with no unsupported claim about compliance, safety, fairness, admissibility, premium reduction or certification.

## 16. Twelve immediate executive decisions

1. Name: **One Receipt** (working); repository `One-ai-Receipt-aigovops-foundation` — confirm or rename.
2. Adopt the v0.2 spec as the incubation baseline and freeze v0.1.
3. The Foundation as neutral convener and initial registry steward with a written transfer intent — yes/no.
4. Invite Glacis and the OVERT community as proposed inaugural technical contributors under the conflict rules — send now with the delta matrix, or after the SCITT draft exists.
5. Host the working group at the Foundation, or ask the Agentic AI Foundation (Linux Foundation) to host.
6. Fund the Public Interest Council first: approve the protected 20% line and the first four to six paid seats.
7. Choose the three founding buyers and the one public-sector pilot to approach.
8. Which ten corpus cases become the first test vectors (twelve are seeded in `testkit/vectors`).
9. Approve the SCITT Internet-Draft as the first standards contribution and name co-authors to approach.
10. Adopt OR-0…OR-5 as the assurance ladder and decline to borrow AAL levels — confirm.
11. Approve the Foundation-project adoption plan (`docs/ADOPTION.md`) and the Fall release versions it implies.
12. Approve the 18-month budget target and the funding guardrails as binding.

## 17. Final direction

Build the smallest receipt a stranger can verify; make it a graph; put contestability inside it; pay the people who make it legitimate; contribute every mapping upstream; publish what breaks. Then let procurement do the rest.
