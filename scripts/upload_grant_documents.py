#!/usr/bin/env python3
"""
Document Upload Handler for CHI-Grants System
Handles PDF, Word, and text file uploads and initiates AI processing.
"""

import os
import sys
import shutil
import argparse
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime

# Add ai_agents to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'ai_agents'))
sys.path.append(os.path.join(os.path.dirname(__file__)))

from workflow_manager import WorkflowManager, WorkflowState


class DocumentUploader:
    """Handles document uploads and initiates processing workflow."""
    
    SUPPORTED_FORMATS = {'.pdf', '.docx', '.doc', '.txt', '.md'}
    MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB limit
    
    def __init__(self, base_path: str = ".."):
        """Initialize uploader with base repository path."""
        self.base_path = Path(base_path).resolve()
        self.workflow_manager = WorkflowManager(str(self.base_path))
        self.intake_pending = self.base_path / "intake" / "pending"
        
        # Ensure directories exist
        self.intake_pending.mkdir(parents=True, exist_ok=True)
    
    def validate_file(self, filepath: str) -> tuple[bool, str]:
        """Validate uploaded file format and size."""
        file_path = Path(filepath)
        
        # Check if file exists
        if not file_path.exists():
            return False, f"File does not exist: {filepath}"
        
        # Check file extension
        if file_path.suffix.lower() not in self.SUPPORTED_FORMATS:
            return False, f"Unsupported file format. Supported: {', '.join(self.SUPPORTED_FORMATS)}"
        
        # Check file size
        file_size = file_path.stat().st_size
        if file_size > self.MAX_FILE_SIZE:
            return False, f"File too large ({file_size / 1024 / 1024:.1f}MB). Maximum: {self.MAX_FILE_SIZE / 1024 / 1024}MB"
        
        # Check if file is readable
        try:
            with open(filepath, 'rb') as f:
                f.read(1024)  # Try to read first 1KB
        except Exception as e:
            return False, f"Cannot read file: {e}"
        
        return True, "File validation passed"
    
    def generate_unique_filename(self, original_filename: str) -> str:
        """Generate unique filename to avoid conflicts."""
        base_name = Path(original_filename).stem
        extension = Path(original_filename).suffix
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Clean the base name
        clean_name = "".join(c for c in base_name if c.isalnum() or c in "-_. ")
        clean_name = clean_name.replace(" ", "_")
        
        unique_name = f"{timestamp}_{clean_name}{extension}"
        
        # Ensure uniqueness
        counter = 1
        while (self.intake_pending / unique_name).exists():
            unique_name = f"{timestamp}_{clean_name}_{counter}{extension}"
            counter += 1
        
        return unique_name
    
    def extract_metadata(self, filepath: str) -> Dict:
        """Extract basic metadata from uploaded file."""
        file_path = Path(filepath)
        stat = file_path.stat()
        
        metadata = {
            'original_filename': file_path.name,
            'file_size_bytes': stat.st_size,
            'file_extension': file_path.suffix.lower(),
            'upload_timestamp': datetime.now().isoformat(),
            'source_path': str(file_path.absolute())
        }
        
        # Try to extract additional metadata based on file type
        if file_path.suffix.lower() == '.pdf':
            try:
                import PyPDF2
                with open(filepath, 'rb') as f:
                    reader = PyPDF2.PdfReader(f)
                    metadata['pdf_pages'] = len(reader.pages)
                    if reader.metadata:
                        metadata['pdf_title'] = reader.metadata.get('/Title', '')
                        metadata['pdf_author'] = reader.metadata.get('/Author', '')
            except ImportError:
                metadata['note'] = 'PyPDF2 not available for PDF metadata extraction'
            except Exception as e:
                metadata['pdf_error'] = str(e)
        
        return metadata
    
    def upload_file(self, filepath: str, custom_metadata: Dict = None) -> tuple[bool, str, str]:
        """Upload a file to the intake system."""
        # Validate file
        is_valid, message = self.validate_file(filepath)
        if not is_valid:
            return False, message, ""
        
        try:
            # Generate unique filename
            original_filename = Path(filepath).name
            unique_filename = self.generate_unique_filename(original_filename)
            destination = self.intake_pending / unique_filename
            
            # Copy file to intake directory
            shutil.copy2(filepath, destination)
            
            # Extract metadata
            metadata = self.extract_metadata(filepath)
            if custom_metadata:
                metadata.update(custom_metadata)
            
            # Register with workflow manager
            self.workflow_manager.register_document(str(destination), metadata)
            
            print(f"✓ Uploaded: {original_filename} → {unique_filename}")
            print(f"  Location: {destination}")
            print(f"  Size: {metadata['file_size_bytes'] / 1024:.1f} KB")
            
            return True, f"File uploaded successfully as {unique_filename}", unique_filename
            
        except Exception as e:
            error_msg = f"Upload failed: {e}"
            print(f"✗ {error_msg}")
            return False, error_msg, ""
    
    def upload_multiple_files(self, filepaths: List[str], 
                            custom_metadata: Dict = None) -> Dict[str, tuple[bool, str, str]]:
        """Upload multiple files at once."""
        results = {}
        
        print(f"Uploading {len(filepaths)} files...")
        
        for filepath in filepaths:
            print(f"\nProcessing: {Path(filepath).name}")
            success, message, filename = self.upload_file(filepath, custom_metadata)
            results[filepath] = (success, message, filename)
        
        # Summary
        successful = sum(1 for success, _, _ in results.values() if success)
        print(f"\n=== Upload Summary ===")
        print(f"Total files: {len(filepaths)}")
        print(f"Successful: {successful}")
        print(f"Failed: {len(filepaths) - successful}")
        
        return results
    
    def list_pending_files(self) -> List[str]:
        """List files currently in pending state."""
        pending_files = []
        if self.intake_pending.exists():
            for file_path in self.intake_pending.iterdir():
                if file_path.is_file():
                    pending_files.append(file_path.name)
        return sorted(pending_files)
    
    def trigger_ai_processing(self, filename: str = None) -> bool:
        """Trigger AI processing for uploaded files."""
        try:
            # Import here to avoid circular imports
            sys.path.append(str(self.base_path / "ai_agents"))
            
            if filename:
                # Process specific file
                print(f"Triggering AI processing for: {filename}")
                # This would call the AI extraction agent
                # For now, just move to processing state
                return self.workflow_manager.move_document(
                    filename, WorkflowState.PENDING, WorkflowState.PROCESSING
                )
            else:
                # Process all pending files
                pending_files = self.workflow_manager.get_next_documents_for_processing(
                    WorkflowState.PENDING
                )
                
                if not pending_files:
                    print("No pending files to process")
                    return True
                
                print(f"Triggering AI processing for {len(pending_files)} files...")
                success_count = 0
                
                for file in pending_files:
                    if self.workflow_manager.move_document(
                        file, WorkflowState.PENDING, WorkflowState.PROCESSING
                    ):
                        success_count += 1
                
                print(f"✓ Moved {success_count}/{len(pending_files)} files to processing")
                return success_count == len(pending_files)
                
        except Exception as e:
            print(f"Error triggering AI processing: {e}")
            return False


def main():
    """Command line interface for document upload."""
    parser = argparse.ArgumentParser(
        description='Upload grant documents for AI processing',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Upload a single file
  python3 upload_grant_documents.py --file grant_proposal.pdf
  
  # Upload multiple files
  python3 upload_grant_documents.py --file file1.pdf --file file2.docx
  
  # Upload with custom metadata
  python3 upload_grant_documents.py --file grant.pdf --agency "NSF" --year "2024"
  
  # List pending files
  python3 upload_grant_documents.py --list-pending
  
  # Trigger AI processing
  python3 upload_grant_documents.py --process-all
        """
    )
    
    parser.add_argument('--file', action='append', 
                       help='File to upload (can be used multiple times)')
    parser.add_argument('--agency', help='Funding agency (optional metadata)')
    parser.add_argument('--year', help='Grant year (optional metadata)')
    parser.add_argument('--type', help='Grant type (optional metadata)')
    parser.add_argument('--list-pending', action='store_true',
                       help='List files in pending state')
    parser.add_argument('--process-all', action='store_true',
                       help='Trigger AI processing for all pending files')
    parser.add_argument('--process-file', 
                       help='Trigger AI processing for specific file')
    
    args = parser.parse_args()
    
    # Initialize uploader
    uploader = DocumentUploader()
    
    if args.list_pending:
        pending_files = uploader.list_pending_files()
        if pending_files:
            print("Pending files:")
            for filename in pending_files:
                print(f"  {filename}")
        else:
            print("No pending files")
        return
    
    if args.process_all:
        uploader.trigger_ai_processing()
        return
    
    if args.process_file:
        uploader.trigger_ai_processing(args.process_file)
        return
    
    if not args.file:
        print("Error: No files specified. Use --file or see --help")
        sys.exit(1)
    
    # Prepare custom metadata
    custom_metadata = {}
    if args.agency:
        custom_metadata['funding_agency'] = args.agency
    if args.year:
        custom_metadata['grant_year'] = args.year
    if args.type:
        custom_metadata['grant_type'] = args.type
    
    # Upload files
    results = uploader.upload_multiple_files(args.file, custom_metadata)
    
    # Check for failures
    failed_files = [filepath for filepath, (success, _, _) in results.items() if not success]
    if failed_files:
        print(f"\nFailed uploads:")
        for filepath in failed_files:
            _, message, _ = results[filepath]
            print(f"  {Path(filepath).name}: {message}")
        sys.exit(1)
    
    # Ask if user wants to trigger processing
    if len(results) > 0:
        response = input("\nTrigger AI processing now? (y/n): ").strip().lower()
        if response in ['y', 'yes']:
            uploader.trigger_ai_processing()


if __name__ == '__main__':
    main()