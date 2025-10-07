# AI Agents Directory

This directory contains AI-powered processing modules for grant information extraction and validation.

## Modules

### ai_extraction_agent.py
- Primary AI agent for extracting grant information from documents
- Handles PDF, DOCX, and text file processing
- Uses OpenAI or similar LLM services for intelligent extraction

### data_models.py
- Defines structured data formats for grant information
- JSON schemas for validation
- Data classes for type safety

### utils.py
- Common utilities for AI processing
- File handling helpers
- Configuration management

## Configuration

AI agents require configuration for:
- API keys (OpenAI, Azure, etc.)
- Model selection and parameters
- Processing timeouts and retry logic
- Confidence thresholds

## Dependencies

Required Python packages:
- openai (for LLM integration)
- PyPDF2 or pdfplumber (for PDF processing)
- python-docx (for Word document processing)
- pydantic (for data validation)