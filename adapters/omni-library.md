# Adapter — aigovops-library / Omni (Gate Check, decide.html)

**Today.** The governed multi-agent core; Gate Check; `decide.html` (level-100 step 4) produces allow/constrain/hold/deny with a SHA-256 decision receipt in the browser; Library ticket T10 is the blocking JCS canonicaliser.

**Delta (4.1).**

- `decide.html` emits a v0.2 `policy-decision` envelope at **OR-0** (`signature.value: "unsigned"`) in the browser; a practitioner who holds a key signs it to OR-1 with the TypeScript SDK when it exists.
- The SHA-256 of the decision becomes a salted `policy_commitment`; the plain hash is retired.
- T10 (JCS canonicaliser) is the shared v0.3 deliverable: one implementation, tested against `testkit/vectors`, used by Beacon, Omni and this repo.
- Gate Check's door suggestion records nothing personal; if it emits a receipt it is `identity.principal_binding_mode: none`.
