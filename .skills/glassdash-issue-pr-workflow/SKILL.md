---
name: glassdash-issue-pr-workflow
description: Use when asked to make code changes to the GlassDash repository
---

# GlassDash Issue/PR Workflow

## Overview

Every code change must follow this workflow: create issue → create branch → work → PR.

## Workflow Steps

### 1. Create Issue (Before Any Code)

When asked to make code changes, create a GitHub issue first:

```bash
gh issue create \
  --title "Brief description of the change" \
  --body "Detailed description of what needs to be done" \
  --repo owner/repo
```

Issue should describe:
- What problem is being solved
- What the expected outcome is
- Any relevant context

### 2. Create Branch Linked to Issue

Create a new branch for the work:

```bash
# Create branch from main
git checkout main
git pull origin main

# Create branch with descriptive name
git checkout -b feat/123-short-description

# Or use issue number in branch name
git checkout -b fix-issue-123
```

### 3. Verify Branch is Up-to-Date

```bash
git status
git log --oneline -3  # Verify you're on correct branch
git pull origin main  # Ensure main is up to date
```

### 4. Make Code Changes

Implement the changes following project conventions:
- Follow existing code patterns
- Add tests for new functionality
- Update documentation if needed

### 5. Commit Changes

```bash
git add .
git commit -m "feat|fix|test|docs|ci|refactor: brief description

- Detailed bullet points of changes
- Reference issue: closes #123"
```

Commit types: `feat`, `fix`, `test`, `docs`, `ci`, `refactor`, `chore`

### 6. Push Branch

```bash
git push -u origin HEAD
```

### 7. Create PR

```bash
gh pr create \
  --title "feat|fix|ci: brief description" \
  --body "$(cat <<'EOF'
## Summary
Brief description of changes

## Changes
- Change 1
- Change 2

## Testing
How was this tested?

## Checklist
- [ ] Tests pass
- [ ] Code follows project conventions
- [ ] Documentation updated (if applicable)
EOF
)" \
  --base main
```

## Quick Reference

| Action | Command |
|--------|---------|
| Create issue | `gh issue create --title "..." --body "..."` |
| Create branch | `git checkout -b feat/description` |
| Verify branch | `git status && git log --oneline -1` |
| Commit | `git commit -m "type: description"` |
| Push | `git push -u origin HEAD` |
| Create PR | `gh pr create --title "..." --body "..." --base main` |

## Anti-Patterns

**Never:**
- Make code changes without an issue first
- Work directly on main branch
- Push changes without a PR
- Skip tests before creating PR
- Force push to main/master
