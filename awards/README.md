# Awards

This folder holds post-award administrative records for funded grants.

A folder is created here only when a proposal in `proposals/` is confirmed funded. The working proposal documents remain in `proposals/`. This folder contains award-specific administration: the award letter, reporting obligations, budget actuals, and compliance records.

## Folder Naming Convention

```
YYYY-sponsor-short-title/
```

Use the same name as the corresponding `proposals/` folder.

## Recommended Folder Contents

```
YYYY-sponsor-short-title/
├── README.md              # Award summary, reporting schedule, contacts
├── award-letter.md        # Key terms from the award notice (or link to PDF)
├── budget-actuals.md      # Tracking against awarded budget
├── reporting/             # Progress and final reports
│   ├── progress-report-1.md
│   └── final-report.md
└── compliance/            # IRB, export control, or sponsor-specific requirements
```

## README.md Front Matter (required)

```markdown
# Award: [Short Title]

- **Proposal:** [link to proposals/YYYY-sponsor-short-title/]
- **Sponsor:** [Agency name]
- **Award Amount:** $[amount]
- **Award Date:** [YYYY-MM-DD]
- **Project Period:** [YYYY-MM-DD] to [YYYY-MM-DD]
- **PI:** [Name]
- **Status:** [active | no-cost-extension | closed]
- **CHIIDS Record:** [link to META-CHIIDS project record]
```
