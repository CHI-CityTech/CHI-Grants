# Project Board Configuration

This document describes how to set up and use GitHub Project Boards for grant tracking.

## Grant Tracking Board

### Board Structure
The main grant tracking board should have the following columns:

1. **📝 Submitted** - New grant proposals
2. **🔍 Under Review** - Proposals being evaluated
3. **✏️ Revisions Needed** - Proposals requiring modifications
4. **✅ Approved** - Approved grants pending repository setup
5. **🚀 Active** - Grants with active repositories
6. **✔️ Completed** - Finished grants
7. **❌ Not Approved** - Declined proposals

### Automation Rules

#### Move to "Under Review"
- **Trigger:** When issue is labeled with `under-review`
- **Action:** Move card to "Under Review" column

#### Move to "Revisions Needed"
- **Trigger:** When issue is labeled with `needs-revision`
- **Action:** Move card to "Revisions Needed" column

#### Move to "Approved"
- **Trigger:** When issue is labeled with `approved`
- **Action:** Move card to "Approved" column

#### Move to "Active"
- **Trigger:** When issue is labeled with `active-grant`
- **Action:** Move card to "Active" column

#### Move to "Completed"
- **Trigger:** When issue is closed and labeled with `completed`
- **Action:** Move card to "Completed" column

## Individual Grant Project Boards

For each approved grant, create a dedicated project board with:

### Columns
1. **📋 Backlog** - Planned tasks
2. **🔜 Next Up** - Prioritized next tasks
3. **🏃 In Progress** - Currently active tasks
4. **👀 Review** - Tasks awaiting review
5. **✅ Done** - Completed tasks

### Custom Fields
- **Priority:** High, Medium, Low
- **Deliverable:** Link to grant deliverable
- **Due Date:** Target completion date
- **Assignee:** Team member responsible
- **Status:** Not Started, In Progress, Blocked, Complete

## Setting Up a New Grant Board

### Manual Setup
1. Go to organization Projects
2. Click "New Project"
3. Select "Board" template
4. Name it: `[Grant ID] - [Project Name]`
5. Add columns as specified above
6. Configure automation rules

### Using GitHub CLI
```bash
# Create new project board
gh project create "[Grant ID] - [Project Name]" --owner CHI-CityTech

# Add columns (requires project ID from above)
gh project field-create [PROJECT_ID] --name "Priority" --data-type "SINGLE_SELECT" --single-select-options "High,Medium,Low"
```

### Using API/Automation
The grant automation workflow can automatically create and configure project boards when a grant is approved.

## Board Views

### Default View (Board)
Shows cards in columns for visual workflow management.

### Table View
Useful for:
- Budget tracking
- Timeline management
- Deliverable status overview

Configure with fields:
- Task name
- Assignee
- Status
- Due date
- Priority
- Deliverable link

### Roadmap View
Timeline-based view for:
- Milestone tracking
- Phase planning
- Deadline visualization

## Labels for Grant Management

### Status Labels
- `grant-proposal` - New submission
- `under-review` - Being evaluated
- `needs-revision` - Requires changes
- `approved` - Approved for funding
- `active-grant` - Currently active
- `completed` - Grant finished
- `on-hold` - Temporarily paused

### Priority Labels
- `priority:high` - Urgent attention needed
- `priority:medium` - Normal priority
- `priority:low` - Can wait

### Type Labels
- `deliverable` - Grant deliverable
- `milestone` - Major milestone
- `report` - Reporting requirement
- `admin` - Administrative task

### Category Labels
- `research` - Research-related
- `development` - Development work
- `documentation` - Documentation task
- `outreach` - Outreach activity

## Best Practices

### 1. Regular Updates
- Update board weekly
- Move cards promptly
- Keep descriptions current

### 2. Clear Communication
- Comment on cards for updates
- Tag relevant team members
- Link related issues/PRs

### 3. Milestone Tracking
- Create milestone issues
- Link to deliverables
- Set clear due dates

### 4. Reporting
- Use board for quarterly reports
- Export data as needed
- Archive completed items

### 5. Integration
- Link commits to issues
- Reference issues in PRs
- Close issues when complete

## Templates

### New Deliverable Issue
```markdown
---
name: Grant Deliverable
about: Track a grant deliverable
title: '[DELIVERABLE] '
labels: deliverable
---

## Deliverable Info
- **Grant:** [Grant ID]
- **Name:** [Deliverable name]
- **Due:** [Date]

## Requirements
- [ ] Requirement 1
- [ ] Requirement 2

## Status
Current progress...
```

## Automation Examples

### Auto-assign to Board
```yaml
name: Add to Project
on:
  issues:
    types: [labeled]

jobs:
  add-to-project:
    if: contains(github.event.issue.labels.*.name, 'grant-proposal')
    runs-on: ubuntu-latest
    steps:
      - uses: actions/add-to-project@v0.5.0
        with:
          project-url: https://github.com/orgs/CHI-CityTech/projects/1
```

### Move on Label
```yaml
name: Move Card
on:
  issues:
    types: [labeled]

jobs:
  move-card:
    runs-on: ubuntu-latest
    steps:
      - name: Move to Under Review
        if: contains(github.event.issue.labels.*.name, 'under-review')
        uses: alex-page/github-project-automation-plus@v0.8.1
        with:
          project: Grant Tracking
          column: Under Review
```

## Reporting from Boards

### Weekly Summary
Generate weekly summaries showing:
- New proposals submitted
- Proposals under review
- Approvals granted
- Active grant status

### Monthly Metrics
Track:
- Proposal success rate
- Average review time
- Active grant count
- Completion rate

### Quarterly Reports
Include:
- Total grants managed
- Funding awarded
- Deliverables completed
- Impact metrics
