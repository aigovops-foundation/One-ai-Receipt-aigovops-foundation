# Crosswalk — SAIL v2 risks ↔ One Receipt evidence

**SAIL** (Secure AI Lifecycle) is Pillar Security's risk catalogue and roadmap process: v1 June 2025 (seven phases, 70+ risks), **v2 published 8 July 2026** (91 risks, agent-specific, three deployment zones, autonomy tiers), mapped by Pillar to ISO/IEC 42001, NIST AI RMF, OWASP Top 10 for Agentic Applications (2026) and for LLM Applications (2025), the EU AI Act, DASF and AIUC-1, and distributed as an installable skill (`pillar-labs/sail-skill`).

**Licence note (binding on this repository).** SAIL is CC BY-NC-SA 4.0 with an internal-use carve-out; redistribution or incorporation into products offered to third parties requires a separate licence from Pillar. This crosswalk therefore cites SAIL risks **by id only** and never reproduces descriptions, mitigations or mapping tables. An implementer who wants the text installs SAIL from Pillar. A liaison invitation and a request for a carve-out covering titles is in the playbook queue (group 3).

**What the crosswalk means.** SAIL says what could go wrong and what control should exist. One Receipt is the evidence that the control *ran on this event*. A receipt that carries `policy.controls[]` with `vocabulary: sail` and `id: "SAIL 5.13"` is an operator's signed claim that the mitigation for that risk executed with the stated outcome — nothing more; the verifier says so in `limitations`.

| SAIL id (phase) | One Receipt evidence | Predicate / field | Foundation project that emits it |
|---|---|---|---|
| 1.11 autonomy-level classification | the declared control intensity per agent | `policy.tier` (e.g. `sail:tier-2`), `policy.risk_class` | Umbrella declares |
| 1.12 / 3.16 action-authorisation policy | a policy version bound to every consequential event | `policy.policy_id`, `policy.version`, `policy_commitment` | Umbrella |
| 1.13 agentic identity policy | each agent named with a workload identity scheme | `identity.agent{id, workload_identity}` | Beacon, Jeeves |
| 2.1 / 2.2 asset inventory, third-party integrations | model, tool and BOM references per event | `identity.model{ref, version, bom_ref}`, `identity.tool_ids[]` | Beacon (discovery) |
| 2.6 untracked agent identities | every acting agent appears in a receipt | `identity.agent`, `issuer` | Beacon, Jeeves |
| 2.7 unmapped inter-agent topology | the delegation graph is the topology | `agent-delegation` receipts, `parent_receipt_ids`, `transaction.delegation_depth` | Jeeves |
| 3.2 / 5.2 insecure or tampered agent instructions | a commitment to the instruction set in force | `policy_commitment` (salted) per version; mismatch across events is visible | prompt-studio, Beacon |
| 3.6 insufficient human oversight | who approved, with what authority | `policy.human_in_loop`, `contestability.human_review.reviewer_authority` | Umbrella, practice |
| 3.13 over-scoped tool permissions | tools actually invoked vs mandate | `identity.tool_ids[]`, `mandate.scope`, `mandate.within_mandate` | Jeeves |
| 5.7 insecure memory and telemetry storage; 7.4 exfiltration via telemetry | evidence that carries no content and no stable identifiers | `privacy_profile`, `runtime.content_included: false`, salted commitments | all issuers |
| 5.10 policy-violating action | the gate decision on the action | `policy.decision` ∈ constrain/hold/escalate/deny; `policy-decision` receipt | Umbrella, Omni `decide.html` |
| 5.13 missing action-level authorisation | one `policy-decision` receipt per action, `enforcement_point: pre-action`, boundary `agent-action` | `policy`, `boundary` | Umbrella + Beacon |
| 5.17 maker-identity inheritance; 5.20 confused deputy | the requesting principal, not only the agent, bound to the action, and whether it stayed inside its mandate | `identity.principal_binding_mode`, `identity.principal_ref` (pseudonym), `mandate.within_mandate`, mandate inherited by reference | Jeeves, Beacon |
| 5.18 session smuggling / A2A impersonation | every hand-off is a signed receipt naming both agents | `agent-delegation` receipts; `identity.agent.workload_identity`; countersignatures | Jeeves |
| 5.19 unsafe consumption of output downstream | the output-delivery event and its commitment | `output-delivery` receipt, `runtime.output_commitment`, `provenance-disclosure.output_kind` | Beacon |
| 6.4 task decomposition for policy evasion | the whole graph, verified as one transaction (weakest link reported) | `verify_graph`, `root_receipt_id`, `sequence` | Lantern verifies |
| 6.7 cross-agent abuse | as 5.18 | | |
| 6.13 approval fatigue | how many holds a human cleared, with what SLA | `human_in_loop` counts across the graph; `contestability.human_review.sla_hours` | practice level 300 |
| 6.14 irreversible actions without rollback | whether reversal was a named remedy before the action | `contestability.remedy.types` includes `reversal`; `remedy` receipts | practice, Omni |
| 7.1 insufficient interaction logging | a receipt per inference, tool call, delegation, review and delivery, chained | the graph; `transaction_type` | Beacon, Jeeves |
| 7.3 undetected agent drift | model/version/policy version per event over time | `identity.model.version`, `policy.version` | Beacon, Lantern |
| 7.5 incident response, tamper-evident evidence capture | signed, logged, witnessed receipts and an `incident` receipt with proofs | `witness`, `incident` receipts, `legal-evidence` profile | Beacon, log-lab |
| 7.7 untracked decommissioning | a closing receipt for the agent's last transaction; key revocation record with the registry steward | `aggregate` receipt + `extensions.aigovops.lifecycle: retired`; registry revocation (v0.3 proposes `transaction_type: lifecycle-event`) | Jeeves, registry |

**Not covered by receipts, by design:** red-teaming coverage (phase 4), sandbox configuration (6.1–6.3, 6.11–6.12), supply-chain vetting (3.1, 3.8, 3.17), credentials in artefacts (3.9, 3.12). A receipt can reference the evidence (`controls[].evidence_ref`) but cannot prove it; SAIL's own roadmap and the AIUC-1/ISO audits are the right instruments there.

**Lifecycle alignment.** SAIL Plan → Declare; SAIL Build/Deploy (action authorisation) → Gate; SAIL Deploy/Operate (runtime, sandbox) → Prove; SAIL Govern (monitor) → Verify and Improve; nothing in SAIL maps to **Contest** — user notice, challenge, review and remedy are outside its scope, which is the largest thing One Receipt adds to a SAIL-shaped program.
