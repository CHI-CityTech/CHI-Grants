# Solicitations

This folder holds external funding opportunities that CHI is tracking or considering.

A solicitation is a funding call issued by a sponsor. It belongs here before CHI decides to respond. Once CHI commits to submitting a proposal, the working proposal documents move to `proposals/`.

## Folder Naming Convention

```
YYYY-sponsor-short-title/
```

Examples:
- `2026-nsf-smart-health/`
- `2026-neh-digital-humanities/`
- `2027-mellon-performing-arts/`

## Minimum Contents Per Solicitation

```
YYYY-sponsor-short-title/
├── README.md        # Status, deadline, sponsor contact, CHI point of contact
├── solicitation.md  # Key requirements, eligibility, scope notes
└── links.md         # URL to official call, related resources
```

If a PDF of the official call is available, include it as `solicitation.pdf` alongside `solicitation.md`.

## Status Values (use in README.md front matter or header)

- `tracking` — monitoring; no commitment yet
- `evaluating` — active internal discussion
- `pursuing` — CHI has committed to submit
- `passed` — decided not to pursue
- `expired` — deadline passed without submission

## Relationship to Proposals

When a solicitation moves to `pursuing`, create a matching folder in `proposals/` and link the two in each README.
