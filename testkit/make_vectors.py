"""Regenerate examples/ and testkit/vectors/ from the corpus cases.

Run from the repository root:  python testkit/make_vectors.py
Uses the demonstration keypair in examples/ (never use it in production). Every vector
records what a conformant verifier must conclude, so a second implementation can prove
it agrees without sharing code.
"""
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT / "src"))
from one_receipt.core import commit, emit_receipt, verify_receipt  # noqa: E402

PRIV = (ROOT / "examples" / "private-key.pem").read_bytes()
PUB = (ROOT / "examples" / "public-key.pem").read_text()
ISSUER = "did:web:cafe.aigovops-foundation.example"
KID = ISSUER + "#receipt-2026-09"
LOG = "did:web:log.independent.example"

CONTEST_OK = {
    "notice": {"given": True, "channel": "in-interface", "languages": ["en", "es"]},
    "explanation": {"available": True, "kind": "decision-summary"},
    "challenge": {"available": True, "cost": "free", "representative_allowed": True},
    "human_review": {"available": True, "reviewer_authority": "override", "reviewer_independent": True, "sla_hours": 72},
    "remedy": {"types": ["correction", "reversal"], "collective_redress": False},
}


def base(case: str, interface: str, policy: dict, contest: dict | None = CONTEST_OK, extra: dict | None = None) -> dict:
    preds = {
        "transaction": {"interface": interface, "id_carrier": "response-header"},
        "identity": {"principal_binding_mode": "pseudonymous", "principal_ref": f"pseud:{case.lower()}", "operator_id": ISSUER, "model": {"ref": "example:model", "version": "2026-09"}},
        "mandate": {"scheme": "plain-words-rule", "scope": "answer within published policy", "within_mandate": "yes"},
        "policy": {"policy_id": f"corpus-{case}", "version": "1", "enforcement_point": "pre-action", **policy},
        "runtime": {"content_included": False, "counts": {"input_tokens": 412, "output_tokens": 96}},
        "provenance-disclosure": {"ai_disclosed": True, "disclosure_channel": "visible-text", "output_kind": "text"},
    }
    if contest:
        preds["contestability"] = contest
    if extra:
        preds.update(extra)
    return {"predicates": preds, "started_at": "2026-09-14T15:00:00Z", "ended_at": "2026-09-14T15:00:02Z", "extensions": {"aigovops.corpus": {"case": case}}}


def witness(log=LOG, witnesses=True, status="not-observed"):
    w = {"log_operator": {"id": log, "kind": "scitt"}, "log_checkpoint": {"tree_size": 4096, "root_hash": "c0ffee"}, "inclusion_proof": {"leaf_index": 41, "hashes": ["a1", "b2", "c3"], "format": "rfc6962"}, "observed_at": "2026-09-14T15:00:03Z", "equivocation_status": status}
    if witnesses:
        w["witnesses"] = [{"id": "did:web:witness.example", "observed_at": "2026-09-14T15:00:04Z"}]
    return w


def emit(p, **kw):
    kw.setdefault("issuer_id", ISSUER)
    kw.setdefault("key_id", KID)
    return emit_receipt(p, PRIV, **kw)


vectors: list[tuple[str, str, dict, dict | None, dict]] = []  # name, case, receipt, registry, expect


def add(name, case, receipt, expect, registry=None):
    vectors.append((name, case, receipt, registry, expect))


# 1 — VH-001 Air Canada: chat answer under a published policy; the receipt makes the answer contestable.
p = base("VH-001", "chat", {"decision": "allow", "controls": [{"id": "UCID-POLICY-TRUTH", "vocabulary": "ucid", "outcome": "pass"}]})
c, _ = commit("the bereavement-fare answer", scheme="salted-sha256")
p["predicates"]["runtime"]["output_commitment"] = c
r1 = emit(p, assurance="OR-1")
add("01-chat-or1-valid", "VH-001 Air Canada", r1, {"valid": True, "verified_level": "OR-1"})
(ROOT / "examples" / "chat-air-canada-or1.json").write_text(json.dumps(r1, indent=2) + "\n")

# 2 — tampered decision
t = copy.deepcopy(r1)
t["predicates"]["policy"]["decision"] = "deny"
add("02-chat-tampered-invalid", "VH-001 Air Canada", t, {"valid": False, "verified_level": None})

# 3 — VH-056 Knight Capital: an agent action that a policy gate held; OR-2 with an operator-run log.
p = base("VH-056", "api", {"decision": "hold", "controls": [{"id": "UCID-KILL-SWITCH", "vocabulary": "ucid", "outcome": "pass"}], "human_in_loop": "approved"}, extra={"witness": witness(log=ISSUER, witnesses=False)})
p["predicates"]["transaction"]["interface"] = "agent-to-agent"
r3 = emit(p, assurance="OR-2", transaction_type="policy-decision", boundary="agent-action")
add("03-agent-hold-or2-valid", "VH-056 Knight Capital", r3, {"valid": True, "verified_level": "OR-2"})

# 4 — same receipt claims OR-3 without an independent log → verified OR-2
r4 = emit(p, assurance="OR-3", transaction_type="policy-decision", boundary="agent-action")
add("04-agent-claims-or3-capped-or2", "VH-056 Knight Capital", r4, {"valid": True, "verified_level": "OR-2"})

# 5 — VH-013 Robodebt: automated benefit decision with independent log and witness → OR-3
p = base("VH-013", "batch", {"decision": "constrain", "risk_class": "annex-iii-social-benefits", "controls": [{"id": "A-14-HUMAN-OVERSIGHT", "vocabulary": "iso-42001", "outcome": "pass"}], "human_in_loop": "approved"}, extra={"witness": witness()})
p["predicates"]["transaction"]["interface"] = "batch"
r5 = emit(p, assurance="OR-3", transaction_type="policy-decision", boundary="batch")
add("05-benefit-decision-or3-valid", "VH-013 Robodebt", r5, {"valid": True, "verified_level": "OR-3"})

# 6 — equivocation suspected on the same log → frozen at OR-2
p6 = copy.deepcopy(p)
p6["predicates"]["witness"] = witness(status="suspected")
add("06-equivocation-frozen-or2", "VH-013 Robodebt", emit(p6, assurance="OR-3", transaction_type="policy-decision", boundary="batch"), {"valid": True, "verified_level": "OR-2"})

# 7 — VH-035 Cigna: contestability omitted on a consequential decision → signed but capped at OR-1
p = base("VH-035", "batch", {"decision": "deny", "risk_class": "health-coverage"}, contest=None, extra={"witness": witness()})
p["omissions"] = {"contestability": "not-collected"}
add("07-contestability-omitted-capped-or1", "VH-035 Cigna", emit(p, assurance="OR-3", transaction_type="policy-decision", boundary="batch"), {"valid": True, "verified_level": "OR-1"})

# 8 — VH-088 Horizon: OR-4 claimed; verified only when the registry shows an independent assessor
p = base("VH-088", "embedded", {"decision": "allow", "controls": [{"id": "UCID-LEDGER-RECONCILE", "vocabulary": "ucid", "outcome": "pass"}]}, extra={"witness": witness()})
r8 = emit(p, assurance="OR-4")
add("08-or4-without-registry-capped-or3", "VH-088 Horizon", r8, {"valid": True, "verified_level": "OR-3"})
add("09-or4-with-registry-valid", "VH-088 Horizon", r8, {"valid": True, "verified_level": "OR-4"}, registry={ISSUER: {"assessor_id": "did:web:assessor.example", "assessment_valid_until": "2027-03-31"}})

# 10 — privacy: a stable personal identifier in principal_ref is rejected
p = base("VH-015", "chat", {"decision": "allow"})
p["predicates"]["identity"]["principal_ref"] = "someone@example.com"
add("10-personal-identifier-invalid", "VH-015 Arup", emit(p, assurance="OR-1"), {"valid": False, "verified_level": None})

# 11 — VH-022 Chevy $1 Tahoe: commerce mandate; the agent left its mandate → still a valid receipt (it records the breach)
p = base("VH-022", "commerce", {"decision": "allow", "controls": [{"id": "UCID-PRICE-FLOOR", "vocabulary": "ucid", "outcome": "fail"}]})
p["predicates"]["mandate"] = {"scheme": "ap2-cart", "scope": "quote a vehicle at list price", "within_mandate": "no", "mandate_ref": "ap2:cart:demo"}
add("11-commerce-outside-mandate-valid", "VH-022 Chevrolet of Watsonville", emit(p, assurance="OR-1", transaction_type="output-delivery"), {"valid": True, "verified_level": "OR-1"})

# 12 — unsigned export: OR-0 only
p = base("VH-001", "chat", {"decision": "allow"})
add("12-unsigned-export-or0", "VH-001 Air Canada", emit(p, assurance="OR-0"), {"valid": True, "verified_level": "OR-0"})

out = ROOT / "testkit" / "vectors"
out.mkdir(parents=True, exist_ok=True)
for old in out.glob("*.json"):
    old.unlink()
for name, case, receipt, registry, expect in vectors:
    doc = {"spec_version": "0.2-draft", "case": case, "receipt": receipt, "public_key": PUB, "expect": expect}
    if registry:
        doc["registry"] = registry
    (out / f"{name}.json").write_text(json.dumps(doc, indent=2) + "\n")
    got = verify_receipt(receipt, PUB.encode(), registry=registry)
    assert (got["valid"], got["verified_level"]) == (expect["valid"], expect["verified_level"]), (name, got["errors"], got["warnings"])

# minimal example + payload
minimal = {"predicates": {"transaction": {"interface": "api"}, "policy": {"policy_id": "demo", "version": "1", "decision": "allow", "enforcement_point": "pre-action"}, "runtime": {"content_included": False}, "contestability": {"notice": {"given": True}, "explanation": {"available": False}, "challenge": {"available": True}, "human_review": {"available": False}}}}
(ROOT / "examples" / "minimal-payload.json").write_text(json.dumps(minimal, indent=2) + "\n")
(ROOT / "examples" / "minimal-receipt.json").write_text(json.dumps(emit(minimal, assurance="OR-1"), indent=2) + "\n")
print(f"wrote {len(vectors)} vectors and 2 examples")
