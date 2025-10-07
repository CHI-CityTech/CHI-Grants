# Getting Started with CHI-Grants

Welcome to CHI-Grants! This guide will help you get started quickly.

## Overview

CHI-Grants is a repository for managing grant proposals within the CHI (Community Health Initiative) ecosystem. Whether you're submitting a grant proposal, reviewing proposals, or managing approved grants, this guide will help you navigate the system.

## For Grant Applicants

### Step 1: Understand the Requirements

Before submitting a grant proposal:

1. **Read the Guidelines**
   - Review [Submission Guidelines](SUBMISSION_GUIDELINES.md)
   - Check grant categories and eligibility
   - Understand the review criteria

2. **Review Examples**
   - See the [Example Proposal](../proposals/examples/EXAMPLE_PROPOSAL.md)
   - Review completed grants in `/proposals/completed`
   - Learn from successful applications

### Step 2: Prepare Your Proposal

1. **Use the Template**
   ```bash
   cp proposals/templates/GRANT_TEMPLATE.md my-proposal.md
   ```

2. **Fill in All Sections**
   - Project Information
   - Executive Summary
   - Background and Significance
   - Objectives and Methodology
   - Budget and Team
   - Impact and Sustainability

3. **Validate Your Proposal** (Optional but Recommended)
   ```bash
   ./scripts/validate-proposal.sh my-proposal.md
   ```

### Step 3: Submit Your Proposal

1. **Create an Issue**
   - Go to [Issues](../../issues)
   - Click "New Issue"
   - Select "Grant Proposal Submission"
   - Fill in all required fields

2. **Attach Documents**
   - Upload your proposal document
   - Include budget spreadsheet
   - Add supporting materials (CVs, letters, etc.)

3. **Submit**
   - Complete the checklist
   - Click "Submit new issue"

### Step 4: Track Your Proposal

1. **Monitor the Issue**
   - Check for comments from reviewers
   - Respond to questions promptly
   - Watch for label changes

2. **Expected Timeline**
   - Initial review: 1-3 business days
   - Technical review: 5-10 business days
   - Final decision: 2-5 business days

3. **Status Labels**
   - `grant-proposal`: Submitted
   - `under-review`: Being evaluated
   - `needs-revision`: Changes needed
   - `approved`: Approved for funding
   - `not-approved`: Declined

### Step 5: After Approval

If your grant is approved:

1. **Repository Creation**
   - A dedicated repository will be created: `CHI-[your-project]`
   - You'll receive access and instructions
   - Project board will be set up

2. **Kickoff Meeting**
   - Schedule with CHI team
   - Review deliverables and timeline
   - Discuss reporting requirements

3. **Start Development**
   - Use your project repository
   - Track deliverables via project board
   - Submit quarterly reports

## For Reviewers

### Step 1: Find Proposals to Review

```bash
# List all proposals awaiting review
gh issue list --label "grant-proposal" --state open
```

Or visit: [Grant Proposals](../../issues?q=is%3Aissue+is%3Aopen+label%3Agrant-proposal)

### Step 2: Start Review

1. **Add Label**
   ```bash
   gh issue edit <issue-number> --add-label "under-review"
   ```

2. **Evaluate Proposal**
   - Use criteria in [Submission Guidelines](SUBMISSION_GUIDELINES.md)
   - Check for CHI alignment
   - Assess technical merit
   - Review budget and team

3. **Provide Feedback**
   - Comment on the issue
   - Be specific and constructive
   - Ask clarifying questions

### Step 3: Make Decision

**If Approved:**
```bash
gh issue edit <issue-number> --add-label "approved"
```

**If Revisions Needed:**
```bash
gh issue edit <issue-number> --add-label "needs-revision"
```

**If Declined:**
```bash
gh issue edit <issue-number> --add-label "not-approved"
gh issue close <issue-number> --comment "Reason for decline..."
```

## For Administrators

### Initial Setup

1. **Set Up Labels**
   ```bash
   ./scripts/setup-labels.sh
   ```

2. **Configure Project Board**
   - Follow guide in [PROJECT_BOARDS.md](PROJECT_BOARDS.md)
   - Set up automation rules
   - Configure custom fields

### Managing Approved Grants

1. **Create Repository**
   ```bash
   ./scripts/create-grant-repo.sh "Project Name" "GRANT-2024-001"
   ```

2. **Push to GitHub**
   ```bash
   cd CHI-project-name
   git remote add origin https://github.com/CHI-CityTech/CHI-project-name.git
   git push -u origin main
   ```

3. **Configure Repository**
   - Add team members
   - Set up branch protection
   - Enable project board
   - Configure webhooks (if needed)

### Monitoring Grants

1. **Track Active Grants**
   ```bash
   gh issue list --label "active-grant"
   ```

2. **Review Deliverables**
   - Check project boards
   - Monitor milestone completion
   - Review quarterly reports

3. **Archive Completed Grants**
   - Move to `/proposals/completed`
   - Add final report
   - Update metrics

## Quick Commands

### For Everyone

```bash
# View all grant proposals
gh issue list --label "grant-proposal"

# View active grants
gh issue list --label "active-grant"

# Search proposals
gh issue list --search "keyword"

# View a specific proposal
gh issue view <issue-number>
```

### For Applicants

```bash
# Validate proposal
./scripts/validate-proposal.sh my-proposal.md

# Create issue from CLI
gh issue create --template grant-proposal.md
```

### For Reviewers

```bash
# Add review label
gh issue edit <issue-number> --add-label "under-review"

# Comment on issue
gh issue comment <issue-number> --body "Your feedback here"

# Approve grant
gh issue edit <issue-number> --add-label "approved"
```

### For Administrators

```bash
# Create grant repository
./scripts/create-grant-repo.sh "Project Name" "GRANT-ID"

# Set up labels
./scripts/setup-labels.sh

# List workflow runs
gh run list --workflow=grant-automation.yml
```

## Troubleshooting

### Common Issues

**Issue: Validation script shows errors**
- Solution: Ensure all required sections are present
- Check the example proposal for reference

**Issue: GitHub Action not triggering**
- Solution: Ensure labels are correctly applied
- Check workflow permissions in repository settings

**Issue: Can't access generated repository**
- Solution: Contact admin to grant access
- Verify repository was created successfully

**Issue: Proposal template missing**
- Solution: Download from `proposals/templates/GRANT_TEMPLATE.md`
- Copy to your working directory

### Getting Help

- 📖 [Full Documentation](../README.md)
- 💬 [Start a Discussion](../../discussions)
- 🐛 [Report an Issue](../../issues)
- 📧 Contact: CHI Grants Team

## Next Steps

### As an Applicant
1. ✅ Read submission guidelines
2. ✅ Prepare your proposal
3. ✅ Validate locally
4. ✅ Submit via issue
5. ✅ Track progress

### As a Reviewer
1. ✅ Find proposals to review
2. ✅ Evaluate using criteria
3. ✅ Provide constructive feedback
4. ✅ Make informed decisions

### As an Administrator
1. ✅ Set up labels and boards
2. ✅ Monitor submissions
3. ✅ Create repositories for approved grants
4. ✅ Track grant progress

## Resources

- [Submission Guidelines](SUBMISSION_GUIDELINES.md)
- [Project Boards Guide](PROJECT_BOARDS.md)
- [Quick Reference](QUICK_REFERENCE.md)
- [Contributing Guide](../CONTRIBUTING.md)
- [Example Proposal](../proposals/examples/EXAMPLE_PROPOSAL.md)

---

**Ready to get started?** Choose your role above and follow the steps! 🚀
