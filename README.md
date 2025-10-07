# CHI-Grants

A comprehensive repository for managing grant proposals, tracking development, and automating grant-related workflows within the CHI (Community Health Initiative) ecosystem.

## 🎯 Purpose

This repository serves as the central hub for:
- **Grant Proposal Submissions** - Submit and track new grant proposals
- **Grant Development** - Monitor progress of active grants
- **CHI Ecosystem Integration** - Connect grants to the larger CHI infrastructure
- **Repository Automation** - Automatically create project repositories for approved grants
- **Project Tracking** - Use GitHub project boards for deliverable and milestone tracking

## 📁 Repository Structure

```
CHI-Grants/
├── .github/
│   ├── workflows/
│   │   └── grant-automation.yml    # Automated grant processing
│   └── ISSUE_TEMPLATE/
│       └── grant-proposal.md       # Grant submission template
├── proposals/
│   ├── templates/
│   │   └── GRANT_TEMPLATE.md       # Standard grant proposal template
│   ├── examples/
│   │   └── EXAMPLE_PROPOSAL.md     # Example completed proposal
│   ├── active/                     # Active grant proposals
│   └── completed/                  # Completed grants
├── scripts/
│   └── create-grant-repo.sh        # Script to create grant repositories
└── docs/
    ├── SUBMISSION_GUIDELINES.md    # How to submit a grant proposal
    └── PROJECT_BOARDS.md           # Project board setup and usage
```

## 🚀 Getting Started

### Submitting a Grant Proposal

1. **Prepare Your Proposal**
   - Review the [Grant Template](proposals/templates/GRANT_TEMPLATE.md)
   - See [Example Proposal](proposals/examples/EXAMPLE_PROPOSAL.md) for reference
   - Read the [Submission Guidelines](docs/SUBMISSION_GUIDELINES.md)

2. **Create a Grant Proposal Issue**
   - Go to [Issues](../../issues) → New Issue
   - Select "Grant Proposal Submission" template
   - Fill in all required information
   - Attach your proposal document

3. **Track Your Proposal**
   - Monitor the issue for feedback
   - Respond to reviewer questions
   - Make revisions as needed

4. **Upon Approval**
   - A dedicated repository will be created for your project
   - You'll receive access to project boards and tracking tools
   - Kickoff meeting will be scheduled

### For Approved Grants

Once your grant is approved:
- **Repository Created:** `CHI-[your-project-name]`
- **Project Board:** Deliverable tracking board configured
- **Team Access:** Collaborators added
- **Documentation:** Templates and structure provided

## 🔧 Automation Features

### Automated Workflows
- **Grant Proposal Processing** - Auto-tags and assigns proposals to project boards
- **Proposal Validation** - Automatically checks proposal completeness
- **Repository Creation** - Generates project repositories for approved grants
- **Status Tracking** - Updates grant status based on labels
- **Notifications** - Sends updates to stakeholders

### Repository Generation Script
Use the provided script to manually create a grant repository:

```bash
./scripts/create-grant-repo.sh "Project Name" "GRANT-2024-001"
```

This creates a complete repository structure with:
- Documentation templates
- Issue templates for deliverables
- GitHub Actions workflows
- Project tracking setup

### Proposal Validation Script
Validate your proposal locally before submission:

```bash
./scripts/validate-proposal.sh my-proposal.md
```

This checks for:
- Required sections
- Key information fields
- CHI integration
- Budget details
- Timeline and deliverables

## 📊 Project Boards

### Grant Tracking Board
Main board columns:
- 📝 Submitted
- 🔍 Under Review
- ✏️ Revisions Needed
- ✅ Approved
- 🚀 Active
- ✔️ Completed
- ❌ Not Approved

See [Project Boards Documentation](docs/PROJECT_BOARDS.md) for detailed setup instructions.

## 📋 Grant Categories

- **Research Grants** - Basic and applied research
- **Development Grants** - Software and tool development
- **Education & Outreach** - Training and community engagement
- **Collaborative Grants** - Multi-institutional partnerships

## 🔍 Review Process

1. **Initial Review** (1-3 days) - Completeness check
2. **Technical Review** (5-10 days) - Detailed evaluation
3. **Decision** (2-5 days) - Final approval/feedback

Total timeline: ~2-3 weeks

## 📚 Resources

### Templates
- [Grant Proposal Template](proposals/templates/GRANT_TEMPLATE.md)
- [Grant Submission Issue Template](.github/ISSUE_TEMPLATE/grant-proposal.md)

### Documentation
- [Submission Guidelines](docs/SUBMISSION_GUIDELINES.md)
- [Project Board Setup](docs/PROJECT_BOARDS.md)

### Examples
- [Example Grant Proposal](proposals/examples/EXAMPLE_PROPOSAL.md)

### Automation
- [Grant Automation Workflow](.github/workflows/grant-automation.yml)
- [Proposal Validation Workflow](.github/workflows/validate-proposal.yml)
- [Repository Creation Script](scripts/create-grant-repo.sh)
- [Proposal Validation Script](scripts/validate-proposal.sh)
- [Label Setup Script](scripts/setup-labels.sh)

## 🤝 CHI Ecosystem Integration

All approved grants integrate with the CHI ecosystem through:
- Standardized APIs for data sharing
- Common documentation frameworks
- Shared project management tools
- Collaborative development practices
- Open-source contribution model

## 💬 Support

- **Questions?** Open a [Discussion](../../discussions)
- **Issues?** File an [Issue](../../issues)
- **Contributions?** Submit a [Pull Request](../../pulls)

## 📈 Metrics & Reporting

Track grant performance through:
- Quarterly progress reports
- Deliverable completion tracking
- Budget utilization monitoring
- Impact assessment metrics

## 🔐 Data & Privacy

All grant materials are subject to:
- CHI data governance policies
- Institutional review requirements
- Privacy and security standards
- Open science principles (where applicable)

## 📝 License

Grant templates and automation tools in this repository are available under MIT License. Individual grant proposals retain their respective licenses as specified by funding agencies and institutions.

---

**Ready to submit a grant proposal?** [Get Started →](../../issues/new?template=grant-proposal.md)
