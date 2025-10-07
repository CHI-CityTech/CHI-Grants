# Grant Labels Configuration

This document defines the label structure for grant management in the CHI-Grants repository.

## Label Categories

### Status Labels
These track the current state of a grant proposal:

- `grant-proposal` 🟦 **#0366d6** - New grant proposal submission
- `under-review` 🟨 **#fbca04** - Currently being reviewed
- `needs-revision` 🟧 **#d93f0b** - Requires modifications before approval
- `approved` 🟩 **#0e8a16** - Approved for funding
- `active-grant` 🟩 **#2da44e** - Currently active project
- `completed` ⬜ **#d4c5f9** - Grant finished
- `on-hold` 🟨 **#fbca04** - Temporarily paused
- `not-approved` 🟥 **#d73a4a** - Declined

### Priority Labels
Indicate urgency level:

- `priority:high` 🟥 **#b60205** - Urgent attention needed
- `priority:medium` 🟨 **#fbca04** - Normal priority
- `priority:low` 🟦 **#0e8a16** - Low priority

### Type Labels
Categorize the type of item:

- `deliverable` 📦 **#5319e7** - Grant deliverable item
- `milestone` 🎯 **#1d76db** - Major milestone
- `report` 📊 **#fbca04** - Reporting requirement
- `admin` ⚙️ **#d4c5f9** - Administrative task
- `question` ❓ **#d876e3** - Question or clarification needed

### Category Labels
Grant category classification:

- `research` 🔬 **#006b75** - Research-related
- `development` 💻 **#0075ca** - Development work
- `documentation` 📝 **#0e8a16** - Documentation task
- `outreach` 📢 **#d93f0b** - Outreach activity
- `education` 🎓 **#fef2c0** - Educational initiative
- `collaborative` 🤝 **#bfdadc** - Multi-institutional project

### Size/Effort Labels
Estimate effort required:

- `size:small` 🔵 **#c5def5** - Small effort (< 1 week)
- `size:medium` 🟡 **#fef2c0** - Medium effort (1-4 weeks)
- `size:large` 🔴 **#f9d0c4** - Large effort (> 1 month)

## Automation Triggers

Labels that trigger automated workflows:

### `grant-proposal`
- Adds issue to Grant Tracking Project Board
- Posts welcome comment with next steps
- Assigns to "Submitted" column

### `under-review`
- Moves card to "Under Review" column
- Assigns reviewers (if configured)
- Sets review due date

### `approved`
- Moves to "Approved" column
- Triggers repository creation process
- Sends approval notification
- Comments with next steps

### `active-grant`
- Moves to "Active" column
- Creates project board for grant
- Sets up deliverable tracking

### `completed`
- Moves to "Completed" column
- Archives related project boards
- Generates final report template

## Creating Labels

### Using GitHub Web Interface
1. Go to Issues → Labels
2. Click "New label"
3. Enter name, description, and color
4. Click "Create label"

### Using GitHub CLI
```bash
# Status labels
gh label create "grant-proposal" --color "0366d6" --description "New grant proposal submission"
gh label create "under-review" --color "fbca04" --description "Currently being reviewed"
gh label create "needs-revision" --color "d93f0b" --description "Requires modifications"
gh label create "approved" --color "0e8a16" --description "Approved for funding"
gh label create "active-grant" --color "2da44e" --description "Currently active project"
gh label create "completed" --color "d4c5f9" --description "Grant finished"
gh label create "on-hold" --color "fbca04" --description "Temporarily paused"
gh label create "not-approved" --color "d73a4a" --description "Declined"

# Priority labels
gh label create "priority:high" --color "b60205" --description "Urgent attention needed"
gh label create "priority:medium" --color "fbca04" --description "Normal priority"
gh label create "priority:low" --color "0e8a16" --description "Low priority"

# Type labels
gh label create "deliverable" --color "5319e7" --description "Grant deliverable item"
gh label create "milestone" --color "1d76db" --description "Major milestone"
gh label create "report" --color "fbca04" --description "Reporting requirement"
gh label create "admin" --color "d4c5f9" --description "Administrative task"
gh label create "question" --color "d876e3" --description "Question or clarification"

# Category labels
gh label create "research" --color "006b75" --description "Research-related"
gh label create "development" --color "0075ca" --description "Development work"
gh label create "documentation" --color "0e8a16" --description "Documentation task"
gh label create "outreach" --color "d93f0b" --description "Outreach activity"
gh label create "education" --color "fef2c0" --description "Educational initiative"
gh label create "collaborative" --color "bfdadc" --description "Multi-institutional"

# Size labels
gh label create "size:small" --color "c5def5" --description "< 1 week effort"
gh label create "size:medium" --color "fef2c0" --description "1-4 weeks effort"
gh label create "size:large" --color "f9d0c4" --description "> 1 month effort"
```

### Using API Script
Create a file `setup-labels.sh`:

```bash
#!/bin/bash

REPO="CHI-CityTech/CHI-Grants"

# Function to create label
create_label() {
    local name=$1
    local color=$2
    local description=$3
    
    curl -X POST \
        -H "Accept: application/vnd.github+json" \
        -H "Authorization: Bearer $GITHUB_TOKEN" \
        https://api.github.com/repos/$REPO/labels \
        -d "{\"name\":\"$name\",\"color\":\"$color\",\"description\":\"$description\"}"
}

# Create all labels
create_label "grant-proposal" "0366d6" "New grant proposal submission"
# ... (repeat for all labels)
```

## Label Usage Guidelines

### For Submitters
- Issues start with `grant-proposal`
- Add category labels (research, development, etc.)
- Add priority if urgent

### For Reviewers
- Add `under-review` when starting review
- Add `needs-revision` with specific feedback
- Add `approved` when ready

### For Administrators
- Add `active-grant` when repository created
- Update status labels as needed
- Add `completed` when finished

## Label Workflows

### New Proposal Flow
1. `grant-proposal` (automatic)
2. `under-review` (reviewer adds)
3. Either:
   - `needs-revision` → back to review
   - `approved` → `active-grant`
4. `completed` (when done)

### Priority Escalation
- Start: `priority:low`
- If deadlines approach: `priority:medium`
- If urgent: `priority:high`

## Best Practices

1. **Be Consistent** - Use labels consistently across all issues
2. **Update Regularly** - Keep labels current as status changes
3. **Use Multiple Labels** - Combine status, priority, and category
4. **Document Changes** - Comment when changing important labels
5. **Clean Up** - Remove outdated labels

## Custom Labels

Teams can add custom labels for specific needs:
- Funding source labels (NSF, NIH, etc.)
- Partner organization labels
- Technology stack labels
- Geographic region labels

Always use consistent naming and color schemes.
