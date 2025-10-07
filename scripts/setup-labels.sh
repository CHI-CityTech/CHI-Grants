#!/bin/bash

# Setup Labels for CHI-Grants Repository
# This script creates all required labels for grant management

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}=== CHI-Grants Label Setup ===${NC}\n"

# Check if gh CLI is installed
if ! command -v gh &> /dev/null; then
    echo -e "${RED}Error: GitHub CLI (gh) is not installed${NC}"
    echo "Install it from: https://cli.github.com/"
    exit 1
fi

# Check if authenticated
if ! gh auth status &> /dev/null; then
    echo -e "${RED}Error: Not authenticated with GitHub CLI${NC}"
    echo "Run: gh auth login"
    exit 1
fi

echo -e "${YELLOW}Creating labels...${NC}\n"

# Function to create label
create_label() {
    local name=$1
    local color=$2
    local description=$3
    
    if gh label create "$name" --color "$color" --description "$description" 2>/dev/null; then
        echo -e "${GREEN}✓${NC} Created: $name"
    else
        echo -e "${YELLOW}→${NC} Already exists: $name"
    fi
}

# Status Labels
echo -e "\n${YELLOW}Status Labels:${NC}"
create_label "grant-proposal" "0366d6" "New grant proposal submission"
create_label "under-review" "fbca04" "Currently being reviewed"
create_label "needs-revision" "d93f0b" "Requires modifications before approval"
create_label "approved" "0e8a16" "Approved for funding"
create_label "active-grant" "2da44e" "Currently active project"
create_label "completed" "d4c5f9" "Grant finished"
create_label "on-hold" "fbca04" "Temporarily paused"
create_label "not-approved" "d73a4a" "Declined"

# Priority Labels
echo -e "\n${YELLOW}Priority Labels:${NC}"
create_label "priority:high" "b60205" "Urgent attention needed"
create_label "priority:medium" "fbca04" "Normal priority"
create_label "priority:low" "0e8a16" "Low priority"

# Type Labels
echo -e "\n${YELLOW}Type Labels:${NC}"
create_label "deliverable" "5319e7" "Grant deliverable item"
create_label "milestone" "1d76db" "Major milestone"
create_label "report" "fbca04" "Reporting requirement"
create_label "admin" "d4c5f9" "Administrative task"
create_label "question" "d876e3" "Question or clarification needed"

# Category Labels
echo -e "\n${YELLOW}Category Labels:${NC}"
create_label "research" "006b75" "Research-related"
create_label "development" "0075ca" "Development work"
create_label "documentation" "0e8a16" "Documentation task"
create_label "outreach" "d93f0b" "Outreach activity"
create_label "education" "fef2c0" "Educational initiative"
create_label "collaborative" "bfdadc" "Multi-institutional project"

# Size Labels
echo -e "\n${YELLOW}Size/Effort Labels:${NC}"
create_label "size:small" "c5def5" "< 1 week effort"
create_label "size:medium" "fef2c0" "1-4 weeks effort"
create_label "size:large" "f9d0c4" "> 1 month effort"

echo -e "\n${GREEN}✓ Label setup complete!${NC}"
echo -e "\nView all labels at: $(gh repo view --json url -q .url)/labels"
