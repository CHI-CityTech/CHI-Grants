# CHI-Grants Quick Reference

## For Grant Submitters

### 📝 Submitting a New Grant Proposal

1. **Prepare your proposal** using the [template](proposals/templates/GRANT_TEMPLATE.md)
2. **Validate locally** (optional): `./scripts/validate-proposal.sh my-proposal.md`
3. **Create an issue** using the [Grant Proposal template](../../issues/new?template=grant-proposal.md)
4. **Track progress** through the issue comments
5. **Respond to feedback** from reviewers
6. **Wait for approval** (typically 2-3 weeks)

### 📚 Key Documents
- [Grant Template](proposals/templates/GRANT_TEMPLATE.md) - Fill this out
- [Example Proposal](proposals/examples/EXAMPLE_PROPOSAL.md) - See a complete example
- [Submission Guidelines](docs/SUBMISSION_GUIDELINES.md) - Detailed instructions

## For Reviewers

### 🔍 Reviewing a Grant Proposal

1. **Find proposals** in [Issues](../../issues?q=is%3Aissue+is%3Aopen+label%3Agrant-proposal)
2. **Add label** `under-review` when you start
3. **Evaluate** using the criteria in [Submission Guidelines](docs/SUBMISSION_GUIDELINES.md)
4. **Provide feedback** as issue comments
5. **Add label**:
   - `approved` if accepted
   - `needs-revision` if changes needed
   - `not-approved` if declined

### 📊 Review Criteria (100 points)
- CHI Alignment: 25 points
- Technical Merit: 25 points
- Team Qualifications: 20 points
- Budget & Resources: 15 points
- Impact & Sustainability: 15 points

## For Administrators

### ⚙️ Setting Up a New Grant Repository

**Option 1: Manual**
```bash
./scripts/create-grant-repo.sh "Project Name" "GRANT-2024-001"
```

**Option 2: Automated**
- Add `approved` label to the grant issue
- GitHub Action will trigger and comment with next steps
- Follow the automated instructions

### 🏷️ Setting Up Labels
```bash
./scripts/setup-labels.sh
```

### 📋 Project Board Setup
See [Project Boards Documentation](docs/PROJECT_BOARDS.md)

## Common Tasks

### Validate a Proposal Locally
```bash
./scripts/validate-proposal.sh my-proposal.md
```

### Adding a Label to an Issue
```bash
gh issue edit <issue-number> --add-label "label-name"
```

### Closing a Grant Issue
```bash
gh issue close <issue-number> --comment "Grant completed successfully!"
```

### Listing All Grant Proposals
```bash
gh issue list --label "grant-proposal"
```

### Finding Active Grants
```bash
gh issue list --label "active-grant"
```

## Repository Structure Quick Map

```
CHI-Grants/
├── .github/
│   ├── workflows/          # Automation workflows
│   └── ISSUE_TEMPLATE/     # Issue templates
├── proposals/
│   ├── templates/          # Grant templates
│   ├── examples/           # Example proposals
│   ├── active/            # In-progress proposals
│   └── completed/         # Archived grants
├── scripts/               # Automation scripts
└── docs/                 # Documentation
```

## Labels Quick Reference

### Status
- `grant-proposal` - New submission
- `under-review` - Being evaluated
- `needs-revision` - Requires changes
- `approved` - Approved for funding
- `active-grant` - Currently active
- `completed` - Finished

### Priority
- `priority:high` - Urgent
- `priority:medium` - Normal
- `priority:low` - Can wait

### Category
- `research` - Research project
- `development` - Development work
- `education` - Educational initiative
- `collaborative` - Multi-institutional

## Workflows

### Grant Submission → Approval
```
Submit Issue → under-review → (needs-revision) → approved → active-grant → completed
                                      ↓
                                 not-approved
```

### Repository Creation Flow
```
approved label → GitHub Action triggers → Repository created → Team notified
```

## Quick Commands

### View Grant Proposal Template
```bash
cat proposals/templates/GRANT_TEMPLATE.md
```

### Check Workflow Status
```bash
gh run list --workflow=grant-automation.yml
```

### Create Test Proposal (Development)
```bash
gh issue create --title "[GRANT] Test Proposal" \
  --label "grant-proposal" \
  --body "Test grant proposal for development"
```

## Help & Support

- 📖 [Full Documentation](README.md)
- 🤝 [Contributing Guide](CONTRIBUTING.md)
- 💬 [Discussions](../../discussions)
- 🐛 [Report Issues](../../issues)

## Useful Links

- [CHI Ecosystem](https://github.com/CHI-CityTech)
- [Grant Tracking Board](../../projects)
- [All Grant Proposals](../../issues?q=label%3Agrant-proposal)
- [Active Grants](../../issues?q=label%3Aactive-grant)

---

💡 **Tip:** Bookmark this page for quick access to common tasks and information!
