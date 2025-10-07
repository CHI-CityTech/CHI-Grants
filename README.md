# CHI-Grants
Location for materials related to research, acquisition, and management of CHI grant activities.

## Overview
This repository provides an AI-powered automated system for managing and tracking grant information. It features a multi-state workflow that processes grant documents through AI extraction, validation, and human review before generating standardized grant files.

## Repository Structure
```
CHI-Grants/
├── grants/          # Final grant information files
├── scripts/         # Automation and workflow scripts
├── templates/       # Grant templates
├── intake/          # Document upload and processing
│   ├── pending/     # Documents awaiting processing
│   ├── processing/  # Documents being processed by AI
│   └── processed/   # Completed document processing
├── workflows/       # Multi-state workflow management
│   ├── extracted/   # AI-extracted grant data (JSON)
│   ├── validated/   # AI-validated data
│   └── approved/    # Human-approved data
├── ai_agents/       # AI processing modules
└── README.md        # This file
```

## Workflow Overview

The CHI-Grants system uses a **4-state workflow**:

1. **Document Upload** → Upload grant documents (PDF, Word, text)
2. **AI Extraction** → AI extracts structured grant information
3. **Human Review** → Validate and approve AI-extracted data
4. **Grant Generation** → Create final standardized grant files

## Prerequisites

- Python 3.6 or higher
- OpenAI API key (for AI features) - set as `OPENAI_API_KEY` environment variable
- Git (for version control)

### Installation

```bash
# Clone the repository
git clone https://github.com/CHI-CityTech/CHI-Grants.git
cd CHI-Grants

# Install dependencies
pip install -r requirements.txt

# Set OpenAI API key (required for AI features)
export OPENAI_API_KEY="your-api-key-here"
```

## Quick Start

### Option 1: AI-Powered Workflow (Recommended)

#### Step 1: Upload Grant Documents

**Interactive File Browser (Easiest):**
```bash
# Launch interactive uploader with file browser
python3 scripts/interactive_uploader.py
```
This provides a user-friendly interface to:
- Browse and select files visually
- Add metadata interactively  
- Preview files before upload
- Trigger AI processing automatically

**Command Line Upload:**
```bash
# Upload a single document
python3 scripts/upload_grant_documents.py --file grant_proposal.pdf

# Upload multiple documents with metadata
python3 scripts/upload_grant_documents.py \
  --file proposal.pdf --file award_letter.pdf \
  --agency "NSF" --year "2024"
```

#### Step 2: Process with AI
Extract grant information using AI:
```bash
# Process all uploaded documents
python3 ai_agents/ai_extraction_agent.py --process-all

# Process specific document
python3 ai_agents/ai_extraction_agent.py --file path/to/document.pdf
```

#### Step 3: Review and Approve
Review AI-extracted information and approve for final generation:
```bash
# View workflow status
python3 scripts/workflow_manager.py --summary

# List extracted data awaiting review
python3 scripts/workflow_manager.py --list-state extracted
```

#### Step 4: Generate Final Grant Files
Convert approved data to standardized grant files:
```bash
# This will be implemented in Phase 2
# python3 scripts/generate_grant_files.py --from-approved
```

### Option 2: Manual Entry (Legacy Method)

#### Interactive Mode
Run the script without arguments to be prompted for information:
```bash
python3 scripts/add_grant.py
```

#### Command Line Mode
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

## Workflow Management

### Monitor Processing Status
```bash
# View overall workflow summary
python3 scripts/workflow_manager.py --summary

# List documents in specific states
python3 scripts/workflow_manager.py --list-state pending
python3 scripts/workflow_manager.py --list-state extracted
python3 scripts/workflow_manager.py --list-state approved

# Handle error recovery
python3 scripts/workflow_manager.py --cleanup-errors
```

### File Organization
- **Upload documents** to `intake/pending/` (or use upload script)
- **AI extractions** saved to `workflows/extracted/`
- **Final grant files** stored in `grants/` directory
- Each file follows naming convention: `{GRANT_ID}_{grant_name}.md`

### Editing Grant Information
After creating a grant file, you can edit it directly to add more details:
- Update timeline information
- Add co-investigators
- Include project objectives
- Add budget details
- Link to documents
- Update status and progress

## AI Features

### Supported Document Formats
- **PDF** (.pdf) - Extracts text from grant proposals, award letters
- **Word Documents** (.docx, .doc) - Processes application documents
- **Text Files** (.txt, .md) - Handles plain text grant information

### AI Extraction Capabilities
- **Basic Grant Information**: ID, name, funding agency, award amount, type
- **Timeline Data**: Application, award, start, and end dates
- **Team Information**: Principal investigator, co-investigators, personnel
- **Project Details**: Abstract, objectives, technical approach
- **Budget Breakdown**: Personnel, equipment, travel, and total costs
- **Confidence Scoring**: Each extracted field includes confidence levels

### Configuration Options
Set environment variables to customize AI behavior:
```bash
export OPENAI_API_KEY="your-api-key"           # Required for AI features
export CHI_GRANTS_OPENAI_MODEL="gpt-4"         # AI model selection
export CHI_GRANTS_CONFIDENCE_THRESHOLD="0.7"   # Minimum confidence for auto-approval
export CHI_GRANTS_MAX_FILE_SIZE_MB="50"        # Maximum file size for processing
```

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

## Additional Documentation

- **[Usage Guide](USAGE_GUIDE.md)**: Comprehensive step-by-step instructions
- **[Quick Reference](QUICK_REFERENCE.md)**: Quick command reference card
- **[Scripts README](scripts/README.md)**: Script documentation
