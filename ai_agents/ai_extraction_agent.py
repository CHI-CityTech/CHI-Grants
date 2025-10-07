#!/usr/bin/env python3
"""
AI Extraction Agent for CHI-Grants System
Uses OpenAI GPT models to extract grant information from documents.
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import time

# Add project paths
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root / "scripts"))
sys.path.append(str(project_root / "ai_agents"))

from data_models import (
    GrantData, ExtractedField, ConfidenceLevel, TeamMember, 
    Timeline, BudgetSummary, ProjectInfo, ExtractionMetadata,
    GrantDataValidator, save_grant_data
)
from workflow_manager import WorkflowManager, WorkflowState


class DocumentProcessor:
    """Handles different document formats for text extraction."""
    
    @staticmethod
    def extract_text_from_pdf(filepath: str) -> str:
        """Extract text from PDF file."""
        try:
            import PyPDF2
            text = ""
            with open(filepath, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                for page in reader.pages:
                    text += page.extract_text() + "\n"
            return text
        except ImportError:
            raise ImportError("PyPDF2 package required for PDF processing. Install with: pip install PyPDF2")
        except Exception as e:
            raise Exception(f"Error extracting PDF text: {e}")
    
    @staticmethod
    def extract_text_from_docx(filepath: str) -> str:
        """Extract text from Word document."""
        try:
            import docx
            doc = docx.Document(filepath)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        except ImportError:
            raise ImportError("python-docx package required for Word processing. Install with: pip install python-docx")
        except Exception as e:
            raise Exception(f"Error extracting Word text: {e}")
    
    @staticmethod
    def extract_text_from_txt(filepath: str) -> str:
        """Extract text from plain text file."""
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                return file.read()
        except UnicodeDecodeError:
            # Try with different encoding
            with open(filepath, 'r', encoding='latin-1') as file:
                return file.read()
        except Exception as e:
            raise Exception(f"Error reading text file: {e}")
    
    @classmethod
    def extract_text(cls, filepath: str) -> Tuple[str, Dict]:
        """Extract text from any supported document format."""
        file_path = Path(filepath)
        extension = file_path.suffix.lower()
        
        start_time = time.time()
        
        if extension == '.pdf':
            text = cls.extract_text_from_pdf(filepath)
        elif extension in ['.docx', '.doc']:
            text = cls.extract_text_from_docx(filepath)
        elif extension in ['.txt', '.md']:
            text = cls.extract_text_from_txt(filepath)
        else:
            raise ValueError(f"Unsupported file format: {extension}")
        
        processing_time = time.time() - start_time
        
        # Extract basic metadata
        stat = file_path.stat()
        metadata = {
            'file_size_bytes': stat.st_size,
            'text_length_chars': len(text),
            'extraction_time_seconds': processing_time,
            'file_extension': extension
        }
        
        # Estimate page count for PDFs
        if extension == '.pdf':
            try:
                import PyPDF2
                with open(filepath, 'rb') as file:
                    reader = PyPDF2.PdfReader(file)
                    metadata['total_pages'] = len(reader.pages)
            except:
                metadata['total_pages'] = None
        
        return text, metadata


class AIExtractionAgent:
    """AI agent for extracting grant information from documents."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4"):
        """Initialize AI extraction agent."""
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        self.model = model
        self.workflow_manager = WorkflowManager()
        
        if not self.api_key:
            print("Warning: No OpenAI API key found. Set OPENAI_API_KEY environment variable or pass api_key parameter.")
            print("You can also run in simulation mode for testing.")
    
    def _call_openai(self, prompt: str, text: str) -> str:
        """Call OpenAI API with the given prompt and text."""
        if not self.api_key:
            return self._simulate_ai_response()
        
        try:
            import openai
            
            # Set up OpenAI client
            client = openai.OpenAI(api_key=self.api_key)
            
            # Construct messages
            messages = [
                {"role": "system", "content": prompt},
                {"role": "user", "content": f"Document text to analyze:\n\n{text[:8000]}"}  # Limit text length
            ]
            
            # Make API call
            response = client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.1,  # Low temperature for consistent extraction
                max_tokens=2000
            )
            
            return response.choices[0].message.content
            
        except ImportError:
            raise ImportError("openai package required for AI processing. Install with: pip install openai")
        except Exception as e:
            print(f"OpenAI API error: {e}")
            return self._simulate_ai_response()
    
    def _simulate_ai_response(self) -> str:
        """Simulate AI response for testing without API key."""
        return json.dumps({
            "grant_id": {"value": "SIMULATED-2024-001", "confidence": "medium"},
            "grant_name": {"value": "Simulated Grant Extraction", "confidence": "high"},
            "funding_agency": {"value": "Simulation Foundation", "confidence": "high"},
            "award_amount": {"value": 100000, "confidence": "medium"},
            "grant_type": {"value": "Research", "confidence": "high"},
            "principal_investigator": {
                "name": {"value": "Dr. Simulation Researcher", "confidence": "high"},
                "role": {"value": "Principal Investigator", "confidence": "high"}
            },
            "timeline": {
                "project_start_date": {"value": "2024-01-01", "confidence": "low"},
                "project_end_date": {"value": "2026-12-31", "confidence": "low"}
            },
            "project": {
                "abstract": {"value": "This is a simulated grant extraction for testing purposes.", "confidence": "high"}
            },
            "budget": {
                "total": {"value": 100000, "confidence": "medium"}
            }
        })
    
    def create_extraction_prompt(self) -> str:
        """Create the prompt for grant information extraction."""
        return """You are an expert grant information extraction system. Your task is to extract structured information from grant-related documents including proposals, award letters, and application materials.

Extract the following information in JSON format with confidence scores:

1. Basic Grant Information:
   - grant_id (grant identifier, award number, etc.)
   - grant_name (title of the grant/project)
   - funding_agency (organization providing funding)
   - award_amount (monetary value, extract number only)
   - grant_type (Research/Education/Infrastructure/Training/Equipment/Other)

2. Timeline:
   - application_date (when application was submitted)
   - award_date (when grant was awarded)
   - project_start_date (project start date)
   - project_end_date (project end date)

3. Team Information:
   - principal_investigator (name and role)
   - co_investigators (list of co-investigators if any)

4. Project Information:
   - abstract (project summary/description)
   - objectives (list of project goals)

5. Budget Summary:
   - personnel (personnel costs)
   - equipment (equipment costs)
   - travel (travel costs)
   - total (total award amount)

For each extracted field, provide:
- "value": the extracted information
- "confidence": "high" (90-100%), "medium" (70-89%), "low" (50-69%), or "uncertain" (<50%)

If information is not found or unclear, use "uncertain" confidence and provide your best interpretation.

Return only valid JSON. Use null for missing values."""
    
    def parse_ai_response(self, response: str) -> GrantData:
        """Parse AI response into GrantData structure."""
        try:
            data = json.loads(response)
        except json.JSONDecodeError as e:
            print(f"Error parsing AI response as JSON: {e}")
            return self._create_empty_grant_data()
        
        grant_data = GrantData()
        
        # Helper function to create ExtractedField
        def create_field(value, confidence_str):
            if value is None:
                return None
            confidence_map = {
                "high": ConfidenceLevel.HIGH,
                "medium": ConfidenceLevel.MEDIUM,
                "low": ConfidenceLevel.LOW,
                "uncertain": ConfidenceLevel.UNCERTAIN
            }
            confidence = confidence_map.get(confidence_str.lower(), ConfidenceLevel.UNCERTAIN)
            return ExtractedField(value, confidence)
        
        # Extract basic information
        if "grant_id" in data:
            grant_data.grant_id = create_field(
                data["grant_id"].get("value"), 
                data["grant_id"].get("confidence", "uncertain")
            )
        
        if "grant_name" in data:
            grant_data.grant_name = create_field(
                data["grant_name"].get("value"),
                data["grant_name"].get("confidence", "uncertain")
            )
        
        if "funding_agency" in data:
            grant_data.funding_agency = create_field(
                data["funding_agency"].get("value"),
                data["funding_agency"].get("confidence", "uncertain")
            )
        
        if "award_amount" in data:
            grant_data.award_amount = create_field(
                data["award_amount"].get("value"),
                data["award_amount"].get("confidence", "uncertain")
            )
        
        if "grant_type" in data:
            grant_data.grant_type = create_field(
                data["grant_type"].get("value"),
                data["grant_type"].get("confidence", "uncertain")
            )
        
        # Extract timeline
        if "timeline" in data:
            timeline_data = data["timeline"]
            grant_data.timeline = Timeline()
            
            for field in ["project_start_date", "project_end_date", "application_date", "award_date"]:
                if field in timeline_data:
                    setattr(grant_data.timeline, field, create_field(
                        timeline_data[field].get("value"),
                        timeline_data[field].get("confidence", "uncertain")
                    ))
        
        # Extract principal investigator
        if "principal_investigator" in data:
            pi_data = data["principal_investigator"]
            if "name" in pi_data:
                grant_data.principal_investigator = TeamMember(
                    name=create_field(
                        pi_data["name"].get("value"),
                        pi_data["name"].get("confidence", "uncertain")
                    ),
                    role=create_field(
                        pi_data.get("role", {}).get("value", "Principal Investigator"),
                        pi_data.get("role", {}).get("confidence", "high")
                    )
                )
        
        # Extract project information
        if "project" in data:
            project_data = data["project"]
            grant_data.project = ProjectInfo()
            
            if "abstract" in project_data:
                grant_data.project.abstract = create_field(
                    project_data["abstract"].get("value"),
                    project_data["abstract"].get("confidence", "uncertain")
                )
        
        # Extract budget
        if "budget" in data:
            budget_data = data["budget"]
            grant_data.budget = BudgetSummary()
            
            for field in ["personnel", "equipment", "travel", "total"]:
                if field in budget_data:
                    setattr(grant_data.budget, field, create_field(
                        budget_data[field].get("value"),
                        budget_data[field].get("confidence", "uncertain")
                    ))
        
        return grant_data
    
    def _create_empty_grant_data(self) -> GrantData:
        """Create empty grant data structure for failed extractions."""
        return GrantData()
    
    def process_document(self, filepath: str) -> Tuple[bool, GrantData, str]:
        """Process a single document and extract grant information."""
        start_time = time.time()
        
        try:
            # Extract text from document
            print(f"Extracting text from: {Path(filepath).name}")
            text, file_metadata = DocumentProcessor.extract_text(filepath)
            
            if not text.strip():
                return False, self._create_empty_grant_data(), "No text extracted from document"
            
            print(f"Extracted {len(text)} characters of text")
            
            # Use AI to extract grant information
            print("Calling AI for information extraction...")
            prompt = self.create_extraction_prompt()
            ai_response = self._call_openai(prompt, text)
            
            # Parse AI response
            grant_data = self.parse_ai_response(ai_response)
            
            # Add extraction metadata
            total_time = time.time() - start_time
            grant_data.extraction_metadata = ExtractionMetadata(
                source_document=Path(filepath).name,
                extraction_timestamp=datetime.now(),
                ai_model_used=self.model,
                processing_time_seconds=total_time,
                total_pages=file_metadata.get('total_pages'),
                file_size_bytes=file_metadata.get('file_size_bytes')
            )
            
            # Validate extracted data
            validator = GrantDataValidator()
            grant_data.validation_flags = validator.validate(grant_data)
            
            print(f"✓ Extraction completed in {total_time:.1f}s")
            return True, grant_data, "Extraction successful"
            
        except Exception as e:
            error_msg = f"Document processing failed: {e}"
            print(f"✗ {error_msg}")
            return False, self._create_empty_grant_data(), error_msg
    
    def process_pending_documents(self, limit: int = 5) -> List[Tuple[str, bool, str]]:
        """Process multiple pending documents."""
        # Get pending documents from workflow manager
        pending_files = self.workflow_manager.get_next_documents_for_processing(
            WorkflowState.PROCESSING, limit
        )
        
        if not pending_files:
            print("No documents in processing state")
            return []
        
        results = []
        
        for filename in pending_files:
            print(f"\n=== Processing {filename} ===")
            
            # Get full path
            processing_dir = Path(self.workflow_manager.base_path) / "intake" / "processing"
            filepath = processing_dir / filename
            
            if not filepath.exists():
                error_msg = f"File not found: {filepath}"
                print(f"✗ {error_msg}")
                self.workflow_manager.transition_state(filename, WorkflowState.ERROR, error_msg)
                results.append((filename, False, error_msg))
                continue
            
            # Process document
            success, grant_data, message = self.process_document(str(filepath))
            
            if success:
                # Save extracted data
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_filename = f"{timestamp}_{filename.replace('.', '_')}.json"
                output_path = Path(self.workflow_manager.base_path) / "workflows" / "extracted" / output_filename
                
                try:
                    output_path.parent.mkdir(parents=True, exist_ok=True)
                    save_grant_data(grant_data, str(output_path))
                    
                    # Move to extracted state
                    self.workflow_manager.transition_state(filename, WorkflowState.EXTRACTED)
                    
                    # Move original document to processed
                    processed_dir = Path(self.workflow_manager.base_path) / "intake" / "processed"
                    processed_dir.mkdir(parents=True, exist_ok=True)
                    filepath.rename(processed_dir / filename)
                    
                    print(f"✓ Saved extraction results: {output_filename}")
                    results.append((filename, True, f"Extracted to {output_filename}"))
                    
                except Exception as e:
                    error_msg = f"Failed to save results: {e}"
                    print(f"✗ {error_msg}")
                    self.workflow_manager.transition_state(filename, WorkflowState.ERROR, error_msg)
                    results.append((filename, False, error_msg))
            else:
                # Mark as error
                self.workflow_manager.transition_state(filename, WorkflowState.ERROR, message)
                results.append((filename, False, message))
        
        return results


def main():
    """Command line interface for AI extraction agent."""
    import argparse
    
    parser = argparse.ArgumentParser(description='AI Grant Information Extraction Agent')
    parser.add_argument('--file', help='Process specific file')
    parser.add_argument('--process-all', action='store_true',
                       help='Process all documents in processing state')
    parser.add_argument('--limit', type=int, default=5,
                       help='Maximum number of documents to process')
    parser.add_argument('--model', default='gpt-4',
                       help='OpenAI model to use (default: gpt-4)')
    parser.add_argument('--api-key', help='OpenAI API key (or set OPENAI_API_KEY env var)')
    
    args = parser.parse_args()
    
    # Initialize agent
    agent = AIExtractionAgent(api_key=args.api_key, model=args.model)
    
    if args.file:
        # Process specific file
        success, grant_data, message = agent.process_document(args.file)
        if success:
            print(f"✓ Processing successful: {message}")
            # Save results
            output_path = f"{Path(args.file).stem}_extracted.json"
            save_grant_data(grant_data, output_path)
            print(f"Results saved to: {output_path}")
        else:
            print(f"✗ Processing failed: {message}")
            sys.exit(1)
    
    elif args.process_all:
        # Process pending documents
        results = agent.process_pending_documents(limit=args.limit)
        
        if not results:
            print("No documents to process")
            return
        
        # Summary
        successful = sum(1 for _, success, _ in results if success)
        print(f"\n=== Processing Summary ===")
        print(f"Total processed: {len(results)}")
        print(f"Successful: {successful}")
        print(f"Failed: {len(results) - successful}")
        
        # Show details
        for filename, success, message in results:
            status = "✓" if success else "✗"
            print(f"{status} {filename}: {message}")
    
    else:
        print("Use --file to process specific file or --process-all for batch processing")
        print("Use --help for more options")


if __name__ == '__main__':
    main()