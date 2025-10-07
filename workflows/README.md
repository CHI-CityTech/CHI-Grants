# Workflows Directory

This directory manages the workflow states for grant processing.

## Subdirectories

### extracted/
- JSON files containing AI-extracted grant information
- Includes confidence scores and identified fields
- Files named: `{timestamp}_{source_document_name}.json`

### validated/
- JSON files that have passed AI validation
- Contains enriched data and flagged uncertainties
- Ready for human review

### approved/
- JSON files approved by humans
- Final structured data ready for template generation
- Input for generating final grant markdown files

## Data Flow

```
intake/processed/ → workflows/extracted/ → workflows/validated/ → workflows/approved/ → grants/
```

## File Structure

Each JSON file contains:
- Source document information
- Extracted grant fields
- Confidence scores
- Processing timestamps
- Validation flags