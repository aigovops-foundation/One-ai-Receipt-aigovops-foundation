# Adapter — aigovops (Jeeves, the orchestrator)

**Today.** Orchestrates Beacon, Lantern and Umbrella.

**Delta (4.1).** Jeeves owns the transaction graph:

- Opens a `transaction_id` per task and assigns `root_receipt_id` to the first receipt (usually Umbrella's pre-action `policy-decision`).
- Emits an `agent-delegation` receipt for every hand-off between agents with `identity.agent`, `transaction.delegation_depth` and the mandate inherited by `mandate.mandate_ref`; the mandate scope never widens down the chain.
- Closes streams and batches with an `aggregate` receipt that names every segment or declares `dropped_events_declared`.
- Runs `verify_graph` before reporting a task complete and records the weakest verified level in the task log.
