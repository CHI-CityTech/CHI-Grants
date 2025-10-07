# Active Grant Proposals

This directory contains grant proposals that are currently being developed or are under review.

## Structure

Each grant proposal should be in its own subdirectory:

```
active/
├── grant-2024-001-ai-healthcare/
│   ├── proposal.md
│   ├── budget.xlsx
│   ├── supporting-docs/
│   │   ├── cv-pi.pdf
│   │   ├── letter-of-support.pdf
│   │   └── data-management-plan.pdf
│   └── README.md
├── grant-2024-002-mobile-clinic/
│   └── ...
```

## Naming Convention

Use the format: `grant-YYYY-NNN-short-description`

- `YYYY`: Year (e.g., 2024)
- `NNN`: Sequential number (e.g., 001, 002)
- `short-description`: Brief project identifier (e.g., ai-healthcare)

## What Goes Here

- **In Development:** Proposals being written
- **Under Review:** Proposals submitted and awaiting decision
- **Approved (Pending Setup):** Approved grants before repository creation

## What Doesn't Go Here

- **Rejected Proposals:** Archive or remove
- **Active Grants:** Move to dedicated repository after approval
- **Completed Grants:** Move to `/completed` directory

## Tips

1. Keep all related files in the grant subdirectory
2. Include a README.md in each grant folder
3. Use version control for tracking changes
4. Link the folder to your grant proposal issue
5. Remove sensitive information before committing

## Example README for Grant Folder

```markdown
# Grant 2024-001: AI-Powered Healthcare Analytics

**Status:** Under Review
**PI:** Dr. Jane Smith
**Submitted:** 2024-01-15
**Issue:** #123

## Files
- `proposal.md` - Main proposal document
- `budget.xlsx` - Detailed budget
- `supporting-docs/` - CVs, letters, etc.

## Review Status
- [ ] Initial review
- [ ] Technical review
- [ ] Budget review
- [ ] Final decision

## Next Steps
- Awaiting reviewer feedback
- Prepare presentation for committee
```
