# Requirements catalogue

`requirements.csv` holds exactly 360 traceable requirements — eighteen domains, twenty each — with id, domain, requirement, priority, acceptance evidence, owner and status. CI fails if the count, the domain split or the id uniqueness changes.

| Domain | Where it is satisfied in this repository |
|---|---|
| STR strategy · GOV governance · PAR partners · PMO program | `docs/MASTER-PLAN.md`, `governance/` |
| PRD product | `docs/MASTER-PLAN.md` §7, `docs/FRAMEWORK.md` |
| ARC architecture · IDM identity/mandate · POL policy · RUN runtime · LOG log/witness · PRI privacy · SEC security · CON contestability | `spec/ONE-RECEIPT-SPEC.md`, `spec/schema/`, `docs/ARCHITECTURE.md` |
| SDK · TST testing · DEV development | `src/`, `packages/typescript/`, `testkit/`, `.github/workflows/ci.yml`, `governance/RELEASE-GATES.md` |
| PRO procurement · MKT marketing/education | `governance/COALITION-PLAYBOOK.md` (group 4), `docs/PRACTITIONER-PROGRAM.md` |

Statuses move from `proposed` to `accepted`/`implemented` by pull request with the evidence linked; owners are assigned when the charter's bodies are seated (gate G2).
