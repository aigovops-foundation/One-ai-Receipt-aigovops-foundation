# Adapter — aigovops-prompt-studio (prompt-level audit)

**Today.** Prompt engineering platform with wizard UI, 2FA, immutable audit logging and version control.

**Delta (next tag).**

- Each prompt version is committed to (`policy_commitment` on a `policy-decision` receipt whose `policy_id` is the prompt id and `version` its version) — the prompt text never enters the receipt.
- Each run emits an `inference` receipt with `identity.model`, `runtime.counts` and salted `input_commitment` / `output_commitment`.
- Each 2FA approval emits a `human-review` receipt with `policy.human_in_loop: approved` and `contestability.human_review.reviewer_authority: override`.
- The immutable audit log registers receipts and exposes checkpoints and inclusion proofs so runs reach OR-2 inside the studio and OR-3 with an external log.
