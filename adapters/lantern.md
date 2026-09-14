# Adapter — aigovops-lantern (the reader)

**Today.** "Beacon signs. Lantern reads." Lantern verifies Beacon receipts and the log offline for the human carrying it.

**Delta (0.2.0).** Lantern becomes the Foundation's reference verifier UI:

- Embeds the reference verifier (Python today; the TypeScript SDK when it passes the vectors) and shows, for every receipt: **claimed level**, **verified level**, why they differ (the verifier's warnings), and the `limitations` text verbatim.
- Draws the transaction graph (root, parents, delegation depth) and reports the weakest verified level as the transaction's level.
- Renders `contestability` as actions: "Ask for the explanation", "Challenge this", "Who reviews, with what authority?", "What remedies are named?" — each opening the route the receipt names.
- Gate lenses (Lantern #9) read `policy.decision` and `policy.controls[]` by vocabulary.
- Never shows a receipt as "anonymous" or "certified"; shows OR-4/OR-5 only after a registry lookup it performed.
- Reads the v0.1-era Beacon/Replay format through `adapters/replay.md` and labels it "legacy — OR-0".
