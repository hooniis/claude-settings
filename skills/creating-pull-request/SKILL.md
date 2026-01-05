---
name: creating-pull-request
description: Creates a GitHub pull request with Jira ticket integration. Analyzes commits, extracts Jira info from branch name, and asks for user confirmation before creating PR. Use when user wants to create a pull request.
---

# Creating Pull Request

$ARGUMENTS

## Instructions

1. **Analyze current branch and commits**
   - Run `git branch --show-current` to get current branch name
   - Run `git log main..HEAD --oneline` to see commits to be included
   - Run `git diff main..HEAD --stat` to see changed files

2. **Extract Jira ticket (if applicable)**
   - Parse branch name for ticket pattern: `feature/PROJ-123-*`, `bugfix/PROJ-123-*`
   - Use `mcp__mcp-atlassian__jira_get_issue` to fetch ticket details if found
   - Include ticket summary in PR description

3. **Draft PR content**
   - Generate title from commits or Jira ticket
   - Create description with summary, changes, and Jira link

4. **Ask user to confirm before creating**
   - Show complete PR content (title, description, files changed)
   - Use `AskUserQuestion` tool to select target branch and get approval
   - Common target options: `main`, `develop`, `release/*`, or custom branch
   - Allow user to edit or cancel

5. **Create the pull request**
   - Use `gh pr create` command with confirmed content
   - Return the PR URL to user

---

## PR Title Format

```
<type>(<scope>): <description> [TICKET-123]
```

Examples:
- `feat(auth): add OAuth2 login support [PROJ-123]`
- `fix(cart): resolve quantity update issue [PROJ-456]`
- `refactor(api): extract validation logic`

---

## PR Description Template

```markdown
## Summary

[Brief description of changes - 1-3 sentences]

## Jira Ticket

- **Ticket**: [PROJ-123](https://your-jira.atlassian.net/browse/PROJ-123)
- **Summary**: [Ticket summary from Jira]

## Changes

- [List of main changes]
- [Organized by category if needed]

## Test Plan

- [ ] [How to test these changes]
- [ ] [Any specific test scenarios]

---

> If your pull request relates to any existing issues, please reference them by using the issue number prefixed with #.
```

---

## Pre-Creation Confirmation

**IMPORTANT: Use `AskUserQuestion` tool to confirm PR and select target branch**

Show the user:
- PR title
- PR description (full content)
- Source branch and files changed summary
- Target branch selection

### Example Output Before Asking

```markdown
## PR Preview

**Title:** feat(auth): add OAuth2 login [PROJ-123]

**Source Branch:** feature/PROJ-123-add-oauth
**Commits:** 3 commits
**Files Changed:** 5 files (+120, -30)

**Description:**
[Full PR description here]
```

### AskUserQuestion Options

Use `AskUserQuestion` with target branch options:
- `main` - create PR to main branch
- `develop` - create PR to develop branch
- `release/*` - create PR to release branch (specify version)
- `Edit` - modify PR content
- `Cancel` - abort PR creation

---

## Examples

### Example 1: Feature with Jira Ticket

**Branch:** `feature/PROJ-123-add-user-auth`
**Jira Summary:** "Add user authentication feature"

**Generated PR:**
```
Title: feat(auth): add user authentication [PROJ-123]

## Summary

Implement user authentication with JWT tokens and session management.

## Jira Ticket

- **Ticket**: [PROJ-123](https://jira.example.com/browse/PROJ-123)
- **Summary**: Add user authentication feature

## Changes

- Add JWT token generation and validation
- Implement login/logout endpoints
- Add session middleware

## Test Plan

- [ ] Test login with valid credentials
- [ ] Test login with invalid credentials
- [ ] Verify JWT token expiration
```

### Example 2: Bug Fix

**Branch:** `bugfix/PROJ-456-fix-cart-update`

**Generated PR:**
```
Title: fix(cart): resolve quantity update race condition [PROJ-456]

## Summary

Fix race condition when multiple quantity updates occur simultaneously.

## Jira Ticket

- **Ticket**: [PROJ-456](https://jira.example.com/browse/PROJ-456)
- **Summary**: Cart quantity not updating correctly

## Changes

- Add optimistic locking to cart updates
- Implement retry logic for concurrent modifications

## Test Plan

- [ ] Test rapid quantity button clicks
- [ ] Verify final quantity matches expected value
```

---

## Git Commands Reference

```bash
# Check current branch
git branch --show-current

# See commits to include
git log main..HEAD --oneline

# See file changes
git diff main..HEAD --stat

# Create PR with gh cli
gh pr create --base <target> --title "<title>" --body "<body>"
```
