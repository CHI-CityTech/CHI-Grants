# Contributing to CHI-Grants

Thank you for your interest in contributing to the CHI-Grants repository! This guide will help you understand how to contribute effectively.

## Table of Contents
- [Code of Conduct](#code-of-conduct)
- [How to Contribute](#how-to-contribute)
- [Submitting Grant Proposals](#submitting-grant-proposals)
- [Improving Documentation](#improving-documentation)
- [Enhancing Automation](#enhancing-automation)
- [Development Guidelines](#development-guidelines)

## Code of Conduct

We are committed to providing a welcoming and inclusive environment. Please:
- Be respectful and professional
- Focus on constructive feedback
- Support fellow contributors
- Follow CHI community guidelines

## How to Contribute

### Types of Contributions

1. **Grant Proposals** - Submit new grant applications
2. **Documentation** - Improve guides and templates
3. **Automation** - Enhance workflows and scripts
4. **Templates** - Create or improve proposal templates
5. **Bug Reports** - Report issues with automation
6. **Feature Requests** - Suggest improvements

## Submitting Grant Proposals

### Process
1. Review [Submission Guidelines](docs/SUBMISSION_GUIDELINES.md)
2. Use the [Grant Template](proposals/templates/GRANT_TEMPLATE.md)
3. Create a Grant Proposal Issue
4. Respond to reviewer feedback
5. Revise as needed

### Requirements
- Complete all template sections
- Provide budget justification
- Demonstrate CHI alignment
- Include team qualifications
- Attach supporting documents

## Improving Documentation

We welcome documentation improvements!

### What to Document
- Grant writing best practices
- CHI integration examples
- Workflow usage guides
- FAQ entries
- Troubleshooting tips

### Documentation Standards
- Use clear, concise language
- Include examples where helpful
- Keep formatting consistent
- Test all code snippets
- Add table of contents for long docs

### How to Submit
1. Fork the repository
2. Create a feature branch: `git checkout -b docs/improve-submission-guide`
3. Make your changes
4. Submit a Pull Request
5. Address review feedback

## Enhancing Automation

### Workflow Improvements
We use GitHub Actions for automation. Contributions could include:
- Improving grant processing workflows
- Adding notification systems
- Enhancing repository creation
- Building reporting tools

### Script Contributions
- Follow shell scripting best practices
- Add error handling
- Include usage documentation
- Test thoroughly

### Before Submitting
1. Test in a fork first
2. Document what the automation does
3. Include error handling
4. Add usage examples

## Development Guidelines

### Git Workflow

1. **Fork the Repository**
   ```bash
   # Click "Fork" on GitHub
   git clone https://github.com/YOUR-USERNAME/CHI-Grants.git
   cd CHI-Grants
   ```

2. **Create a Branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bug-fix
   # or
   git checkout -b docs/your-doc-improvement
   ```

3. **Make Changes**
   - Write clear, focused commits
   - Follow existing code style
   - Update documentation as needed

4. **Commit Changes**
   ```bash
   git add .
   git commit -m "Clear, descriptive commit message"
   ```

5. **Push to Fork**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create Pull Request**
   - Go to GitHub and create PR
   - Fill in PR template
   - Link related issues
   - Request review

### Commit Message Guidelines

Format: `type(scope): subject`

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks

**Examples:**
```
feat(automation): add email notifications for approved grants
fix(workflow): correct label trigger for repository creation
docs(readme): add section on grant categories
chore(scripts): update repository creation script permissions
```

### Pull Request Guidelines

**Good PR Practices:**
- Keep changes focused and atomic
- Write clear PR description
- Reference related issues
- Update documentation
- Add tests if applicable
- Ensure CI passes

**PR Title Format:**
```
[TYPE] Brief description of changes
```

**Examples:**
- `[FEATURE] Add automated budget validation`
- `[FIX] Correct grant template formatting`
- `[DOCS] Update submission guidelines`

### File Organization

```
CHI-Grants/
├── .github/           # GitHub-specific files
├── proposals/         # Grant proposals
├── scripts/          # Automation scripts
├── docs/             # Documentation
└── README.md         # Main readme
```

Keep files in their appropriate directories.

### Naming Conventions

**Files:**
- Use UPPERCASE for major docs: `README.md`, `CONTRIBUTING.md`
- Use kebab-case for scripts: `create-grant-repo.sh`
- Use SCREAMING_SNAKE_CASE for templates: `GRANT_TEMPLATE.md`

**Branches:**
- `feature/feature-name` - New features
- `fix/bug-description` - Bug fixes
- `docs/doc-improvement` - Documentation
- `refactor/refactor-description` - Refactoring

## Testing Changes

### For Documentation
1. Render markdown locally
2. Check all links work
3. Verify code examples
4. Ensure formatting is correct

### For Scripts
1. Test in isolated environment
2. Verify error handling
3. Check permissions
4. Validate output

### For Workflows
1. Test in fork first
2. Use workflow visualization
3. Check all paths
4. Validate triggers

## Review Process

### What Reviewers Look For
- Code quality and clarity
- Documentation completeness
- Test coverage
- Security considerations
- CHI alignment

### Timeline
- Initial review: 2-3 business days
- Follow-up reviews: 1-2 days
- Merge: After approval

### Addressing Feedback
- Respond to all comments
- Make requested changes
- Push updates to same branch
- Re-request review when ready

## Questions or Problems?

- **General Questions:** Open a Discussion
- **Bug Reports:** Create an Issue
- **Security Issues:** Email security contact (see README)
- **Grant Questions:** Review submission guidelines

## Recognition

Contributors will be recognized in:
- Repository contributors list
- Release notes (for significant contributions)
- Annual CHI reports

## License

By contributing, you agree that your contributions will be licensed under the same license as the project (MIT License for templates and tools).

## Additional Resources

- [GitHub Flow Guide](https://guides.github.com/introduction/flow/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Markdown Guide](https://www.markdownguide.org/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)

---

Thank you for contributing to CHI-Grants! Your contributions help improve grant management for the entire CHI ecosystem. 🎉
