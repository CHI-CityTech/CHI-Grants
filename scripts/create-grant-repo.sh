#!/bin/bash

# Grant Repository Setup Script
# This script creates a new repository for an approved grant project

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_message() {
    local color=$1
    local message=$2
    echo -e "${color}${message}${NC}"
}

# Check if required arguments are provided
if [ "$#" -lt 2 ]; then
    print_message "$RED" "Usage: $0 <project-name> <grant-number>"
    print_message "$YELLOW" "Example: $0 'AI-Healthcare-Study' 'GRANT-2024-001'"
    exit 1
fi

PROJECT_NAME="$1"
GRANT_NUMBER="$2"
PROJECT_SLUG=$(echo "$PROJECT_NAME" | tr '[:upper:]' '[:lower:]' | tr ' ' '-')
REPO_NAME="CHI-${PROJECT_SLUG}"

print_message "$GREEN" "=== CHI Grant Repository Setup ==="
echo ""
print_message "$YELLOW" "Project Name: $PROJECT_NAME"
print_message "$YELLOW" "Grant Number: $GRANT_NUMBER"
print_message "$YELLOW" "Repository Name: $REPO_NAME"
echo ""

# Create local directory structure
print_message "$GREEN" "Creating local repository structure..."
mkdir -p "$REPO_NAME"
cd "$REPO_NAME"

# Initialize git repository
git init

# Create directory structure
mkdir -p docs src tests deliverables .github/workflows .github/ISSUE_TEMPLATE

# Create README.md
cat > README.md << EOF
# $PROJECT_NAME

**Grant Number:** $GRANT_NUMBER

## Project Overview
*Add project description here*

## CHI Ecosystem Integration
This project is part of the CHI (Community Health Initiative) ecosystem.

## Getting Started
*Add setup instructions here*

## Documentation
- [Project Plan](docs/PROJECT_PLAN.md)
- [Technical Documentation](docs/TECHNICAL_DOCS.md)
- [Deliverables Tracking](docs/DELIVERABLES.md)

## Team
*List team members here*

## License
*Add license information*

## Acknowledgments
This project is funded through the CHI grant program.
EOF

# Create project documentation
cat > docs/PROJECT_PLAN.md << EOF
# Project Plan - $PROJECT_NAME

## Objectives
1. 
2. 
3. 

## Timeline
| Phase | Duration | Deliverables |
|-------|----------|--------------|
| Phase 1 | | |
| Phase 2 | | |
| Phase 3 | | |

## Resources
- Personnel:
- Equipment:
- Budget:

## Risk Management
| Risk | Mitigation Strategy |
|------|-------------------|
| | |
EOF

cat > docs/DELIVERABLES.md << EOF
# Deliverables Tracking - $PROJECT_NAME

## Grant Requirements
- [ ] Deliverable 1: 
- [ ] Deliverable 2: 
- [ ] Deliverable 3: 

## Status Reports
### Month 1
*Add status update*

### Month 2
*Add status update*

## Final Report
*To be completed at project end*
EOF

cat > docs/TECHNICAL_DOCS.md << EOF
# Technical Documentation - $PROJECT_NAME

## Architecture
*Describe system architecture*

## Technologies Used
- 
- 

## Development Setup
\`\`\`bash
# Add setup commands
\`\`\`

## API Documentation
*If applicable*

## Testing
*Describe testing approach*
EOF

# Create GitHub workflow
cat > .github/workflows/ci.yml << EOF
name: CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Run tests
      run: |
        # Add test commands here
        echo "Tests will be configured based on project needs"
EOF

# Create issue templates
cat > .github/ISSUE_TEMPLATE/deliverable.md << EOF
---
name: Deliverable Tracking
about: Track grant deliverable progress
title: '[DELIVERABLE] '
labels: deliverable
assignees: ''
---

## Deliverable Information
**Deliverable Name:** 
**Due Date:** 
**Grant Milestone:** 

## Description
*Describe the deliverable*

## Completion Criteria
- [ ] 
- [ ] 
- [ ] 

## Status
- [ ] In Progress
- [ ] Completed
- [ ] Submitted to funding agency
EOF

# Create .gitignore
cat > .gitignore << EOF
# Dependencies
node_modules/
venv/
__pycache__/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Build
dist/
build/
*.egg-info/

# Secrets
.env
*.key
*.pem
EOF

# Initial commit
git add .
git commit -m "Initial repository setup for $PROJECT_NAME (Grant: $GRANT_NUMBER)"

print_message "$GREEN" "✅ Repository structure created successfully!"
echo ""
print_message "$YELLOW" "Next steps:"
echo "1. Create remote repository on GitHub: https://github.com/CHI-CityTech/$REPO_NAME"
echo "2. Run: git remote add origin https://github.com/CHI-CityTech/$REPO_NAME.git"
echo "3. Run: git push -u origin main"
echo "4. Configure repository settings and team access"
echo "5. Set up project board for deliverable tracking"
echo ""
print_message "$GREEN" "Repository is ready in: $(pwd)"
