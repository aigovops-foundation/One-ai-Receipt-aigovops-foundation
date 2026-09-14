# Adapter — umbrella-govops (the gate)

**Today.** Governance as executable code: YAML policy orchestration mapping NIST AI RMF and the EU AI Act to CI/CD checks, UCID control ids, cryptographically signed evidence bundles.

**Delta (0.1.0, first PyPI).**

- Every gate evaluation emits a `policy-decision` receipt: `policy.policy_id` = the YAML policy id, `policy.version` = its version, `policy_commitment` = salted commitment to the policy text, `decision` ∈ allow/constrain/hold/escalate/deny, `enforcement_point: pre-action` (CI) or `in-flight` (runtime), `controls[]` = the UCIDs checked with `vocabulary: ucid` and outcomes, `jurisdiction_refs[]` = the articles the policy maps.
- The signed evidence bundle's signature is attached as a `countersignature` with role `reviewer`; the bundle id goes to `controls[].evidence_ref`.
- UCID is registered as a control vocabulary in `spec/registries`; the UCID ↔ OVERT ↔ AIUC-1 ↔ AICM crosswalk lives here and is contributed upstream.
- Umbrella never signs `inference` receipts; it declares and gates. Beacon signs what ran.
