#!/usr/bin/env python3
"""
Interactive Grant Document Uploader
A user-friendly interface for selecting and uploading grant documents.
"""

import os
import sys
from pathlib import Path
from typing import List, Dict, Optional
import subprocess

# Add project paths
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root / "scripts"))

from upload_grant_documents import DocumentUploader


class InteractiveUploader:
    """Interactive file selection and upload interface."""
    
    def __init__(self):
        """Initialize the interactive uploader."""
        self.uploader = DocumentUploader()
        self.selected_files = []
        self.metadata = {}
    
    def clear_screen(self):
        """Clear the terminal screen."""
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def print_header(self):
        """Print the application header."""
        print("=" * 60)
        print("      CHI-Grants Interactive Document Uploader")
        print("=" * 60)
        print()
    
    def get_user_input(self, prompt: str, default: str = "") -> str:
        """Get user input with optional default value."""
        if default:
            full_prompt = f"{prompt} [{default}]: "
        else:
            full_prompt = f"{prompt}: "
        
        user_input = input(full_prompt).strip()
        return user_input if user_input else default
    
    def browse_for_files(self) -> List[str]:
        """Browse and select files for upload."""
        print("File Selection Methods:")
        print("1. Browse current directory")
        print("2. Browse specific directory") 
        print("3. Enter file paths manually")
        print("4. Use drag & drop (paste paths)")
        print()
        
        choice = self.get_user_input("Select method (1-4)", "1")
        
        if choice == "1":
            return self.browse_directory(Path.cwd())
        elif choice == "2":
            path = self.get_user_input("Enter directory path", str(Path.home()))
            return self.browse_directory(Path(path))
        elif choice == "3":
            return self.manual_file_entry()
        elif choice == "4":
            return self.drag_drop_entry()
        else:
            print("Invalid choice. Using current directory.")
            return self.browse_directory(Path.cwd())
    
    def browse_directory(self, directory: Path) -> List[str]:
        """Browse a directory and select files."""
        if not directory.exists() or not directory.is_dir():
            print(f"Error: Directory does not exist: {directory}")
            return []
        
        print(f"\nBrowsing: {directory}")
        print("-" * 50)
        
        # Get all files in directory
        all_files = []
        supported_extensions = {'.pdf', '.docx', '.doc', '.txt', '.md'}
        
        try:
            for item in directory.iterdir():
                if item.is_file() and item.suffix.lower() in supported_extensions:
                    all_files.append(item)
        except PermissionError:
            print(f"Permission denied accessing: {directory}")
            return []
        
        if not all_files:
            print("No supported files found in this directory.")
            print(f"Supported formats: {', '.join(supported_extensions)}")
            return []
        
        # Sort files by name
        all_files.sort(key=lambda x: x.name.lower())
        
        # Display files with numbers
        print("Available files:")
        for i, file_path in enumerate(all_files, 1):
            size_mb = file_path.stat().st_size / (1024 * 1024)
            print(f"{i:2d}. {file_path.name} ({size_mb:.1f} MB)")
        
        print(f"\n{len(all_files)} files found")
        print("Selection options:")
        print("  - Single file: Enter number (e.g., '5')")
        print("  - Multiple files: Enter numbers separated by commas (e.g., '1,3,5')")
        print("  - Range: Enter range with dash (e.g., '1-5')")
        print("  - All files: Enter 'all'")
        print("  - Cancel: Press Enter")
        
        selection = self.get_user_input("\nSelect files").strip()
        
        if not selection:
            return []
        
        selected_files = []
        
        try:
            if selection.lower() == 'all':
                selected_files = [str(f) for f in all_files]
            elif '-' in selection and ',' not in selection:
                # Range selection
                start, end = map(int, selection.split('-'))
                start = max(1, min(start, len(all_files)))
                end = max(start, min(end, len(all_files)))
                selected_files = [str(all_files[i-1]) for i in range(start, end + 1)]
            else:
                # Individual selections
                indices = [int(x.strip()) for x in selection.split(',')]
                for idx in indices:
                    if 1 <= idx <= len(all_files):
                        selected_files.append(str(all_files[idx-1]))
        except ValueError:
            print("Invalid selection format. Please try again.")
            return self.browse_directory(directory)
        
        if selected_files:
            print(f"\nSelected {len(selected_files)} files:")
            for file_path in selected_files:
                print(f"  ✓ {Path(file_path).name}")
        
        return selected_files
    
    def manual_file_entry(self) -> List[str]:
        """Manually enter file paths."""
        print("\nManual File Entry")
        print("-" * 20)
        print("Enter file paths one per line. Press Enter twice when done.")
        print("Tip: Use tab completion or copy/paste full paths")
        print()
        
        files = []
        while True:
            file_path = input(f"File {len(files) + 1}: ").strip()
            if not file_path:
                break
            
            # Expand user path and resolve
            full_path = Path(file_path).expanduser().resolve()
            
            if full_path.exists() and full_path.is_file():
                files.append(str(full_path))
                print(f"  ✓ Added: {full_path.name}")
            else:
                print(f"  ✗ File not found: {file_path}")
                retry = self.get_user_input("Try again? (y/n)", "y").lower()
                if retry in ['y', 'yes']:
                    continue
        
        return files
    
    def drag_drop_entry(self) -> List[str]:
        """Handle drag & drop file paths."""
        print("\nDrag & Drop / Paste Paths")
        print("-" * 25)
        print("Drag files from Finder onto this terminal window,")
        print("or paste file paths separated by spaces or newlines.")
        print("Press Enter twice when done.")
        print()
        
        all_input = []
        while True:
            line = input().strip()
            if not line:
                break
            all_input.append(line)
        
        # Parse input - handle multiple files in one line or multiple lines
        file_paths = []
        for line in all_input:
            # Split by spaces, but preserve quoted paths
            import shlex
            try:
                paths = shlex.split(line)
                file_paths.extend(paths)
            except ValueError:
                # Fallback to simple split if shlex fails
                file_paths.extend(line.split())
        
        # Validate and resolve paths
        valid_files = []
        for path_str in file_paths:
            full_path = Path(path_str).expanduser().resolve()
            if full_path.exists() and full_path.is_file():
                valid_files.append(str(full_path))
                print(f"  ✓ Added: {full_path.name}")
            else:
                print(f"  ✗ File not found: {path_str}")
        
        return valid_files
    
    def preview_files(self, files: List[str]) -> bool:
        """Preview selected files and confirm upload."""
        if not files:
            return False
        
        print(f"\n{'='*60}")
        print(f"PREVIEW: {len(files)} files selected for upload")
        print(f"{'='*60}")
        
        total_size = 0
        valid_files = []
        
        for file_path in files:
            path = Path(file_path)
            if path.exists():
                size = path.stat().st_size
                total_size += size
                
                # Validate file
                is_valid, message = self.uploader.validate_file(file_path)
                status = "✓" if is_valid else "✗"
                
                print(f"{status} {path.name}")
                print(f"    Size: {size / (1024*1024):.1f} MB")
                print(f"    Type: {path.suffix}")
                if not is_valid:
                    print(f"    Error: {message}")
                else:
                    valid_files.append(file_path)
                print()
        
        print(f"Total size: {total_size / (1024*1024):.1f} MB")
        print(f"Valid files: {len(valid_files)}/{len(files)}")
        
        if not valid_files:
            print("No valid files to upload!")
            return False
        
        if len(valid_files) < len(files):
            print(f"\nWarning: {len(files) - len(valid_files)} files will be skipped due to validation errors.")
        
        confirm = self.get_user_input(f"\nProceed with uploading {len(valid_files)} files? (y/n)", "y")
        
        if confirm.lower() in ['y', 'yes']:
            self.selected_files = valid_files
            return True
        
        return False
    
    def collect_metadata(self):
        """Collect optional metadata for the files."""
        print(f"\n{'='*60}")
        print("METADATA (Optional)")
        print(f"{'='*60}")
        print("You can add metadata that will be applied to all uploaded files.")
        print("Leave blank to skip any field.")
        print()
        
        # Collect metadata
        agency = self.get_user_input("Funding Agency (e.g., NSF, NIH, DOE)")
        year = self.get_user_input("Grant Year (e.g., 2024)")
        grant_type = self.get_user_input("Grant Type (e.g., Research, Education)")
        pi_name = self.get_user_input("Principal Investigator")
        
        # Build metadata dictionary
        metadata = {}
        if agency:
            metadata['funding_agency'] = agency
        if year:
            metadata['grant_year'] = year
        if grant_type:
            metadata['grant_type'] = grant_type
        if pi_name:
            metadata['principal_investigator'] = pi_name
        
        self.metadata = metadata
        
        if metadata:
            print("\nMetadata to be added:")
            for key, value in metadata.items():
                print(f"  {key}: {value}")
        else:
            print("\nNo metadata will be added.")
    
    def upload_files(self) -> bool:
        """Upload the selected files."""
        if not self.selected_files:
            return False
        
        print(f"\n{'='*60}")
        print("UPLOADING FILES")
        print(f"{'='*60}")
        
        results = self.uploader.upload_multiple_files(self.selected_files, self.metadata)
        
        # Check results
        successful = sum(1 for success, _, _ in results.values() if success)
        failed = len(results) - successful
        
        print(f"\n{'='*60}")
        print("UPLOAD RESULTS")
        print(f"{'='*60}")
        print(f"Total files: {len(results)}")
        print(f"Successful: {successful}")
        print(f"Failed: {failed}")
        
        if failed > 0:
            print(f"\nFailed uploads:")
            for filepath, (success, message, _) in results.items():
                if not success:
                    print(f"  ✗ {Path(filepath).name}: {message}")
        
        return successful > 0
    
    def offer_ai_processing(self):
        """Offer to trigger AI processing immediately."""
        print(f"\n{'='*60}")
        print("AI PROCESSING")
        print(f"{'='*60}")
        print("Files have been uploaded and are ready for AI processing.")
        print("AI processing will extract grant information from your documents.")
        print()
        
        if not os.getenv('OPENAI_API_KEY'):
            print("⚠️  Note: No OpenAI API key detected.")
            print("   AI processing will run in simulation mode for testing.")
            print("   Set OPENAI_API_KEY environment variable for full AI features.")
            print()
        
        process_now = self.get_user_input("Start AI processing now? (y/n)", "y")
        
        if process_now.lower() in ['y', 'yes']:
            print("\nStarting AI processing...")
            try:
                # Import and run AI processing
                ai_script = project_root / "ai_agents" / "ai_extraction_agent.py"
                result = subprocess.run([
                    sys.executable, str(ai_script), "--process-all"
                ], capture_output=True, text=True, cwd=str(project_root))
                
                if result.returncode == 0:
                    print("✓ AI processing completed successfully!")
                    print("\nTo view results:")
                    print(f"  python3 scripts/workflow_manager.py --summary")
                    print(f"  python3 scripts/workflow_manager.py --list-state extracted")
                else:
                    print("✗ AI processing encountered errors:")
                    print(result.stderr)
                    
            except Exception as e:
                print(f"✗ Error starting AI processing: {e}")
                print("\nYou can run it manually later with:")
                print(f"  python3 ai_agents/ai_extraction_agent.py --process-all")
        else:
            print("\nAI processing skipped. To run it later:")
            print(f"  python3 ai_agents/ai_extraction_agent.py --process-all")
    
    def show_next_steps(self):
        """Show next steps after upload."""
        print(f"\n{'='*60}")
        print("NEXT STEPS")
        print(f"{'='*60}")
        print("Your files have been uploaded to the CHI-Grants system.")
        print()
        print("Available commands:")
        print("  • View workflow status:")
        print("    python3 scripts/workflow_manager.py --summary")
        print()
        print("  • Process with AI:")
        print("    python3 ai_agents/ai_extraction_agent.py --process-all")
        print()
        print("  • Upload more files:")
        print("    python3 scripts/interactive_uploader.py")
        print()
        print("  • View extracted data:")
        print("    python3 scripts/workflow_manager.py --list-state extracted")
        print()
    
    def run(self):
        """Run the interactive uploader."""
        try:
            while True:
                self.clear_screen()
                self.print_header()
                
                # Step 1: File selection
                print("Step 1: Select Files")
                print("-" * 20)
                files = self.browse_for_files()
                
                if not files:
                    print("\nNo files selected.")
                    retry = self.get_user_input("Try again? (y/n)", "y")
                    if retry.lower() not in ['y', 'yes']:
                        break
                    continue
                
                # Step 2: Preview and confirm
                print("\nStep 2: Preview & Confirm")
                print("-" * 25)
                if not self.preview_files(files):
                    continue
                
                # Step 3: Metadata collection
                print("\nStep 3: Add Metadata")
                print("-" * 20)
                self.collect_metadata()
                
                # Step 4: Upload
                print("\nStep 4: Upload")
                print("-" * 15)
                if self.upload_files():
                    # Step 5: Offer AI processing
                    self.offer_ai_processing()
                    
                    # Show next steps
                    self.show_next_steps()
                    
                    # Ask if user wants to upload more files
                    another = self.get_user_input("\nUpload more files? (y/n)", "n")
                    if another.lower() not in ['y', 'yes']:
                        break
                else:
                    print("Upload failed. Please try again.")
                    retry = self.get_user_input("Try again? (y/n)", "y")
                    if retry.lower() not in ['y', 'yes']:
                        break
                        
        except KeyboardInterrupt:
            print("\n\nUpload cancelled by user.")
        except Exception as e:
            print(f"\nUnexpected error: {e}")
            print("Please report this issue.")


def main():
    """Main entry point."""
    print("Initializing CHI-Grants Interactive Uploader...")
    
    # Check if we're in the right directory
    if not (Path.cwd() / "scripts").exists():
        print("Error: Please run this script from the CHI-Grants repository root directory.")
        print(f"Current directory: {Path.cwd()}")
        print("Expected structure: CHI-Grants/scripts/interactive_uploader.py")
        sys.exit(1)
    
    # Initialize and run
    uploader = InteractiveUploader()
    uploader.run()
    
    print("\nThank you for using CHI-Grants Interactive Uploader!")


if __name__ == '__main__':
    main()