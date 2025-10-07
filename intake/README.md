# Intake Directory

This directory manages the document intake process for grants.

## Subdirectories

### pending/
- Raw documents uploaded for processing
- Supported formats: PDF, DOCX, TXT, MD
- Files here are waiting to be processed by AI agents

### processing/
- Documents currently being processed by AI extraction agents
- Temporary location during AI analysis
- Files are moved here from pending/ during processing

### processed/
- Documents that have completed AI extraction
- Contains original documents with corresponding extracted data
- Files remain here for reference and audit trail

## File Naming Convention

Upload files with descriptive names:
- `{agency}_{year}_{brief_description}.{ext}`
- Example: `NSF_2024_AI_Research_Proposal.pdf`

## Workflow

1. Upload documents to `pending/`
2. Run `upload_grant_documents.py` to process
3. AI moves files through processing/ to processed/
4. Extracted data appears in `workflows/extracted/`