# One Receipt: notes for Claude

A draft specification (v0.2-draft, incubation, not a standard) and reference implementation for
one signed, content-free receipt per AI transaction. Public repo. Code is Apache-2.0; text is
CC BY 4.0.

## Layout

- `spec/ONE-RECEIPT-SPEC.md` and `spec/schema/`: the specification and its JSON Schemas.
- `src/`: the Python reference implementation and the `one-receipt` CLI.
- `packages/typescript/`: the TypeScript package.
- `testkit/`, `tests/`, `examples/`: the conformance vectors, tests and worked examples.

## Checks to run before a pull request

```bash
pip install -e '.[dev]'
ruff check src tests testkit
pytest -q
one-receipt vectors
one-receipt verify examples/minimal-receipt.json --public examples/public-key.pem
check-jsonschema --check-metaschema spec/schema/one-receipt-envelope.schema.json spec/schema/predicates/*.schema.json
cd packages/typescript && npm install --no-audit --no-fund && npm test
```

## Things that are easy to get wrong

- The spec, the schemas, the vectors and both implementations must agree. A change to one is a
  change to all of them, in the same pull request.
- The keys in `examples/` are demonstration keys for the vectors only. Never present them as
  usable, and never add a real key to the repo.
- Do not overclaim. A verified receipt proves who signed which claims and when. It does not prove
  an AI output was true, fair, safe or lawful, and no wording in code, docs or verifier output may
  suggest it does.
- A receipt is content-free. Never add a field that carries prompt or output content.

## Rules for an agent

- Agents propose, humans approve. Open a pull request; do not merge it, and do not push to `main`.
- Never sign, approve or rule on anything in a human's name.
- Secrets live in 1Password. Never print, paste or commit a key, token or private key.
- A check that was not run is reported as not run. Do not write "passes" from memory.
- Read `CONTRIBUTING.md` where there is one. It wins over this file where they differ.
