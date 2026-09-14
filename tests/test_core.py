import copy
import json
from pathlib import Path

import pytest

from one_receipt.core import (
    LEVELS,
    canonical_bytes,
    commit,
    emit_receipt,
    generate_keypair,
    open_commitment,
    verify_graph,
    verify_receipt,
)

ROOT = Path(__file__).parents[1]


def payload(**over):
    base = {
        "predicates": {
            "transaction": {"interface": "chat", "id_carrier": "response-header"},
            "identity": {"principal_binding_mode": "pseudonymous", "principal_ref": "pseud:7f3a", "operator_id": "did:web:cafe.example"},
            "mandate": {"scheme": "plain-words-rule", "scope": "answer the question", "within_mandate": "yes"},
            "policy": {"policy_id": "cafe-100", "version": "3", "decision": "allow", "enforcement_point": "pre-action", "controls": [{"id": "UCID-12", "vocabulary": "ucid", "outcome": "pass"}]},
            "runtime": {"content_included": False},
            "provenance-disclosure": {"ai_disclosed": True, "output_kind": "text"},
            "contestability": {
                "notice": {"given": True, "channel": "in-interface"},
                "explanation": {"available": True, "kind": "decision-summary"},
                "challenge": {"available": True, "cost": "free"},
                "human_review": {"available": True, "reviewer_authority": "override"},
            },
        }
    }
    base.update(over)
    return base


def witness(log_id="did:web:log.example", witnesses=True, status="not-observed"):
    w = {
        "log_operator": {"id": log_id, "kind": "scitt"},
        "log_checkpoint": {"tree_size": 1024, "root_hash": "abc"},
        "inclusion_proof": {"leaf_index": 7, "hashes": ["h1", "h2"], "format": "rfc6962"},
        "equivocation_status": status,
    }
    if witnesses:
        w["witnesses"] = [{"id": "did:web:witness.example", "observed_at": "2026-09-14T12:00:00Z"}]
    return w


@pytest.fixture(scope="module")
def keys():
    return generate_keypair()


def test_roundtrip(keys):
    private, public = keys
    r = emit_receipt(payload(), private)
    out = verify_receipt(r, public)
    assert out["valid"] and out["verified_level"] == "OR-1" and out["checks"]["signature"] is True


def test_tamper_fails(keys):
    private, public = keys
    r = emit_receipt(payload(), private)
    changed = copy.deepcopy(r)
    changed["predicates"]["policy"]["decision"] = "deny"
    assert not verify_receipt(changed, public)["valid"]


def test_wrong_key_fails(keys):
    private, _ = keys
    _, wrong = generate_keypair()
    assert not verify_receipt(emit_receipt(payload(), private), wrong)["valid"]


def test_limitations_required(keys):
    private, public = keys
    r = emit_receipt(payload(), private)
    r["limitations"] = []
    assert not verify_receipt(r, public)["valid"]


def test_unsigned_export_is_or0(keys):
    private, public = keys
    r = emit_receipt(payload(), private, assurance="OR-0")
    out = verify_receipt(r, public)
    assert out["valid"] and out["verified_level"] == "OR-0" and out["checks"]["signature"] is None
    r["assurance_level"] = "OR-1"
    assert not verify_receipt(r, public)["valid"]


def test_no_key_caps_at_or0(keys):
    private, _ = keys
    out = verify_receipt(emit_receipt(payload(), private), None)
    assert out["valid"] and out["verified_level"] == "OR-0"


def test_critical_omission_needs_reason_and_caps(keys):
    private, public = keys
    p = payload()
    del p["predicates"]["contestability"]
    p["omissions"] = {"contestability": "deferred-to-parent"}
    r = emit_receipt(p, private, assurance="OR-2")
    out = verify_receipt(r, public)
    assert out["valid"] and out["verified_level"] == "OR-1" and not out["checks"]["critical_complete"]
    # strip the reason after signing → manifest check fails before signature even matters
    r2 = copy.deepcopy(r)
    for m in r2["predicate_manifest"]:
        m.pop("omission_reason", None)
    assert not verify_receipt(r2, public)["valid"]


def test_undeclared_predicate_fails(keys):
    private, public = keys
    r = emit_receipt(payload(), private)
    r["predicates"]["legal-evidence"] = {"jurisdiction_profile": "generic", "collection_method": "x", "collector_identity": "y", "timestamp_assurance": "issuer-clock"}
    out = verify_receipt(r, public)
    assert not out["valid"] and any("not declared" in e for e in out["errors"])


def test_assurance_ladder(keys):
    private, public = keys
    # OR-2 claimed with no witness → OR-1
    out = verify_receipt(emit_receipt(payload(), private, assurance="OR-2"), public)
    assert out["valid"] and out["verified_level"] == "OR-1"
    # OR-2 with operator-run log → OR-2
    p = payload()
    p["predicates"]["witness"] = witness(log_id="did:web:example.org", witnesses=False)
    out = verify_receipt(emit_receipt(p, private, assurance="OR-2"), public)
    assert out["verified_level"] == "OR-2"
    # OR-3 with operator-run log → capped OR-2
    out = verify_receipt(emit_receipt(p, private, assurance="OR-3"), public)
    assert out["verified_level"] == "OR-2"
    # OR-3 with independent log + witness → OR-3
    p["predicates"]["witness"] = witness()
    out = verify_receipt(emit_receipt(p, private, assurance="OR-3"), public)
    assert out["verified_level"] == "OR-3"
    # equivocation freezes at OR-2
    p["predicates"]["witness"] = witness(status="suspected")
    out = verify_receipt(emit_receipt(p, private, assurance="OR-3"), public)
    assert out["verified_level"] == "OR-2" and any("equivocation" in w for w in out["warnings"])


def test_or4_or5_need_registry(keys):
    private, public = keys
    p = payload()
    p["predicates"]["witness"] = witness()
    r = emit_receipt(p, private, assurance="OR-5")
    assert verify_receipt(r, public)["verified_level"] == "OR-3"
    reg = {"did:web:example.org": {"assessor_id": "did:web:assessor.example"}}
    assert verify_receipt(r, public, registry=reg)["verified_level"] == "OR-4"
    reg["did:web:example.org"]["public_interest_review_ref"] = "pirp:2026-09"
    assert verify_receipt(r, public, registry=reg)["verified_level"] == "OR-5"
    # an issuer assessing itself is not independent
    assert verify_receipt(r, public, registry={"did:web:example.org": {"assessor_id": "did:web:example.org", "public_interest_review_ref": "x"}})["verified_level"] == "OR-3"


def test_privacy_guards(keys):
    private, public = keys
    p = payload()
    p["predicates"]["identity"]["principal_ref"] = "alice@example.com"
    assert not verify_receipt(emit_receipt(p, private), public)["valid"]
    p = payload()
    p["predicates"]["identity"]["principal_ref"] = "203.0.113.9"
    assert not verify_receipt(emit_receipt(p, private), public)["valid"]
    p = payload()
    c, secret = commit("the prompt", scheme="salted-sha256")
    p["predicates"]["runtime"]["input_commitment"] = c
    r = emit_receipt(p, private)
    assert verify_receipt(r, public)["valid"]
    assert open_commitment(c, "the prompt", secret) and not open_commitment(c, "another prompt", secret)
    r["predicates"]["runtime"]["input_commitment"]["scheme"] = "plain-sha256"
    assert not verify_receipt(r, public)["valid"]


def test_canonical_rejects_floats():
    with pytest.raises(ValueError):
        canonical_bytes({"a": 1.5})
    assert canonical_bytes({"b": 1, "a": [True, None, "é"]}) == b'{"a":[true,null,"\xc3\xa9"],"b":1}'


def test_time_order(keys):
    private, public = keys
    p = payload(started_at="2026-09-14T12:00:05Z", ended_at="2026-09-14T12:00:00Z")
    assert not verify_receipt(emit_receipt(p, private), public)["valid"]


def test_graph_three_hops(keys):
    private, public = keys
    kid = "did:web:example.org#receipt-1"
    root = emit_receipt(payload(), private, transaction_type="inference", sequence=0)
    tx, rid = root["transaction_id"], root["receipt_id"]
    tool = emit_receipt(payload(), private, transaction_type="tool-call", parent_receipt_ids=[rid], root_receipt_id=rid, transaction_id=tx, sequence=1)
    out = emit_receipt(payload(), private, transaction_type="output-delivery", parent_receipt_ids=[tool["receipt_id"]], root_receipt_id=rid, transaction_id=tx, sequence=2)
    g = verify_graph([root, tool, out], {kid: public})
    assert g["valid"] and g["weakest_verified_level"] == "OR-1" and not g["graph_errors"]
    # a missing parent breaks the graph
    g = verify_graph([root, out], {kid: public})
    assert not g["valid"] and any("missing parent" in e for e in g["graph_errors"])
    # a non-root claiming to be root breaks the receipt
    bad = copy.deepcopy(tool)
    bad["parent_receipt_ids"] = []
    assert not verify_receipt(bad, public)["valid"]


def test_levels_order():
    assert LEVELS == ["OR-0", "OR-1", "OR-2", "OR-3", "OR-4", "OR-5"]


def test_examples_verify():
    public = (ROOT / "examples" / "public-key.pem").read_bytes()
    for name in ["minimal-receipt.json", "chat-air-canada-or1.json"]:
        r = json.loads((ROOT / "examples" / name).read_text())
        assert verify_receipt(r, public)["valid"], name


def test_vectors_pass():
    from one_receipt.vectors import run_vectors

    report = run_vectors(ROOT / "testkit" / "vectors")
    assert report["total"] >= 8 and report["failed"] == 0, json.dumps(report, indent=1)
