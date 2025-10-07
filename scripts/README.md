# Grant Automation Scripts

This directory contains automation scripts for managing grant information in the CHI-Grants repository.

## Available Scripts

### add_grant.py

Automates the creation of grant information files from the standard template.

**Features:**
- Interactive and command-line modes
- Automatic filename generation
- Template-based file creation
- Input validation
- Helpful usage instructions

**Usage:**

Interactive mode:
```bash
python3 add_grant.py
```

Command line mode:
```bash
python3 add_grant.py --id GRANT-ID --name "Grant Name" --agency "Agency Name" \
  --amount AMOUNT --type TYPE --pi "PI Name"
```

**Arguments:**
- `--id`: Grant ID (e.g., NSF-2024-001)
- `--name`: Full name of the grant
- `--agency`: Funding agency name
- `--amount`: Award amount (numeric, without $ sign)
- `--type`: Grant type (Research/Education/Infrastructure/etc.)
- `--pi`: Principal Investigator name
- `--output-dir`: Output directory (default: grants)

**Examples:**

```bash
# Research grant
python3 add_grant.py --id NSF-2024-001 --name "Machine Learning Research" \
  --agency "National Science Foundation" --amount 500000 \
  --type Research --pi "Dr. Alice Johnson"

# Education grant
python3 add_grant.py --id DOE-2024-100 --name "STEM Education Initiative" \
  --agency "Department of Education" --amount 250000 \
  --type Education --pi "Dr. Bob Williams"
```

## Requirements

- Python 3.6 or higher
- No external dependencies (uses only Python standard library)

## Adding New Scripts

When adding new automation scripts:
1. Follow Python best practices
2. Include comprehensive documentation
3. Add usage examples
4. Update this README
