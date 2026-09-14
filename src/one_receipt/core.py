"""One Receipt reference signer and verifier — spec v0.2-draft.

What this module proves, and only this: that an identified issuer signed the declared
claims, bound them to identifiers and time, and supplied the evidence the claimed
assurance level requires. It never proves truth, fairness, safety, legality, accuracy,
meaningful human review, or absence of harm. The verifier says so in every result.
"""
from __future__ import annotations

import base64
import copy
import hashlib
import hmac
import json
import os
import re
import uuid
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey
from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

SPEC_VERSION = "0.2-draft"
SCHEMA_DIR = Path(__file__).parents[2] / "spec" / "schema"
ENVELOPE_SCHEMA = SCHEMA_DIR / "one-receipt-envelope.schema.json"
LEVELS = ["OR-0", "OR-1", "OR-2", "OR-3", "OR-4", "OR-5"]

# The four predicates a verifier expects on every consequential event. A missing critical
# predicate must be declared in the manifest with an omission_reason, and caps the level
# a verifier will substantiate at OR-1: signed, but not complete.
CRITICAL = {"transaction", "policy", "runtime", "contestability"}
PREDICATE_VERSIONS = {
    "transaction": "1.0",
    "identity": "1.0",
    "mandate": "1.0",
    "policy": "1.0",
    "runtime": "1.0",
    "provenance-disclosure": "1.0",
    "witness": "1.0",
    "contestability": "1.0",
    "legal-evidence": "1.0",
    "community-authority": "1.0",
}
LIMITATIONS = [
    "Integrity verification proves that the issuer signed these claims; it does not prove truth, fairness, safety, legality, accuracy, or absence of harm.",
    "Commitments are content-free; a verifier cannot recover prompts, outputs, weights or personal data from this receipt.",
    "Assurance above OR-2 depends on an independent log and witnesses; the verified level is what the verifier could substantiate, not what the issuer claimed.",
]
_PERSONAL = re.compile(r"(@|\b\d{1,3}(\.\d{1,3}){3}\b|\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b)", re.IGNORECASE)


# --------------------------------------------------------------------------- canonical form
def canonical_bytes(value: object) -> bytes:
    """Deterministic JSON (sorted keys, no whitespace, UTF-8). The draft profile rejects
    floating-point values so every implementation serialises identical bytes; a full
    RFC 8785 canonicalizer is a v0.3 gate."""

    def reject_floats(v: Any) -> Any:
        if isinstance(v, float):
            raise ValueError("Draft canonical profile rejects floating-point values")
        if isinstance(v, dict):
            if any(not isinstance(k, str) for k in v):
                raise ValueError("Object keys must be strings")
            return {k: reject_floats(x) for k, x in v.items()}
        if isinstance(v, list):
            return [reject_floats(x) for x in v]
        return v

    return json.dumps(reject_floats(value), ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()


def _b64u(raw: bytes) -> str:
    return base64.urlsafe_b64encode(raw).decode().rstrip("=")


def _unb64u(text: str) -> bytes:
    return base64.urlsafe_b64decode(text + "=" * ((4 - len(text) % 4) % 4))


def _now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")


def new_urn(kind: str = "r") -> str:
    return f"urn:one-receipt:{kind}:{uuid.uuid4()}"


# --------------------------------------------------------------------------- keys & commitments
def generate_keypair() -> tuple[bytes, bytes]:
    private = Ed25519PrivateKey.generate()
    return (
        private.private_bytes(serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8, serialization.NoEncryption()),
        private.public_key().public_bytes(serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo),
    )


def commit(content: bytes | str, salt: bytes | None = None, *, scheme: str = "salted-sha256", key: bytes | None = None) -> tuple[dict, bytes]:
    """Return (commitment, secret). The secret (salt or HMAC key) never enters the receipt;
    whoever may later open the commitment receives it out of band. A plain hash of
    guessable content is not a commitment and is not offered here."""
    data = content.encode() if isinstance(content, str) else content
    if scheme == "salted-sha256":
        salt = salt or os.urandom(32)
        digest = hashlib.sha256(salt + data).digest()
        return {"scheme": scheme, "value": _b64u(digest)}, salt
    if scheme == "hmac-sha256":
        key = key or os.urandom(32)
        digest = hmac.new(key, data, hashlib.sha256).digest()
        return {"scheme": scheme, "value": _b64u(digest)}, key
    raise ValueError(f"unsupported commitment scheme {scheme}")


def open_commitment(commitment: dict, content: bytes | str, secret: bytes) -> bool:
    data = content.encode() if isinstance(content, str) else content
    if commitment["scheme"] == "salted-sha256":
        return hmac.compare_digest(_unb64u(commitment["value"]), hashlib.sha256(secret + data).digest())
    if commitment["scheme"] == "hmac-sha256":
        return hmac.compare_digest(_unb64u(commitment["value"]), hmac.new(secret, data, hashlib.sha256).digest())
    return False


# --------------------------------------------------------------------------- emit
def build_manifest(predicates: dict, omissions: dict[str, str] | None = None) -> list[dict]:
    omissions = omissions or {}
    manifest = []
    for name in sorted(set(predicates) | CRITICAL | set(omissions)):
        entry = {"type": name, "version": PREDICATE_VERSIONS.get(name, "1.0"), "critical": name in CRITICAL}
        if name not in predicates:
            entry["omission_reason"] = omissions.get(name, "not-collected")
        manifest.append(entry)
    return manifest


def emit_receipt(
    payload: dict,
    private_pem: bytes,
    *,
    issuer_id: str = "did:web:example.org",
    key_id: str = "did:web:example.org#receipt-1",
    role: str | None = None,
    assurance: str = "OR-1",
    transaction_type: str | None = None,
    boundary: str | None = None,
    parent_receipt_ids: list[str] | None = None,
    root_receipt_id: str | None = None,
    transaction_id: str | None = None,
    event_id: str | None = None,
    sequence: int | None = None,
    clock_source: str = "issuer",
    privacy_profile: dict | None = None,
    extensions: dict | None = None,
    extra_limitations: list[str] | None = None,
) -> dict:
    """Build and sign one envelope. `payload` carries `predicates` and may carry any of the
    graph fields; keyword arguments override the payload."""
    predicates = copy.deepcopy(payload.get("predicates", {}))
    receipt_id = new_urn("r")
    parents = parent_receipt_ids if parent_receipt_ids is not None else payload.get("parent_receipt_ids", [])
    root = root_receipt_id or payload.get("root_receipt_id") or (receipt_id if not parents else None)
    if root is None:
        raise ValueError("a receipt with parents must name its root_receipt_id")
    started = payload.get("started_at") or _now()
    ended = payload.get("ended_at") or started
    receipt = {
        "spec_version": SPEC_VERSION,
        "receipt_id": receipt_id,
        "transaction_id": transaction_id or payload.get("transaction_id") or new_urn("t"),
        "event_id": event_id or payload.get("event_id") or new_urn("e"),
        "parent_receipt_ids": list(parents),
        "root_receipt_id": root,
        "transaction_type": transaction_type or payload.get("transaction_type", "inference"),
        "sequence": sequence if sequence is not None else int(payload.get("sequence", 0)),
        "boundary": boundary or payload.get("boundary", "request-response"),
        "started_at": started,
        "ended_at": ended,
        "issued_at": _now(),
        "clock_source": clock_source,
        "issuer": {"id": issuer_id, "key_id": key_id, "role": role or payload.get("issuer_role", "operator")},
        "assurance_level": assurance,
        "privacy_profile": privacy_profile
        or payload.get("privacy_profile")
        or {"profile": "content-free", "commitment_scheme": "salted-sha256", "linkability_scope": "transaction", "metadata_minimization": True},
        "predicate_manifest": build_manifest(predicates, payload.get("omissions")),
        "predicates": predicates,
        "limitations": LIMITATIONS + list(extra_limitations or payload.get("limitations", [])),
        "signature": {"algorithm": "Ed25519", "canonicalization": "JCS", "key_id": key_id, "value": ""},
    }
    if extensions or payload.get("extensions"):
        receipt["extensions"] = extensions or payload["extensions"]
    if assurance == "OR-0":
        receipt["signature"]["value"] = "unsigned"
        return receipt
    return sign(receipt, private_pem)


def sign(receipt: dict, private_pem: bytes) -> dict:
    unsigned = copy.deepcopy(receipt)
    unsigned["signature"]["value"] = ""
    unsigned["signature"].pop("countersignatures", None)
    key = serialization.load_pem_private_key(private_pem, password=None)
    receipt["signature"]["value"] = _b64u(key.sign(canonical_bytes(unsigned)))
    return receipt


# --------------------------------------------------------------------------- verify
_registry_cache: Registry | None = None


def _validator(schema_path: Path | None) -> Draft202012Validator:
    global _registry_cache
    schema_path = schema_path or ENVELOPE_SCHEMA
    if _registry_cache is None:
        resources = []
        for p in (schema_path.parent / "predicates").glob("*.schema.json"):
            doc = json.loads(p.read_text())
            resources.append((doc["$id"], Resource.from_contents(doc)))
        _registry_cache = Registry().with_resources(resources)
    schema = json.loads(schema_path.read_text())
    return Draft202012Validator(schema, format_checker=FormatChecker(), registry=_registry_cache)


def _level_index(level: str) -> int:
    return LEVELS.index(level)


def _walk_commitments(node: Any):
    if isinstance(node, dict):
        if set(node) >= {"scheme", "value"} and node.get("scheme") in {"salted-sha256", "hmac-sha256", "pedersen", "plain-sha256", "sha256"}:
            yield node
        for v in node.values():
            yield from _walk_commitments(v)
    elif isinstance(node, list):
        for v in node:
            yield from _walk_commitments(v)


def verify_receipt(receipt: dict, public_pem: bytes | None = None, schema_path: Path | None = None, registry: dict | None = None) -> dict:
    """Verify one envelope. Returns a result with the level the verifier could substantiate
    (`verified_level`) next to the level the issuer claimed (`claimed_level`). `registry`
    optionally maps issuer ids to independent-assessment and public-interest-review facts
    for OR-4 and OR-5; without it those levels are reported as unverifiable, never as met."""
    checks: dict[str, Any] = {}
    errors: list[str] = []
    warnings: list[str] = []
    limitations = receipt.get("limitations", []) if isinstance(receipt, dict) else []

    schema_errors = sorted(_validator(schema_path).iter_errors(receipt), key=lambda e: list(e.path))
    checks["schema"] = not schema_errors
    if schema_errors:
        errors += [f"schema: {'/'.join(str(p) for p in e.path) or '$'}: {e.message}" for e in schema_errors]
        return {"valid": False, "claimed_level": receipt.get("assurance_level") if isinstance(receipt, dict) else None, "verified_level": None, "checks": checks, "errors": errors, "warnings": warnings, "limitations": limitations}

    claimed = receipt["assurance_level"]
    ceiling = _level_index(claimed)

    # --- signature
    if receipt["signature"]["value"] == "unsigned":
        checks["signature"] = None
        if claimed != "OR-0":
            errors.append("signature: unsigned envelope may only claim OR-0")
        ceiling = min(ceiling, 0)
    elif public_pem is None:
        checks["signature"] = None
        warnings.append("signature: no public key supplied; treated as OR-0 unverified export")
        ceiling = min(ceiling, 0)
    else:
        try:
            unsigned = copy.deepcopy(receipt)
            unsigned["signature"]["value"] = ""
            unsigned["signature"].pop("countersignatures", None)
            key = serialization.load_pem_public_key(public_pem)
            if not isinstance(key, Ed25519PublicKey):
                raise ValueError("reference verifier supports Ed25519 keys only")
            key.verify(_unb64u(receipt["signature"]["value"]), canonical_bytes(unsigned))
            checks["signature"] = True
        except Exception as exc:  # every failure is a verification failure
            checks["signature"] = False
            errors.append(f"signature: {type(exc).__name__}")

    # --- manifest ↔ predicates
    manifest = {m["type"]: m for m in receipt["predicate_manifest"]}
    predicates = receipt["predicates"]
    manifest_ok = True
    for name in predicates:
        if name not in manifest:
            manifest_ok = False
            errors.append(f"manifest: predicate {name} present but not declared")
    for name, entry in manifest.items():
        if name not in predicates and "omission_reason" not in entry:
            manifest_ok = False
            errors.append(f"manifest: {name} declared, absent, and no omission_reason given")
    critical_omitted = [n for n in CRITICAL if n not in predicates]
    for n in critical_omitted:
        if n not in manifest:
            manifest_ok = False
            errors.append(f"manifest: critical predicate {n} neither present nor declared omitted")
    checks["manifest"] = manifest_ok
    if critical_omitted and manifest_ok:
        warnings.append(f"critical predicates omitted ({', '.join(sorted(critical_omitted))}); verified level capped at OR-1")
        ceiling = min(ceiling, 1)
    checks["critical_complete"] = not critical_omitted

    # --- graph and time
    graph_ok = True
    if not receipt.get("parent_receipt_ids") and receipt["root_receipt_id"] != receipt["receipt_id"]:
        graph_ok = False
        errors.append("graph: a receipt without parents must be its own root")
    if receipt["receipt_id"] in receipt.get("parent_receipt_ids", []):
        graph_ok = False
        errors.append("graph: a receipt cannot be its own parent")
    try:
        s, e, i = (datetime.fromisoformat(receipt[k].replace("Z", "+00:00")) for k in ("started_at", "ended_at", "issued_at"))
        if not (s <= e <= i):
            graph_ok = False
            errors.append("time: started_at <= ended_at <= issued_at must hold")
    except ValueError:
        graph_ok = False
        errors.append("time: unparseable timestamp")
    checks["graph"] = graph_ok

    # --- privacy
    privacy_ok = True
    for c in _walk_commitments(predicates):
        if c["scheme"] not in {"salted-sha256", "hmac-sha256", "pedersen"}:
            privacy_ok = False
            errors.append(f"privacy: plain hash commitment ({c['scheme']}) is forbidden")
    principal_ref = predicates.get("identity", {}).get("principal_ref", "")
    if principal_ref and _PERSONAL.search(principal_ref):
        privacy_ok = False
        errors.append("privacy: identity.principal_ref looks like a stable personal identifier")
    if receipt["privacy_profile"]["commitment_scheme"] == "none" and any(True for _ in _walk_commitments(predicates)):
        privacy_ok = False
        errors.append("privacy: commitments present but privacy_profile.commitment_scheme is none")
    checks["privacy"] = privacy_ok

    # --- assurance ladder
    witness = predicates.get("witness")
    issuer_id = receipt["issuer"]["id"]
    if ceiling >= 2 and (not witness or "inclusion_proof" not in witness):
        warnings.append("OR-2 needs a log inclusion proof; capped at OR-1")
        ceiling = min(ceiling, 1)
    if ceiling >= 3 and witness:
        independent = witness["log_operator"]["id"] != issuer_id
        witnessed = bool(witness.get("witnesses"))
        if not independent:
            warnings.append("OR-3 needs a log operator that is not the issuer; capped at OR-2")
            ceiling = min(ceiling, 2)
        elif not witnessed:
            warnings.append("OR-3 needs at least one independent witness; capped at OR-2")
            ceiling = min(ceiling, 2)
        if witness.get("equivocation_status") in {"suspected", "confirmed"}:
            warnings.append(f"log equivocation {witness['equivocation_status']}: assurance frozen at OR-2 pending an incident receipt")
            ceiling = min(ceiling, 2)
    checks["witness"] = witness.get("equivocation_status") == "not-observed" if witness else None
    if ceiling >= 4:
        facts = (registry or {}).get(issuer_id, {})
        if not facts.get("assessor_id") or facts.get("assessor_id") == issuer_id:
            warnings.append("OR-4 needs an independent assessment on record; not in the supplied registry, capped at OR-3")
            ceiling = min(ceiling, 3)
    if ceiling >= 5:
        facts = (registry or {}).get(issuer_id, {})
        if not facts.get("public_interest_review_ref"):
            warnings.append("OR-5 needs a public-interest review on record; not in the supplied registry, capped at OR-4")
            ceiling = min(ceiling, 4)

    # --- contestability sanity for consequential events
    contest = predicates.get("contestability")
    consequential = receipt["transaction_type"] in {"policy-decision", "output-delivery", "human-review"}
    if contest and consequential and contest["human_review"]["available"] and contest["human_review"].get("reviewer_authority") == "none":
        warnings.append("contestability: human review is offered but the reviewer has no authority")
    checks["limitations"] = len(limitations) > 0

    valid = not errors
    return {
        "valid": valid,
        "claimed_level": claimed,
        "verified_level": LEVELS[ceiling] if valid else None,
        "checks": checks,
        "errors": errors,
        "warnings": warnings,
        "limitations": limitations,
    }


def verify_graph(receipts: list[dict], keys: dict[str, bytes], registry: dict | None = None) -> dict:
    """Verify a set of receipts as one transaction graph: each receipt individually, every
    parent present, one root, and no duplicated sequence per transaction. `keys` maps
    key_id to public PEM."""
    by_id = {r["receipt_id"]: r for r in receipts}
    results = {rid: verify_receipt(r, keys.get(r["signature"]["key_id"]), registry=registry) for rid, r in by_id.items()}
    errors: list[str] = []
    roots = {r["root_receipt_id"] for r in receipts}
    if len(roots) != 1:
        errors.append(f"graph: {len(roots)} roots in one graph")
    for r in receipts:
        for p in r.get("parent_receipt_ids", []):
            if p not in by_id:
                errors.append(f"graph: {r['receipt_id']} names missing parent {p}")
    seen: dict[tuple[str, int], str] = {}
    for r in receipts:
        k = (r["transaction_id"], r["sequence"])
        if k in seen and r["issuer"]["role"] == by_id[seen[k]]["issuer"]["role"]:
            errors.append(f"graph: duplicate sequence {r['sequence']} in {r['transaction_id']}")
        seen.setdefault(k, r["receipt_id"])
    levels = [res["verified_level"] for res in results.values() if res["valid"]]
    weakest = min(levels, key=_level_index) if levels and all(levels) else None
    return {
        "valid": all(res["valid"] for res in results.values()) and not errors,
        "receipts": results,
        "graph_errors": errors,
        "weakest_verified_level": weakest,
        "limitations": LIMITATIONS,
    }
