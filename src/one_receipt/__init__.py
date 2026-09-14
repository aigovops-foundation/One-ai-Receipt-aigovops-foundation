"""One Receipt reference implementation — spec v0.2-draft (AiGovOps Foundation, incubation)."""
from .core import SPEC_VERSION, commit, emit_receipt, generate_keypair, open_commitment, verify_graph, verify_receipt

__all__ = ["SPEC_VERSION", "commit", "emit_receipt", "generate_keypair", "open_commitment", "verify_graph", "verify_receipt"]
__version__ = "0.2.0"
