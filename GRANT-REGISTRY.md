# CHI Grant Registry

Canonical lifecycle register for all CHI grant activity. One row per grant opportunity.

**Status values:**
`tracking` → `evaluating` → `pursuing` → `submitted` → `awarded` / `rejected` / `deferred` → `closed`

Update this file whenever a grant changes stage. For full documentation, see the matching folder in `solicitations/`, `proposals/`, or `awards/`.

---

## Registry

| Grant ID | Proposal ID | CHIIDS Proposal Slug | Short Title | Sponsor | PI | Submitted | Status | Award Amount | Proposal Record | Award Record |
|:---------|:------------|:---------------------|:------------|:--------|:---|:----------|:-------|:-------------|:----------------|:-------------|
| CHI-2025-001 | CHI-PROP-2025-001 | proposal-oaa-ai-innovation-2025 | Integrated AI Ethics and Immersive Blended Learning Initiative | CUNY Office of Academic Affairs | Dr David B Smith | 2025-12-01 | awarded | $25,000 | [proposals/2025-cuny-oaa-ai-innovation/](proposals/2025-cuny-oaa-ai-innovation/) | [awards/2025-cuny-oaa-ai-innovation/](awards/2025-cuny-oaa-ai-innovation/) |
| CHI-2025-002 | CHI-PROP-2025-002 | proposal-avmi-gvsc-2025 | AVMI-GVSC Modeling and Simulation Ecosystem | US Army GVSC (via WPI subcontract) | David Smith (CUNY subrecipient PI) | 2025-10-07 | awarded | $50,000 (CUNY subcontract) | TBD (source package in award folder) | [awards/2025-avmi-gvsc-mobility-ecosystem/](awards/2025-avmi-gvsc-mobility-ecosystem/) |
| CHI-2025-003 | CHI-PROP-2025-003 | proposal-cuny-irg-bsp-cai-2025 | CUNY IRG 2025 - Blended Shadow Puppetry and Collaborative AI | CUNY Interdisciplinary Research Grant (IRG) | Dr David B Smith | 2025-10-06 | rejected | N/A | [proposals/2025-cuny-irg-bsp-cai/](proposals/2025-cuny-irg-bsp-cai/) | N/A |

---

## Lifecycle Definitions

| Status | Meaning |
|:-------|:--------|
| `tracking` | Monitoring a funding call; no internal commitment yet |
| `evaluating` | Active internal discussion about whether to pursue |
| `pursuing` | Committed to submit; proposal in development |
| `submitted` | Submitted to sponsor; awaiting decision |
| `awarded` | Funded; see `awards/` folder for post-award record |
| `rejected` | Not funded by sponsor |
| `deferred` | Submission postponed to a future cycle |
| `closed` | Award period ended; all reporting complete |

---

## Grant ID Convention

Format: `CHI-YYYY-NNN` where `YYYY` is the submission year and `NNN` is a sequential number.

Next available: `CHI-2025-004` / `CHI-2026-001`

## Proposal ID Convention

Format: `CHI-PROP-YYYY-NNN` where `YYYY` is the proposal year and `NNN` aligns with the related grant record when applicable.

Next available: `CHI-PROP-2025-004` / `CHI-PROP-2026-001`

## Reference Model

- Every grant record should have both a `Grant ID` and `Proposal ID`.
- Every grant row should link to both proposal and award records when available.
- `CHIIDS Proposal Slug` should map to the proposal record in META-CHIIDS (`proposals.slug`).

---

## Notes

- This file is the human-readable register. The authoritative machine-readable version will be the `grants` table in the CHIIDS SQLite database (migration: `database/migrations/003_add_grants.sql`).
- Each grant should also have a linked record in META-CHIIDS identifying which meta-projects it supports.
