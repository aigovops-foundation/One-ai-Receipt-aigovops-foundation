"""one-receipt command line: keygen · emit · verify · graph · commit · vectors."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .core import commit, emit_receipt, generate_keypair, verify_graph, verify_receipt


def _load(path: str) -> dict:
    return json.loads(Path(path).read_text())


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="one-receipt", description="One Receipt reference tools (spec v0.2-draft)")
    sub = p.add_subparsers(dest="cmd", required=True)

    k = sub.add_parser("keygen", help="write an Ed25519 keypair (PEM)")
    k.add_argument("private")
    k.add_argument("public")

    e = sub.add_parser("emit", help="sign a payload into a receipt")
    e.add_argument("payload")
    e.add_argument("private")
    e.add_argument("--issuer", default="did:web:example.org")
    e.add_argument("--key-id", default="did:web:example.org#receipt-1")
    e.add_argument("--role", default=None)
    e.add_argument("--assurance", default="OR-1", choices=["OR-0", "OR-1", "OR-2", "OR-3", "OR-4", "OR-5"])
    e.add_argument("--type", dest="transaction_type", default=None)
    e.add_argument("--parent", action="append", default=None, help="parent receipt id (repeatable)")
    e.add_argument("--root", default=None)
    e.add_argument("--transaction", default=None)
    e.add_argument("--sequence", type=int, default=None)

    v = sub.add_parser("verify", help="verify one receipt")
    v.add_argument("receipt")
    v.add_argument("--public", default=None, help="issuer public key PEM; omit to report OR-0")
    v.add_argument("--registry", default=None, help="JSON of issuer id → assessment facts for OR-4/OR-5")

    g = sub.add_parser("graph", help="verify a transaction graph (receipts as a JSON array or NDJSON)")
    g.add_argument("receipts")
    g.add_argument("--keys", required=True, help="JSON of key_id → public key PEM path")
    g.add_argument("--registry", default=None)

    c = sub.add_parser("commit", help="compute a salted commitment to a file; prints the commitment and the salt (keep the salt out of the receipt)")
    c.add_argument("file")
    c.add_argument("--scheme", default="salted-sha256", choices=["salted-sha256", "hmac-sha256"])

    t = sub.add_parser("vectors", help="run the test vectors in testkit/vectors")
    t.add_argument("--dir", default=str(Path(__file__).parents[2] / "testkit" / "vectors"))

    a = p.parse_args(argv)

    if a.cmd == "keygen":
        private, public = generate_keypair()
        Path(a.private).write_bytes(private)
        Path(a.public).write_bytes(public)
        return 0
    if a.cmd == "emit":
        receipt = emit_receipt(
            _load(a.payload),
            Path(a.private).read_bytes(),
            issuer_id=a.issuer,
            key_id=a.key_id,
            role=a.role,
            assurance=a.assurance,
            transaction_type=a.transaction_type,
            parent_receipt_ids=a.parent,
            root_receipt_id=a.root,
            transaction_id=a.transaction,
            sequence=a.sequence,
        )
        print(json.dumps(receipt, indent=2, ensure_ascii=False))
        return 0
    if a.cmd == "verify":
        registry = _load(a.registry) if a.registry else None
        result = verify_receipt(_load(a.receipt), Path(a.public).read_bytes() if a.public else None, registry=registry)
        print(json.dumps(result, indent=2))
        return 0 if result["valid"] else 1
    if a.cmd == "graph":
        text = Path(a.receipts).read_text()
        receipts = json.loads(text) if text.lstrip().startswith("[") else [json.loads(line) for line in text.splitlines() if line.strip()]
        keys = {kid: Path(path).read_bytes() for kid, path in _load(a.keys).items()}
        result = verify_graph(receipts, keys, registry=_load(a.registry) if a.registry else None)
        print(json.dumps(result, indent=2))
        return 0 if result["valid"] else 1
    if a.cmd == "commit":
        commitment, secret = commit(Path(a.file).read_bytes(), scheme=a.scheme)
        print(json.dumps({"commitment": commitment, "secret_b64": __import__("base64").urlsafe_b64encode(secret).decode()}, indent=2))
        return 0
    if a.cmd == "vectors":
        from .vectors import run_vectors

        report = run_vectors(Path(a.dir))
        print(json.dumps(report, indent=2))
        return 0 if report["failed"] == 0 else 1
    return 2


if __name__ == "__main__":
    sys.exit(main())
