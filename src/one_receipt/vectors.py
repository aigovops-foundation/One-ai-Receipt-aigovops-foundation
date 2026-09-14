"""Test-vector runner. Each vector is a JSON file with `receipt`, `public_key` (PEM text or
null), optional `registry`, and `expect` = {valid, verified_level}. Any implementation that
produces the same verdicts on every vector is interoperable at the syntax layer."""
from __future__ import annotations

import json
from pathlib import Path

from .core import verify_receipt


def run_vectors(directory: Path) -> dict:
    results = []
    for path in sorted(directory.glob("*.json")):
        vec = json.loads(path.read_text())
        key = vec.get("public_key")
        out = verify_receipt(vec["receipt"], key.encode() if key else None, registry=vec.get("registry"))
        expect = vec["expect"]
        ok = out["valid"] == expect["valid"] and out["verified_level"] == expect.get("verified_level")
        results.append({"vector": path.name, "case": vec.get("case"), "pass": ok, "got": {"valid": out["valid"], "verified_level": out["verified_level"]}, "expect": expect, "errors": out["errors"], "warnings": out["warnings"]})
    return {"total": len(results), "failed": sum(1 for r in results if not r["pass"]), "results": results}
