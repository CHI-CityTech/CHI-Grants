#!/usr/bin/env python3
"""
Grant Information Automation Script
This script helps automate the creation of grant information files in the CHI-Grants repository.
"""

import os
import sys
from datetime import datetime
import argparse
import re


def sanitize_filename(name):
    """Convert grant name to a valid filename."""
    # Remove special characters and replace spaces with underscores
    name = re.sub(r'[^\w\s-]', '', name)
    name = re.sub(r'[-\s]+', '_', name)
    return name.lower()


def create_grant_file(grant_id, grant_name, funding_agency, award_amount, grant_type,
                      pi_name, output_dir='grants'):
    """Create a new grant information file from template."""
    
    template_path = os.path.join(os.path.dirname(__file__), '..', 'templates', 'grant_template.md')
    
    # Read template
    try:
        with open(template_path, 'r') as f:
            template = f.read()
    except FileNotFoundError:
        print(f"Error: Template file not found at {template_path}")
        sys.exit(1)
    
    # Replace placeholders
    current_date = datetime.now().strftime('%Y-%m-%d')
    content = template.replace('[Unique identifier]', grant_id)
    content = content.replace('[Full name of the grant]', grant_name)
    content = content.replace('[Name of the funding organization]', funding_agency)
    # Only replace the main award amount, not budget placeholders
    content = content.replace('- **Award Amount**: $[Amount]', f'- **Award Amount**: ${award_amount}')
    content = content.replace('[Research/Education/Infrastructure/etc.]', grant_type)
    content = content.replace('[Name]', pi_name)
    content = content.replace('[YYYY-MM-DD]', current_date)
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate filename
    filename = f"{grant_id}_{sanitize_filename(grant_name)}.md"
    filepath = os.path.join(output_dir, filename)
    
    # Write file
    with open(filepath, 'w') as f:
        f.write(content)
    
    print(f"✓ Grant file created successfully: {filepath}")
    return filepath


def main():
    parser = argparse.ArgumentParser(
        description='Automate grant information file creation',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode (prompts for all information)
  python3 add_grant.py
  
  # Command line mode with all parameters
  python3 add_grant.py --id NSF-2024-001 --name "AI Research Initiative" \\
    --agency "National Science Foundation" --amount 500000 \\
    --type Research --pi "Dr. Jane Smith"
        """
    )
    
    parser.add_argument('--id', help='Grant ID (e.g., NSF-2024-001)')
    parser.add_argument('--name', help='Grant name')
    parser.add_argument('--agency', help='Funding agency')
    parser.add_argument('--amount', help='Award amount (without $ sign)')
    parser.add_argument('--type', help='Grant type (Research/Education/Infrastructure/etc.)')
    parser.add_argument('--pi', help='Principal Investigator name')
    parser.add_argument('--output-dir', default='grants', help='Output directory (default: grants)')
    
    args = parser.parse_args()
    
    # Interactive mode if no arguments provided
    if not args.id:
        print("=== Grant Information Entry ===\n")
        grant_id = input("Grant ID: ").strip()
        grant_name = input("Grant Name: ").strip()
        funding_agency = input("Funding Agency: ").strip()
        award_amount = input("Award Amount (without $ sign): ").strip()
        grant_type = input("Grant Type (Research/Education/Infrastructure/etc.): ").strip()
        pi_name = input("Principal Investigator Name: ").strip()
    else:
        # Use command line arguments
        if not all([args.id, args.name, args.agency, args.amount, args.type, args.pi]):
            parser.error("All parameters required: --id, --name, --agency, --amount, --type, --pi")
        
        grant_id = args.id
        grant_name = args.name
        funding_agency = args.agency
        award_amount = args.amount
        grant_type = args.type
        pi_name = args.pi
    
    # Validate inputs
    if not all([grant_id, grant_name, funding_agency, award_amount, grant_type, pi_name]):
        print("Error: All fields are required!")
        sys.exit(1)
    
    # Create the grant file
    filepath = create_grant_file(
        grant_id=grant_id,
        grant_name=grant_name,
        funding_agency=funding_agency,
        award_amount=award_amount,
        grant_type=grant_type,
        pi_name=pi_name,
        output_dir=args.output_dir
    )
    
    print(f"\nNext steps:")
    print(f"1. Edit {filepath} to add more details")
    print(f"2. Commit the changes: git add {filepath} && git commit -m 'Add grant: {grant_name}'")
    print(f"3. Push to repository: git push")


if __name__ == '__main__':
    main()
