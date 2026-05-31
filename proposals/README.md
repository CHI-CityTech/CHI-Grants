# Proposals

This folder holds CHI's authored grant proposals — the working documents for each submission.

A proposal folder is created when CHI commits to responding to a solicitation. All narrative drafts, budget documents, biosketches, and submission materials live here.

## Folder Naming Convention

```
YYYY-sponsor-short-title/
```

Use the same name as the corresponding `solicitations/` folder so the two are trivially linked.

Examples:
- `2026-nsf-smart-health/`
- `2026-neh-digital-humanities/`

## Recommended Folder Contents

```
YYYY-sponsor-short-title/
├── README.md           # Status, deadline, owner, links to solicitation + CHIIDS record
├── proposal.md         # Main narrative draft
├── budget.md           # Budget breakdown and notes
├── timeline.md         # Submission milestones and internal deadlines
├── biosketches/        # PI and co-PI biographical sketches
│   └── smith-biosketch.md
└── attachments/        # Sponsor-required supporting documents
    └── facilities.md
```

## README.md Front Matter (required)

Each proposal README should include at minimum:

```markdown
# Proposal: [Short Title]

- **Solicitation:** [link to solicitations/YYYY-sponsor-short-title/]
- **Sponsor:** [Agency name]
- **Deadline:** [YYYY-MM-DD]
- **Owner:** [CHI faculty or staff lead]
- **Status:** [drafting | under_review | submitted | awarded | rejected]
- **CHIIDS Record:** [link to META-CHIIDS proposal record when created]
- **Related Meta-Projects:** [e.g., BBS, BRPS]
```

## Status Values

- `drafting` — narrative in progress
- `under_review` — internal or sponsor review
- `submitted` — submitted to sponsor
- `awarded` — funded; see `awards/` for post-award record
- `rejected` — not funded

## After Submission

If funded, create a matching folder in `awards/` and update the status here to `awarded` with a link.
