#!/bin/bash

# Validate Grant Proposal Script
# Check if a grant proposal meets basic requirements before submission

# Don't use set -e because we're using conditional arithmetic
set +e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

print_header() {
    echo -e "${GREEN}=== CHI Grant Proposal Validator ===${NC}\n"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

# Check if file is provided
if [ "$#" -lt 1 ]; then
    print_header
    echo "Usage: $0 <proposal-file.md>"
    echo ""
    echo "Example:"
    echo "  $0 my-proposal.md"
    exit 1
fi

PROPOSAL_FILE="$1"

# Check if file exists
if [ ! -f "$PROPOSAL_FILE" ]; then
    print_error "File not found: $PROPOSAL_FILE"
    exit 1
fi

print_header
echo "Validating: $PROPOSAL_FILE"
echo ""

# Initialize counters
ERRORS=0
WARNINGS=0
PASSES=0

# Check for required sections
echo "Checking required sections..."

REQUIRED_SECTIONS=(
    "## Project Information"
    "## Executive Summary"
    "## Project Background and Significance"
    "## Project Objectives"
    "## Methodology and Approach"
    "## Budget"
    "## Team and Resources"
    "## Impact and Sustainability"
)

for section in "${REQUIRED_SECTIONS[@]}"; do
    if grep -qF "$section" "$PROPOSAL_FILE"; then
        print_success "$section"
        ((PASSES++))
    else
        print_error "Missing section: $section"
        ((ERRORS++))
    fi
done

echo ""
echo "Checking key fields..."

# Check for key fields
KEY_FIELDS=(
    "Project Title:"
    "Principal Investigator"
    "Funding Amount"
    "Project Duration"
)

for field in "${KEY_FIELDS[@]}"; do
    if grep -qi "$field" "$PROPOSAL_FILE"; then
        print_success "$field found"
        ((PASSES++))
    else
        print_warning "Field may be missing: $field"
        ((WARNINGS++))
    fi
done

echo ""
echo "Checking content quality..."

# Check for CHI integration
if grep -qi "CHI" "$PROPOSAL_FILE"; then
    print_success "CHI ecosystem integration mentioned"
    ((PASSES++))
else
    print_error "No mention of CHI ecosystem integration"
    ((ERRORS++))
fi

# Check for budget details
if grep -qi "budget" "$PROPOSAL_FILE"; then
    print_success "Budget information included"
    ((PASSES++))
else
    print_error "No budget information found"
    ((ERRORS++))
fi

# Check for timeline/milestones
if grep -qi -e "timeline" -e "milestone" "$PROPOSAL_FILE"; then
    print_success "Timeline or milestones included"
    ((PASSES++))
else
    print_warning "No timeline or milestones found"
    ((WARNINGS++))
fi

# Check for deliverables
if grep -qi "deliverable" "$PROPOSAL_FILE"; then
    print_success "Deliverables mentioned"
    ((PASSES++))
else
    print_warning "No deliverables explicitly mentioned"
    ((WARNINGS++))
fi

# Check for references
if grep -qi -e "reference" -e "citation" "$PROPOSAL_FILE"; then
    print_success "References or citations included"
    ((PASSES++))
else
    print_warning "No references found (consider adding relevant citations)"
    ((WARNINGS++))
fi

# Check file size (should have substantial content)
FILE_SIZE=$(wc -c < "$PROPOSAL_FILE")
if [ "$FILE_SIZE" -gt 5000 ]; then
    print_success "Proposal has substantial content ($(numfmt --to=iec-i --suffix=B $FILE_SIZE))"
    ((PASSES++))
else
    print_warning "Proposal may be too short ($(numfmt --to=iec-i --suffix=B $FILE_SIZE)). Consider adding more detail."
    ((WARNINGS++))
fi

# Summary
echo ""
echo "================================"
echo "Validation Summary:"
echo "================================"
echo -e "Passes:   ${GREEN}$PASSES${NC}"
echo -e "Warnings: ${YELLOW}$WARNINGS${NC}"
echo -e "Errors:   ${RED}$ERRORS${NC}"
echo ""

if [ "$ERRORS" -eq 0 ] && [ "$WARNINGS" -eq 0 ]; then
    echo -e "${GREEN}✓ Excellent! Your proposal looks ready for submission.${NC}"
    exit 0
elif [ "$ERRORS" -eq 0 ]; then
    echo -e "${YELLOW}⚠ Your proposal is acceptable but has some warnings. Consider addressing them.${NC}"
    exit 0
else
    echo -e "${RED}✗ Your proposal has errors that should be fixed before submission.${NC}"
    exit 1
fi
