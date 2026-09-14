# Adapter — aigovops-Replay (legacy receipt verifier)

**Today.** "Cryptographically signed receipt system for AI interactions"; Beacon's receipt schema is wire-compatible with it.

**Delta (next tag).**

- Replay's verifier gains a v0.2 mode: it runs `testkit/vectors` in CI and verifies v0.2 envelopes with the same verdicts as the reference verifier.
- The existing Replay/Beacon format is frozen as the **legacy profile**: documented in `spec/delta-matrix.md`, readable by Lantern as "legacy — OR-0", never extended.
- Migration note for users: legacy receipts carry plain hashes and OIDC subjects; they cannot be upgraded in place — re-emission with salts and pseudonyms is the path.
