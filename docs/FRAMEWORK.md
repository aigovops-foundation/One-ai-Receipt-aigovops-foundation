# The One Receipt Framework

A shared operating framework for making bounded AI transactions independently verifiable, in the shape practitioners already know from the FinOps Foundation: principles, personas, a lifecycle, domains, capabilities and a maturity model. The difference is where power sits — public-interest participants are paid and can bind, and no vendor, log operator, assessor or insurer grades its own commercial interest.

## Principles

1. **Bounded claims.** A receipt proves signing, binding and evidence — never truth, fairness, safety or legality. Say what it proves; say what it does not.
2. **Content-free by construction.** Prompts, outputs, weights and personal data never enter a receipt or a log. Commitments are salted or keyed; plain hashes are forbidden.
3. **Verifiable by a stranger.** A public key and a receipt are enough at OR-1; a log and a witness are enough above it. No account, no vendor dashboard.
4. **One transaction, one graph.** Chat turn, tool call, delegation, review, remedy — every event is a receipt in the same graph; the transaction is as strong as its weakest link.
5. **Separation of roles.** Operator, log operator, assessor and registry steward are distinct parties above OR-2, with published must-nots and disclosures.
6. **Contestability is a predicate, not a footnote.** Notice, explanation, challenge, human review with real authority, and named remedies travel with the decision.
7. **Privacy has a threat model.** Linkability, dictionary attacks, timing and equivocation are designed against, measured, and disclosed. Content-free is not anonymous.
8. **Narrow core, broad adapters.** The envelope and ten predicates are small; everything vendor-, jurisdiction- or interface-specific is an adapter or profile.
9. **Running code and evidence first.** Claims advance only with test vectors, independent implementations, pilot results and published limitations — including negative ones.
10. **Reconcile, do not replace.** Profile SCITT, OVERT, OpenTelemetry, C2PA, AP2 and the control vocabularies; contribute mappings upstream; claim no standards status without a written decision from the body.
11. **Paid public-interest power.** Civil society, affected communities, accessibility, Global South and Indigenous partners hold voting and appeal seats, funded from a protected budget line.
12. **Deployable by the small.** If a two-person shop cannot emit and verify an OR-1 receipt in an afternoon without a compliance department, the core is too big.

## Personas

| Persona | What they need from a receipt | Where they meet the framework |
|---|---|---|
| **Operator / seller** | Prove controls ran without exposing prompts or weights; separate the human's mandate from the agent's identity | Emit at OR-1 → OR-3; adapters; conformance layer 1–2 |
| **Buyer / deployer / procurer** | Which model and policy served this call; six months of evidence without content; evidence that follows the vendor relationship | Procurement profile; evidence-rights clauses; pilot network |
| **End user / affected person** | Was it AI; what did I authorise; how do I challenge; who reviews with authority; what remedy | Contestability predicate; interface profiles; plain-language receipt view |
| **Regulator / supervisory authority** | Is the claim traceable to production; was the log altered; can I inspect without trade secrets | Regulator-view evidence package; incident receipts; observer seat |
| **Civil society / researcher** | Is the system in a register; can an independent party verify a sample; can harms invisible in logs be raised | Public Interest Council; assessor pool; research access |
| **Auditor / assessor / forensic** | Sufficiency, sampling, chain of custody, limitations | Assessor role; legal-evidence profile; methodology registry |
| **Insurer / risk partner** | Incident chronology; control verification at a time | Risk-evidence questions (never premium claims) |
| **Log operator / infrastructure** | A vendor-neutral integration profile; competition on service, not lock-in | Witness predicate; SCITT profile; anti-equivocation drills |
| **Practitioner (100–400)** | One thing to do this week that returns them to the community | The practitioner program (`docs/PRACTITIONER-PROGRAM.md`) |

## Lifecycle — Declare · Gate · Prove · Verify · Contest · Improve

| Stage | Question | Output | Owner persona |
|---|---|---|---|
| **Declare** | Who is the principal, what is the mandate, which system, which policy, what risk, which jurisdiction, what evidence is owed? | `identity`, `mandate`, `policy.policy_id/version`, `privacy_profile` | Operator, buyer |
| **Gate** | Before the consequential action: allow, constrain, hold, escalate or deny? | `policy` predicate; a `policy-decision` receipt | Operator |
| **Prove** | Emit versioned predicates, sign, register, keep the salts | `runtime`, `provenance-disclosure`, `witness`; the signed envelope | Operator, log operator |
| **Verify** | Schema, signature, key status, graph, manifest, privacy, log proofs, witnesses, equivocation, limitations | the verifier result: claimed vs verified level | Anyone |
| **Contest** | Notice, explanation, challenge, review with authority, remedy | `contestability`; `challenge`/`review`/`remedy` receipts | Affected person, reviewer, remediator |
| **Improve** | Incidents, assessments and outcome metrics feed policy, implementation and the spec | `incident` receipts; layer-3 pilot reports; spec issues | Everyone; the councils |

## Domains

Eighteen domains, matching the 360-requirement catalogue (`requirements/requirements.csv`, twenty per domain): Strategy (STR), Governance (GOV), Product (PRD), Architecture (ARC), Identity & mandate (IDM), Policy (POL), Runtime (RUN), Logging & witness (LOG), Privacy (PRI), Security (SEC), Contestability (CON), SDKs (SDK), Testing & conformance (TST), Development (DEV), Program management (PMO), Partners & coalition (PAR), Procurement (PRO), Marketing & education (MKT).

## Capabilities

Each domain breaks into capabilities a team can own, measure and mature. The first-release capabilities are: envelope emission; graph construction; canonicalisation and signing; key discovery and rotation; policy gating; commitment management (salts out of band); log registration; witnessing and consistency checks; equivocation response; contestability routing; challenge/review/remedy receipts; privacy risk assessment; evidence export; conformance testing; procurement profiling; practitioner enablement.

## Maturity model

| Level | Name | You can say | Evidence |
|---|---|---|---|
| **1** | Observe | "We emit OR-1 receipts for one workflow and can verify them offline." | Vectors pass; one interface profile |
| **2** | Implement | "Every consequential decision in scope has a receipt with contestability, and we register them." | OR-2; contestability predicate on every `policy-decision` |
| **3** | Interoperate | "A stranger's verifier and a log we do not run agree with ours." | Conformance layer 2 at a public event |
| **4** | Independently assure | "An assessor we do not control samples our receipts and publishes findings, negative ones included." | OR-4 registry record; methodology public |
| **5** | Public-interest accountable | "Affected people can challenge, get review with authority, and obtain named remedies — and the Public Interest Review Panel says so." | OR-5 record; layer-3 outcomes published |

Maturity describes an organisation's evidence practice; it is never a claim about the AI system's behaviour and never a certification.
