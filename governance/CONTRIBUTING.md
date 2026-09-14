# Contributing

Public issues and pull requests; Developer Certificate of Origin sign-off (`git commit -s`); two non-author approvals for normative changes (spec text, schemas, verifier rules, vectors); passing CI; security review for cryptographic changes; Public Interest Council review for privacy, contestability, accessibility and community-authority changes; a 30-day request-for-comment period for breaking changes; dissent recorded, never removed.

Before proposing a field, check `spec/delta-matrix.md` — if an adjacent standard already has it, map to it. Before proposing a claim, check `spec/ONE-RECEIPT-SPEC.md` §0 — if the receipt cannot prove it, it does not go in.

Maintainer status is earned through sustained, constructive contribution across a release cycle and is not purchased through membership or sponsorship. Test vectors are regenerated only by `testkit/make_vectors.py`; a change to a verdict is a normative change.
