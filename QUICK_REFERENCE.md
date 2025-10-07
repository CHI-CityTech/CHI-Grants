# Quick Reference

## Common Commands

### Add a Grant (Interactive)
```bash
python3 scripts/add_grant.py
```

### Add a Grant (Command Line)
```bash
python3 scripts/add_grant.py --id GRANT-ID --name "Grant Name" \
  --agency "Agency" --amount 100000 --type Type --pi "PI Name"
```

### View Help
```bash
python3 scripts/add_grant.py --help
```

### List All Grants
```bash
ls -lh grants/
```

### Search Grants
```bash
# By agency
ls grants/ | grep NSF

# By year
ls grants/ | grep 2024
```

### Edit a Grant
```bash
# Use your preferred editor
nano grants/GRANT-ID_name.md
vim grants/GRANT-ID_name.md
code grants/GRANT-ID_name.md
```

## Grant ID Format
`AGENCY-YEAR-NUMBER`
- Examples: `NSF-2024-001`, `NIH-2025-012`

## Grant Types
- Research
- Education
- Infrastructure
- Training
- Equipment
- Collaborative

## Workflow
1. Run `python3 scripts/add_grant.py`
2. Enter basic information
3. Edit the generated file to add details
4. Commit: `git add grants/... && git commit -m "..."`
5. Push: `git push`

## File Locations
- **Grants**: `grants/`
- **Templates**: `templates/`
- **Scripts**: `scripts/`
- **Documentation**: `README.md`, `USAGE_GUIDE.md`
