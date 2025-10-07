#!/usr/bin/env python3
"""
Workflow Manager for CHI-Grants Multi-State Processing
Handles state transitions and tracks document processing status.
"""

import os
import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class WorkflowState(Enum):
    """Enumeration of workflow states."""
    PENDING = "pending"
    PROCESSING = "processing"
    EXTRACTED = "extracted"
    VALIDATED = "validated"
    APPROVED = "approved"
    COMPLETED = "completed"
    ERROR = "error"


@dataclass
class DocumentInfo:
    """Information about a document in the workflow."""
    filename: str
    original_path: str
    current_state: WorkflowState
    created_at: datetime
    updated_at: datetime
    metadata: Dict
    error_message: Optional[str] = None


class WorkflowManager:
    """Manages grant processing workflow states and transitions."""
    
    def __init__(self, base_path: str = "."):
        """Initialize workflow manager with base repository path."""
        self.base_path = Path(base_path)
        self.intake_path = self.base_path / "intake"
        self.workflows_path = self.base_path / "workflows"
        self.grants_path = self.base_path / "grants"
        
        # State directories
        self.state_dirs = {
            WorkflowState.PENDING: self.intake_path / "pending",
            WorkflowState.PROCESSING: self.intake_path / "processing",
            WorkflowState.EXTRACTED: self.workflows_path / "extracted",
            WorkflowState.VALIDATED: self.workflows_path / "validated",
            WorkflowState.APPROVED: self.workflows_path / "approved",
        }
        
        # Workflow status file
        self.status_file = self.workflows_path / "workflow_status.json"
        
    def get_workflow_status(self) -> Dict[str, DocumentInfo]:
        """Load workflow status from file."""
        if not self.status_file.exists():
            return {}
            
        try:
            with open(self.status_file, 'r') as f:
                status_data = json.load(f)
            
            # Convert back to DocumentInfo objects
            workflow_status = {}
            for filename, data in status_data.items():
                workflow_status[filename] = DocumentInfo(
                    filename=data['filename'],
                    original_path=data['original_path'],
                    current_state=WorkflowState(data['current_state']),
                    created_at=datetime.fromisoformat(data['created_at']),
                    updated_at=datetime.fromisoformat(data['updated_at']),
                    metadata=data['metadata'],
                    error_message=data.get('error_message')
                )
            return workflow_status
        except Exception as e:
            print(f"Warning: Could not load workflow status: {e}")
            return {}
    
    def save_workflow_status(self, workflow_status: Dict[str, DocumentInfo]):
        """Save workflow status to file."""
        # Convert DocumentInfo objects to serializable format
        status_data = {}
        for filename, doc_info in workflow_status.items():
            status_data[filename] = {
                'filename': doc_info.filename,
                'original_path': doc_info.original_path,
                'current_state': doc_info.current_state.value,
                'created_at': doc_info.created_at.isoformat(),
                'updated_at': doc_info.updated_at.isoformat(),
                'metadata': doc_info.metadata,
                'error_message': doc_info.error_message
            }
        
        try:
            with open(self.status_file, 'w') as f:
                json.dump(status_data, f, indent=2)
        except Exception as e:
            print(f"Error saving workflow status: {e}")
    
    def register_document(self, filepath: str, metadata: Dict = None) -> str:
        """Register a new document in the workflow."""
        if metadata is None:
            metadata = {}
            
        filename = Path(filepath).name
        current_time = datetime.now()
        
        # Create document info
        doc_info = DocumentInfo(
            filename=filename,
            original_path=filepath,
            current_state=WorkflowState.PENDING,
            created_at=current_time,
            updated_at=current_time,
            metadata=metadata
        )
        
        # Load existing status and add new document
        workflow_status = self.get_workflow_status()
        workflow_status[filename] = doc_info
        self.save_workflow_status(workflow_status)
        
        print(f"✓ Registered document: {filename}")
        return filename
    
    def transition_state(self, filename: str, new_state: WorkflowState, 
                        error_message: str = None) -> bool:
        """Transition a document to a new workflow state."""
        workflow_status = self.get_workflow_status()
        
        if filename not in workflow_status:
            print(f"Error: Document {filename} not found in workflow")
            return False
        
        doc_info = workflow_status[filename]
        old_state = doc_info.current_state
        
        # Update document info
        doc_info.current_state = new_state
        doc_info.updated_at = datetime.now()
        doc_info.error_message = error_message
        
        # Save updated status
        workflow_status[filename] = doc_info
        self.save_workflow_status(workflow_status)
        
        print(f"✓ Transitioned {filename}: {old_state.value} → {new_state.value}")
        return True
    
    def move_document(self, filename: str, from_state: WorkflowState, 
                     to_state: WorkflowState) -> bool:
        """Move a document file between state directories."""
        try:
            from_dir = self.state_dirs.get(from_state)
            to_dir = self.state_dirs.get(to_state)
            
            if not from_dir or not to_dir:
                print(f"Error: Invalid state transition {from_state} → {to_state}")
                return False
            
            from_path = from_dir / filename
            to_path = to_dir / filename
            
            if not from_path.exists():
                print(f"Error: File {from_path} does not exist")
                return False
            
            # Ensure target directory exists
            to_dir.mkdir(parents=True, exist_ok=True)
            
            # Move the file
            shutil.move(str(from_path), str(to_path))
            
            # Update workflow state
            self.transition_state(filename, to_state)
            
            print(f"✓ Moved {filename} from {from_state.value} to {to_state.value}")
            return True
            
        except Exception as e:
            print(f"Error moving document {filename}: {e}")
            self.transition_state(filename, WorkflowState.ERROR, str(e))
            return False
    
    def list_documents_by_state(self, state: WorkflowState) -> List[DocumentInfo]:
        """Get all documents currently in a specific state."""
        workflow_status = self.get_workflow_status()
        return [doc for doc in workflow_status.values() if doc.current_state == state]
    
    def get_document_info(self, filename: str) -> Optional[DocumentInfo]:
        """Get information about a specific document."""
        workflow_status = self.get_workflow_status()
        return workflow_status.get(filename)
    
    def get_next_documents_for_processing(self, state: WorkflowState, 
                                        limit: int = 10) -> List[str]:
        """Get next documents ready for processing in a given state."""
        documents = self.list_documents_by_state(state)
        # Sort by creation time (oldest first)
        documents.sort(key=lambda x: x.created_at)
        return [doc.filename for doc in documents[:limit]]
    
    def cleanup_error_documents(self):
        """Move error documents back to pending for retry."""
        error_docs = self.list_documents_by_state(WorkflowState.ERROR)
        
        for doc in error_docs:
            print(f"Moving error document {doc.filename} back to pending")
            self.transition_state(doc.filename, WorkflowState.PENDING)
    
    def print_workflow_summary(self):
        """Print a summary of the current workflow status."""
        workflow_status = self.get_workflow_status()
        
        if not workflow_status:
            print("No documents in workflow")
            return
        
        # Count documents by state
        state_counts = {}
        for doc in workflow_status.values():
            state = doc.current_state
            state_counts[state] = state_counts.get(state, 0) + 1
        
        print("\n=== Workflow Summary ===")
        for state in WorkflowState:
            count = state_counts.get(state, 0)
            if count > 0:
                print(f"{state.value.capitalize()}: {count} documents")
        
        # Show recent activity
        recent_docs = sorted(workflow_status.values(), 
                           key=lambda x: x.updated_at, reverse=True)[:5]
        
        if recent_docs:
            print("\n=== Recent Activity ===")
            for doc in recent_docs:
                print(f"{doc.filename}: {doc.current_state.value} "
                      f"(updated: {doc.updated_at.strftime('%Y-%m-%d %H:%M')})")


def main():
    """Command line interface for workflow manager."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Manage grant processing workflow')
    parser.add_argument('--summary', action='store_true', 
                       help='Show workflow summary')
    parser.add_argument('--cleanup-errors', action='store_true',
                       help='Move error documents back to pending')
    parser.add_argument('--list-state', choices=[s.value for s in WorkflowState],
                       help='List documents in specific state')
    
    args = parser.parse_args()
    
    # Initialize workflow manager
    wm = WorkflowManager()
    
    if args.summary:
        wm.print_workflow_summary()
    elif args.cleanup_errors:
        wm.cleanup_error_documents()
        print("✓ Error cleanup completed")
    elif args.list_state:
        state = WorkflowState(args.list_state)
        docs = wm.list_documents_by_state(state)
        print(f"\nDocuments in {state.value} state:")
        for doc in docs:
            print(f"  {doc.filename} (created: {doc.created_at.strftime('%Y-%m-%d %H:%M')})")
    else:
        wm.print_workflow_summary()


if __name__ == '__main__':
    main()