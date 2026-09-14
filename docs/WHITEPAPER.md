# One Receipt

**A proposal for an end-to-end protocol that lets anyone verify one generative-AI transaction — across every interface, for every party.**

Whitepaper review draft **v0.2** · AiGovOps Foundation · 14 September 2026 · Authors: Bob Rapp, Ken Johnston, with Claude · Status: **for review** (Ken and Bob; then the Review Circle; then the coalition's standards liaisons) · Supersedes v0.1 (13 September 2026), which stays in the `practice` repo as history.

*What changed since v0.1, in one line: the paper now makes only bounded claims, describes the v0.2 specification in this repository rather than a sketch, uses its own OR-0…OR-5 evidence ladder instead of borrowing OVERT's AAL levels, replaces the complaint pointer with a contestability object, adds a privacy threat model and witnessing, separates four roles, and carries the coalition and funding plan alongside it.*

*Assumption stated up front: "UP Path" in the original brief is read as UiPath — founding contributor to, and first platform certified under, AIUC-1. Every claim below carries a source; items that could not be confirmed on 13 September 2026 are marked "unverified" and must not be printed publicly.*

---

## 0. In one paragraph

Today a person can talk to an AI in a chat window, through an API, by voice, inside an IDE, through a browser extension, on a phone, or through another agent — and no party can later prove, without trusting the operator, what model answered, under which policy, on whose authority, with what checks, and whether the record was altered afterwards. Many bodies each hold one piece: ISO 42001 certifies the organisation, AIUC-1 certifies the agent quarterly, OVERT signs the decision, C2PA signs the file, SCITT gives the transparency log, AP2 signs the shopping mandate, OpenTelemetry names the fields, the EU AI Act says logs must exist. No widely adopted profile yet joins them into **one receipt per transaction that a stranger can verify offline and a person can challenge**. This paper proposes that receipt — content-free, signed, chained, interface-agnostic, with contestability inside it — as a *profile that sits on the standards that exist*, contributed upstream rather than issued by the Foundation, and governed so that no party that sells the runtime, runs the log, assesses, or insures also grades its own interest.

## 1. The eight seams

Verified against the current landscape (sources in §9):

1. **No transaction identifier survives the interfaces.** Only China's labelling rules (in force 1 Sep 2025) require a per-output "content reference number". MCP's 2026-07-28 spec *removed* session ids; OpenTelemetry's `gen_ai.*` conventions are still "Development" and unsigned. No id follows chat → API → agent → extension → product.
2. **Identity is split three ways and never bound.** Human (OIDC, W3C VC 2.0), workload (SPIFFE/WIMSE, `draft-klrc-aiagent-auth-03`), and agent/model (A2A signed Agent Cards; ITU FG-TIDA, first meeting Nov 2026). Nothing signs *human + agent + model version + tool* together at call time without a stable personal identifier.
3. **Policy decisions are asserted, not attested.** ISO 42001, NIST AI RMF, CSA AICM v1.1 and EU Arts 9–14 say controls must exist; OVERT 1.1 specifies a per-action proof that a control ran — and OVERT has one vendor implementation, no registered Independent Attestation Provider, and no assessor registry yet. The EU's harmonised logging standard, prEN 18229-1, is at Enquiry stage.
4. **Transparency logs have a transport but no AI payload.** RFC 9943 (SCITT architecture) and RFC 9942 (COSE receipts) were published June 2026; there is no registered SCITT statement profile for "AI inference / agent action". OVERT does not reference SCITT.
5. **Provenance is bound to the asset, not the session.** C2PA 2.3 and IPTC 2025.1 describe what produced a *file*; free-form text, voice and code — most of what generative AI emits — carry nothing, and platforms strip manifests.
6. **Audit rights stop at the organisation.** EU Art. 12/26(6) logs are for the provider, deployer and regulator; ISO 42006 accredits auditors of *management systems*; there is no "verify with a public key, offline" norm outside Sigstore and OVERT tooling.
7. **Incidents are narrative.** Art. 73 templates, OECD AIM, AIID and the Frontier Model Forum's incident sharing accept prose; none takes a receipt hash or inclusion proof as the anchor. NYC Local Law 144's audit regime produced two complaints and no enforcement in two years — evidence that summaries without artefacts do not work.
8. **Interfaces are uneven, and contestability is a footnote.** Voice has no marking channel; coding agents have AGENTS.md (guidance); on-device AI has RATS (RFC 9334) but no AI profile; A2A puts authorisation out of scope by design; commerce protocols (AP2, Visa TAP, Mastercard Verifiable Intent, OpenAI/Stripe ACP) prove *who* transacted but not *what the model did* between intent and cart. And in every one of these, the right to notice, explanation, challenge, review and remedy (EU Art. 86, Colorado SB 26-189) has no machine-readable home keyed to the event.

## 2. What exists, in one table

| Layer | Standard (steward, status) | What it answers | What it cannot |
|---|---|---|---|
| Organisation | ISO/IEC 42001:2023 (+42005 impact, 42006 audit bodies); NIST AI RMF 1.0 + AI 600-1 | Does the operator have a management system? | Anything about one transaction |
| Agent (periodic) | **AIUC-1** (AIUC; quarterly releases, Jul 2026 current; six domains; third-party audit + quarterly adversarial testing; insurance-priced; UiPath, Intercom, Cursor, Harvey, ElevenLabs, KPMG certified) | Was this agent tested and insured this quarter? | Whether the certified controls ran on *your* call |
| Decision (runtime) | **OVERT 1.1** (Glacis, 11 Jun 2026; six domains; AAL-1…4; IAP + Qualified Assessor defined, none registered) | Did a control execute on this action, signed and chained? | Cross-vendor adoption; SCITT/C2PA/OTel mapping; human mandate; contestability |
| Log | **IETF SCITT** RFC 9943 / RFC 9942 (Jun 2026); Sigstore Rekor v2 (Oct 2025) | Was the statement registered and unaltered? | What an AI statement should contain; who witnesses |
| Identity | W3C VC 2.0 / DID 1.1 CR; SPIFFE; `draft-klrc-aiagent-auth`; OpenID AIIM CG; Cloudflare Web Bot Auth (operator only, forbids human binding) | Who is the human / workload / bot? | Binding all three to one act, privately |
| Mandate | Google **AP2** (Sep 2025; Intent/Cart/Payment Mandates as VCs); Mastercard Verifiable Intent (Mar 2026); Visa TAP (RFC 9421 signatures); OpenAI/Stripe ACP (allowance tokens) | What did the human authorise the agent to buy? | Anything outside commerce; what the model did |
| Telemetry | OpenTelemetry GenAI semconv v1.42 (Development) | Field names for model, tokens, tools, agents | Signing; stability |
| Content | C2PA 2.3 (Feb 2026); IPTC 2025.1; EU Transparency Code (Jun 2026) + Art. 50 Guidelines (Jul 2026) | What produced this file? | Text/voice/code; the session |
| Supply chain | CycloneDX 1.7 ML-BOM; SPDX 3.0.1 AI profile; OpenSSF Model Signing 1.0 | What is the model made of? | The transaction |
| Regulation | EU AI Act as amended by (EU) 2026/1744: Art. 12 logging, Art. 50 (live 2 Aug 2026), Annex III 2 Dec 2027, Art. 73 incidents, Art. 86 explanation; Colorado SB 26-189 (1 Jan 2027); Korea AI Basic Act (22 Jan 2026); China labelling (1 Sep 2025); California SB 942 (2 Aug 2026) | What must be logged, disclosed, explained, reported | A format; a verifier |
| Incidents | OECD AIM; AIID; AIAAIC; FMF incident sharing (May 2026); MIT tracker | What went wrong, in prose | Linkage to evidence |
| Confidential compute | Apple PCC (expanded to Google Cloud, Jun 2026); Google Confidential Space; Intel Trust Authority | Which binary ran, in which enclave | What it answered |

## 3. The proposal

The normative text is `spec/ONE-RECEIPT-SPEC.md` in this repository; this section is the reading guide.

### 3.1 One receipt, one graph, ten predicates

A **receipt** is a content-free, signed statement about one *bounded event* — a request and its response, an agent action, a segment of a stream, a batch item, a review — chained into a transaction graph with an id, a root and parents, registered with a log, and carrying pointers and commitments (never payloads) to the evidence each stakeholder may later be entitled to see.

| Predicate | Binds | Built on |
|---|---|---|
| `transaction` | how the event was cut: interface, boundary, segment, id carrier, delegation depth | interface profiles; streaming/voice batching rule |
| `identity` | human (pseudonym), operator, agent, model version, tools — bound to one event, never a stable personal id | OIDC/VC 2.0 by reference; SPIFFE / Web Bot Auth; A2A Agent Card; SPDX/CycloneDX ref |
| `mandate` | what the human or authority authorised, and whether the action stayed inside it | AP2 / Verifiable Intent / TAP / ACP unchanged; a plain-words rule for non-commerce |
| `policy` | which gate ran, which version, allow/constrain/hold/escalate/deny, which controls with which outcomes, human in the loop | UCID, OVERT, AIUC-1, AICM, ISO 42001, NIST RMF control ids |
| `runtime` | salted commitments to input and output, counts, environment attestation reference, OTel ids, child receipts | OTel GenAI attributes; RATS; MCP/A2A ids |
| `provenance-disclosure` | what left, how it was marked, whether the AI nature was disclosed, in which languages and formats | C2PA 2.3; Art. 50; China reference number |
| `witness` | the independent log, checkpoint, inclusion and consistency proofs, witnesses, equivocation status | RFC 9943/9942; RFC 6962 |
| `contestability` | notice · explanation · challenge · human review with named authority · named remedies · collective redress | Art. 86; SB 26-189; the practice's gates |
| `legal-evidence` (optional) | jurisdiction profile, collection, custody, timestamp assurance, export manifest | eIDAS QTSA; FRE 901; CN online litigation |
| `community-authority` (extension) | collective authority, consent basis, use restrictions | CARE principles; drafted only with Indigenous partners |

Envelope: canonical JSON (a full RFC 8785 canonicaliser and a CBOR profile are v0.3 gates), Ed25519 by default with ES256, ML-DSA-65 and a hybrid in the algorithm registry; countersignatures from log operators, witnesses, time authorities, reviewers and assessors; a manifest that declares every predicate present and gives a reason for every one omitted; a privacy profile on every receipt; a non-empty `limitations` list on every receipt. Registered as a **SCITT statement profile** so any RFC 9943 transparency service can hold it. One receipt id, one URL pattern (`…/r/<id>`), one offline verifier that reports the level it could substantiate next to the level the issuer claimed.

### 3.2 Interface profiles

Same envelope; what changes is how the id is carried and how the person sees it.

| Interface | Id carrier | The person sees | Notes |
|---|---|---|---|
| Chat / web | Response header + a visible "receipt" affordance | A link under every answer | The café's Wren Card pattern |
| API | `AI-Receipt` response header; request may carry `AI-Mandate` | The SDK prints it | Maps 1:1 to an OTel span |
| Voice | Spoken id on request; id in the transcript | "Say 'receipt'" → the aggregate receipt of the stream | Fills the channel Art. 50 admits is weak; streams batch per turn or window, never per token |
| Agent-to-agent | Message metadata; nested receipts per hop; a delegation receipt per hand-off | The root receipt for the human principal | MCP has no session id — the receipt graph is the session; a mandate never widens down the chain |
| IDE / coding agent | `One-Receipt:` git trailer | In the commit | Coding agents already sign commits |
| Embedded / phone | On-device receipt with environment evidence; uploads when online | Settings → receipts | RATS profile; environment-level only |
| Commerce | AP2 Cart Mandate hash in `mandate` | The merchant receipt cites it | Visa/Mastercard/ACP compatible; `within_mandate: no` is an honest record of a breach |

### 3.3 Four roles — and the separation rule

- **Operator** (seller/deployer) issues receipts and keeps the salts.
- **Log operator** registers them — a different party from the operator above OR-2, with witnesses co-signing checkpoints so equivocation can be caught and frozen.
- **Assessor** verifies samples without content access — never the operator, the log operator, the runtime seller, or the underwriter of the system it assesses; methodology and negative findings public.
- **Registry steward** publishes keys, profiles, assessor and public-interest review records — never the sole long-term steward, never a party with a commercial interest in an issuer it lists.
- **Verifier** is anyone with the public key and, above OR-1, the log — no account, no vendor dashboard.

Assurance is an evidence ladder the verifier computes, not a badge the issuer claims: **OR-0** unverified export · **OR-1** issuer signed · **OR-2** operator logged · **OR-3** independently logged and witnessed · **OR-4** independently assessed · **OR-5** public-interest accountable. It deliberately does not borrow OVERT's AAL levels or any certification tier, and it says nothing about the AI system's quality. What it adds to the periodic world is the **certificate-to-receipt link**: a quarterly certificate (AIUC-1, ISO 42001) becomes checkable against per-call evidence — "you said control A006 exists; show me it ran on the calls that mattered."

### 3.4 What each party can now ask, and get

| Party | Question | Answered by |
|---|---|---|
| Buyer / deployer | Which model and policy version served this call? Did the certified control run? Can I keep six months of evidence without holding content, and take it with me when I switch vendors? | `identity`, `policy`, `runtime`, `witness`; the procurement profile |
| End user / affected person | Was I talking to an AI, run by whom? What did I authorise, and did the agent stay inside it? Where is the explanation this interaction owes me? Who reviews, with what authority, and what remedies are named? | `identity`, `mandate`, `provenance-disclosure`, `contestability` — and the challenge, review and remedy receipts that answer it in the same graph |
| Regulator | Is the vendor's claim traceable to production runs? Was the log altered after the incident? Can I inspect without trade secrets? | `policy`, `runtime`, `witness`; authorised opening of commitments as a `review` receipt; the regulator-view package |
| Civil society | Is this system in a public register, and does the receipt say so? Can an independent assessor verify a sample without the vendor's cooperation? Is there a challenge route keyed to the receipt id, and can a representative use it? | `contestability` (`collective_redress`), the assessor role, the Public Interest Council's binding review |
| Seller / vendor | Can I prove controls ran without exposing prompts or weights? Is human intent separated from my agent's identity so I am not liable for what I never authorised? | Content-free by design; `mandate` separates the human from the agent; per-call evidence a certificate cannot produce — and no claim about premiums until someone publishes the evidence |

## 4. What it improves on

**The AiGovOps Foundation.** Beacon already signs Ed25519 over JCS with an append-only Merkle log and an offline `VERIFY.md`; Umbrella already compiles law to UCIDs and binds evidence to controls; Lantern already reads them; Replay and prompt-studio share the wire format. What the Foundation's receipt lacks is the *shape* — it is its own envelope, not a SCITT statement; it carries an OIDC subject and plain hashes where v0.2 requires a pseudonym and salted commitments; it has no `mandate`, no interface profiles, no witness, no contestability, no certificate link. `docs/ADOPTION.md` and `adapters/` give each project its delta and its version. The ladder maps rung-for-rung — a 100 reads a receipt, a 200 emits one from CI, a 300 registers a hold, a 400 verifies a stranger's offline — and gains 500 (witness and assess) and 600 (review with authority). The Foundation's own rule stands and is now in the spec: it issues no standard, grades no receipts, and is not the long-term registry, assessor qualifier or notary.

**Glacis / OVERT.** OVERT is the best-specified per-decision receipt in the field and this proposal keeps its control evidence intact as a control vocabulary and an extension. It improves on it in four ways OVERT's own crosswalks leave open: (1) a SCITT profile so any transparency service can hold OVERT receipts, not only Glacis's notary; (2) OTel, C2PA and AP2 mappings; (3) explicit human-mandate, disclosure and contestability predicates (OVERT scopes out truthfulness and user-facing obligations); (4) a governance separation — today the OVERT steward sells the runtime and would qualify the assessors, and no assessor or IAP is registered fourteen months after 1.0. The ask to Glacis: sign the Beacon profile; co-author the SCITT profile; join as a proposed inaugural technical contributor under the conflict rules; let the community's 400s form the first verification pool.

**AIUC-1 and the insurance track.** AIUC-1 is the strongest *periodic* certification — audited, adversarially re-tested quarterly, priced into cover — and its consortium (UiPath among the founding contributors) is the widest industry table. Its limits are structural: a certificate says the agent passed last quarter, not that control A006 ran on this call; the standard's editor also accredits auditors and underwrites the policy. One Receipt gives AIUC-1 what it cannot produce itself — per-call evidence that a certified control executed — and gives insurers a loss-adjustment artefact. The ask: an AIUC-1 requirement that certified agents emit receipts, and a control-id vocabulary shared with OVERT and UCID. This paper makes no claim about premiums; the playbook forbids one without independent published evidence.

## 5. Standards path and governance

1. **IETF SCITT** — an Internet-Draft "AI Transaction Statement Profile" (the envelope as the signed statement; RFC 9942 receipts as inclusion proofs; witness co-signatures). Co-authors sought from Glacis, the SCITT editors, and one log operator.
2. **OVERT** — a registered profile `one-receipt.v0` under Agentic-Extended scope; Beacon's `aigovops-beacon.v1` conforms to it.
3. **OpenTelemetry** — a mapping table `gen_ai.*` ↔ predicate fields, submitted to the semantic-conventions-genai repo.
4. **C2PA** — an assertion type carrying the receipt id, so a signed file points back to the event.
5. **AP2 / Mastercard Verifiable Intent** — the `mandate` slot accepts their credentials unchanged; test vectors from their samples.
6. **NIST AI Agent Standards Initiative / NCCoE** — the interface-profile matrix as a public-interest use-case submission; **ITU FG-TIDA** (Nov 2026) for the identity binding.
7. **EU** — feed the six-month retention and content-free pattern into the prEN 18229-1 (Art. 12 logging) enquiry; propose the receipt id as the Art. 73 incident anchor; the contestability object as the Art. 86 evidence shape.

Governance is the Global One Receipt Collaborative (`governance/`): a Technical Incubator, a paid Public Interest Council with binding review, an Adoption and Pilot Network, an Independent Appeals Panel and a Standards Liaison Forum; funding caps (no contributor above 15%, no sector above 35%, at least 20% for paid public-interest participation, at least 20% for independent research); at least half of non-vendor seats outside North America and the EU; royalty-free IPR; vectors and the reference verifier in the open; and a founding cohort of 18–24 balanced parties invited in the playbook's order — standards communities and public-interest partners before vendors.

## 6. Ninety days for the Foundation

- **Weeks 1–3:** decisions taken; this repository public; Beacon emits v0.2 behind a flag from its existing signer; the ten corpus vectors chosen.
- **Weeks 4–6:** Lantern shows claimed vs verified; the café's Wren Card carries a receipt id; the 200 and 400 worksheets gain their receipt steps.
- **Weeks 7–9:** the Glacis note with the delta matrix; the SCITT -00 outline; the NIST submission; a Thursday devoted to a stranger verifying a receipt offline.
- **Weeks 10–13:** first external verification by a 400; the joint story; v0.2.1 with what broke; the first listening invitations out in order.

## 7. Risks and open questions

Salted commitments are the privacy floor, but content-free is not anonymous: graph shape, timing and counts leak, and the spec says so. A hash cannot explain — the contestability object must be honoured or Art. 86 is unmet. Streams need the batching rule and a closing aggregate, and the rule must hold for voice. On-device and TEE evidence is environment-level, not answer-level; the paper does not claim otherwise. zkML proof-of-inference (Lagrange DeepProve, EZKL) is not viable per request at frontier scale in 2026. A witnessed log can still be attacked by collusion between operator and witnesses — hence the requirement for more than one independent route above OR-2. The legal-evidence profile describes what was done; a court decides what it accepts. Adoption will follow procurement clauses, not goodwill — the EU model contractual clauses (MCC-AI, Mar 2025) and buyer evidence-rights templates are the levers. And the Foundation must not become the thing it warns against: it implements and teaches; it does not grade its own receipts.

## 8. Decisions for Ken and Bob

The twelve executive decisions are in `docs/MASTER-PLAN.md` §16. The four from v0.1 survive as decisions 1, 4, 5 and 8: the name; when to send the Glacis ask; who hosts the working group; which ten corpus cases become the first vectors (twelve are seeded).

## 9. Sources (selected; full memos in the practice repo, `docs/reference/research/`)

OVERT 1.1 standard, conformance and crosswalks (overt.is); Glacis docs and verifier (docs.glacis.io, verify.glacis.io); GeekWire on Glacis (7 Apr 2026); AIUC-1 site and changelog (aiuc-1.com); UiPath AIUC-1 announcements (19 Nov 2025; 9 Mar 2026); RFC 9943, RFC 9942, RFC 9901, RFC 9421, RFC 6962, RFC 8785; draft-klrc-aiagent-auth-03; draft-meunier-web-bot-auth-architecture-05; Regulation (EU) 2026/1744 and law-firm summaries (White & Case, Orrick, Gibson Dunn); AI Act Explorer Arts 12, 14, 50, 71, 73, 78, 86; Commission Transparency Code (10 Jun 2026) and Guidelines (20 Jul 2026); KLA JTC 21 tracker (prEN 18229-1); C2PA 2.3 spec; IPTC 2025.1; Google AP2 announcement; Visa Trusted Agent Protocol; Mastercard Verifiable Intent (PYMNTS, 5 Mar 2026); OpenAI ACP delegated payment spec; Cloudflare Web Bot Auth; Linux Foundation AAIF and A2A releases; MCP spec 2026-07-28; OpenTelemetry semconv 1.41/1.42; CSA AICM v1.1; MITRE ATLAS v2026.08; OWASP Agentic Top 10 (2026); NIST AI Agent Standards Initiative; NCCoE agent identity concept paper; ITU FG-TIDA; NY State Comptroller audit of Local Law 144 (2 Dec 2025); Colorado SB 26-189; Korea AI Basic Act (Cooley); China labelling measures (China Law Translate); Ada Lovelace *Code & Conduct*; Apple PCC expansion (8 Jun 2026); Lagrange DeepProve-1; Attested Intelligence AGA; CARE Principles for Indigenous Data Governance (GIDA).
