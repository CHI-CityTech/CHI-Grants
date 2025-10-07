# CHI-Grants Usage Guide

This guide provides step-by-step instructions for using the CHI-Grants automation system.

## Table of Contents
1. [Getting Started](#getting-started)
2. [Adding a New Grant](#adding-a-new-grant)
3. [Editing Grant Information](#editing-grant-information)
4. [Organizing Grants](#organizing-grants)
5. [Best Practices](#best-practices)

## Getting Started

### Prerequisites
- Python 3.6 or higher
- Git (for committing changes)

### Initial Setup
Clone the repository if you haven't already:
```bash
git clone https://github.com/CHI-CityTech/CHI-Grants.git
cd CHI-Grants
```

## Adding a New Grant

### Method 1: Interactive Mode (Recommended for beginners)

Run the script without arguments:
```bash
python3 scripts/add_grant.py
```

You will be prompted to enter:
- Grant ID
- Grant Name
- Funding Agency
- Award Amount (without $ sign)
- Grant Type
- Principal Investigator Name

### Method 2: Command Line Mode (Quick entry)

Provide all information as arguments:
```bash
python3 scripts/add_grant.py \
  --id NSF-2024-001 \
  --name "AI Research Initiative" \
  --agency "National Science Foundation" \
  --amount 500000 \
  --type Research \
  --pi "Dr. Jane Smith"
```

### Grant ID Format
Use a clear, consistent format for Grant IDs:
- Include agency abbreviation: NSF, NIH, DOE, etc.
- Include year: 2024, 2025, etc.
- Include sequence number: 001, 002, etc.
- Example: `NSF-2024-001`, `NIH-2025-012`

### Grant Types
Common grant types include:
- Research
- Education
- Infrastructure
- Training
- Equipment
- Collaborative

## Editing Grant Information

After creating a grant file, complete the additional details:

1. **Open the file** in your text editor:
   ```bash
   nano grants/NSF-2024-001_ai_research_initiative.md
   # or use your preferred editor
   ```

2. **Update Timeline Information**:
   - Set accurate dates for application, award, start, and end
   - Use YYYY-MM-DD format

3. **Add Team Members**:
   - List co-investigators
   - Include other personnel with their roles

4. **Complete Project Information**:
   - Write a clear abstract (2-3 paragraphs)
   - List specific, measurable objectives
   - Break down the budget by category

5. **Update Status**:
   - Set current status (Active, Completed, Pending, etc.)
   - Add progress updates regularly

6. **Link Documents**:
   - Add links to proposals, awards, reports
   - Can use relative paths or URLs

## Organizing Grants

### Directory Structure
```
grants/
  ├── NSF-2024-001_project_name.md
  ├── NIH-2024-005_project_name.md
  └── DOE-2025-010_project_name.md
```

### File Naming Convention
Files are automatically named as:
```
{GRANT_ID}_{sanitized_grant_name}.md
```
- Grant ID: Preserved as entered
- Grant name: Lowercase, spaces replaced with underscores

### Searching Grants
Find grants by various criteria:
```bash
# By agency
ls grants/ | grep NSF

# By year
ls grants/ | grep 2024

# By keyword in name
ls grants/ | grep -i "research"

# View all grants
ls -lh grants/
```

## Best Practices

### 1. Consistent Naming
- Use standardized Grant IDs
- Include agency, year, and sequence number
- Be descriptive in grant names

### 2. Regular Updates
- Update status and progress regularly
- Add milestones and achievements
- Link to reports and publications

### 3. Complete Information
- Fill out all applicable sections
- Be thorough in the abstract
- Document budget details accurately

### 4. Version Control
- Commit changes regularly:
  ```bash
  git add grants/NSF-2024-001_project.md
  git commit -m "Update grant status: NSF-2024-001"
  git push
  ```

### 5. Collaboration
- Use pull requests for major updates
- Review changes before merging
- Keep teammates informed

### 6. Documentation
- Link to external documents
- Store supporting files in appropriate locations
- Keep README updated with significant changes

## Examples

### Example 1: Research Grant
```bash
python3 scripts/add_grant.py \
  --id NSF-2024-100 \
  --name "Machine Learning for Climate Prediction" \
  --agency "National Science Foundation" \
  --amount 850000 \
  --type Research \
  --pi "Dr. Emily Chen"
```

### Example 2: Education Grant
```bash
python3 scripts/add_grant.py \
  --id DOE-2024-050 \
  --name "STEM Education Outreach Program" \
  --agency "Department of Education" \
  --amount 250000 \
  --type Education \
  --pi "Dr. Michael Brown"
```

### Example 3: Equipment Grant
```bash
python3 scripts/add_grant.py \
  --id NIH-2025-025 \
  --name "Advanced Microscopy Equipment Acquisition" \
  --agency "National Institutes of Health" \
  --amount 1200000 \
  --type Equipment \
  --pi "Dr. Lisa Wang"
```

## Troubleshooting

### Script won't run
- Check Python version: `python3 --version` (needs 3.6+)
- Ensure script is executable: `chmod +x scripts/add_grant.py`

### File already exists
- The script won't overwrite existing files
- Choose a different Grant ID or remove the existing file

### Missing template
- Ensure `templates/grant_template.md` exists
- Re-clone repository if needed

## Support

For questions or issues:
1. Check this guide
2. Review the README.md
3. Open an issue on GitHub
4. Contact repository administrators
