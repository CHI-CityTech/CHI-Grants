# CHI-Grants
Location for materials related to research, acquisition, and management of CHI grant activities.

## Overview
This repository provides an automated system for managing and tracking grant information. It includes templates, automation scripts, and a structured approach to organizing grant-related materials.

## Repository Structure
```
CHI-Grants/
├── grants/          # Grant information files
├── scripts/         # Automation scripts
├── templates/       # Grant templates
└── README.md        # This file
```

## Quick Start

### Adding a New Grant

#### Option 1: Interactive Mode
Run the script without arguments to be prompted for information:
```bash
python3 scripts/add_grant.py
```

#### Option 2: Command Line Mode
Provide all information as command line arguments:
```bash
python3 scripts/add_grant.py \
  --id NSF-2024-001 \
  --name "AI Research Initiative" \
  --agency "National Science Foundation" \
  --amount 500000 \
  --type Research \
  --pi "Dr. Jane Smith"
```

### Viewing Grants
All grant files are stored in the `grants/` directory. Each file follows a standardized naming convention: `{GRANT_ID}_{grant_name}.md`

### Editing Grant Information
After creating a grant file, you can edit it directly to add more details:
- Update timeline information
- Add co-investigators
- Include project objectives
- Add budget details
- Link to documents
- Update status and progress

## Grant Information Fields

Each grant file includes the following sections:

- **Grant Details**: ID, name, funding agency, amount, and type
- **Timeline**: Application, award, start, and end dates
- **Team**: PI, co-investigators, and other personnel
- **Project Information**: Abstract, objectives, and budget summary
- **Status**: Current status and progress updates
- **Documents**: Links to proposals, awards, and reports
- **Notes**: Additional comments and information

## Workflow

1. **Create Grant Entry**: Use the automation script to create a new grant file
2. **Complete Details**: Edit the generated file to add comprehensive information
3. **Commit Changes**: Add and commit the grant file to the repository
4. **Update Regularly**: Keep grant status and progress information current

## Example

An example grant file is included in the repository at:
```
grants/EXAMPLE-2024-001_example_grant_for_demonstration.md
```

## Contributing

When adding new grants:
1. Use the provided automation script
2. Follow the template structure
3. Include all required information
4. Use clear, descriptive grant names
5. Keep information up to date

## Support

For questions or issues with the grant management system, please open an issue in this repository.
