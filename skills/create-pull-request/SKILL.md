---
name: create-pull-request
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

3. **Fetch repository metadata**
   - Run `gh label list` to get available labels
   - Run `gh api repos/{owner}/{repo}/milestones` to get milestones
   - Identify potential reviewers/assignees

4. **Draft PR content**
   - Generate title from commits or Jira ticket
   - Create description with summary, changes, and Jira link

5. **Ask user to confirm PR details**
   - Show drafted title and body
   - Use `AskUserQuestion` tool to select:
     - Target branch (`main`, `develop`, `release/*`)
     - Labels (from repo labels)
     - Assignees
     - Milestone (if available)
   - Allow user to edit or cancel

6. **Create the pull request**
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

**IMPORTANT: Use `AskUserQuestion` tool to confirm PR details**

Show the user:
- PR title
- PR description (full content)
- Source branch and files changed summary
- Available options for selection

### Example Output Before Asking

```markdown
## PR Preview

**Title:** feat(auth): add OAuth2 login [PROJ-123]

**Source Branch:** feature/PROJ-123-add-oauth
**Commits:** 3 commits
**Files Changed:** 5 files (+120, -30)

**Description:**
[Full PR description here]

---

**Available Labels:** bug, enhancement, documentation, feature
**Available Milestones:** v1.0, v1.1, v2.0
```

### AskUserQuestion Options

Use multiple `AskUserQuestion` calls to select:

**1. Target Branch**
- `main` - create PR to main branch
- `develop` - create PR to develop branch
- `release/*` - create PR to release branch

**2. Labels** (multiSelect: true)
- Suggest relevant labels from repo
- Common: `bug`, `enhancement`, `feature`, `documentation`

**3. Assignees**
- `None` - leave unassigned
- `Me` - assign to current user
- Custom - specify username

**4. Milestone** (if available)
- List available milestones from repo
- `None` - no milestone

**5. Final Confirmation**
- `Create PR` - proceed with creation
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

# List available labels
gh label list --json name,description

# List milestones
gh api repos/{owner}/{repo}/milestones --jq '.[].title'

# Create PR with gh cli
gh pr create --base <target> --title "<title>" --body "<body>"

# Create PR with labels, assignee, milestone
gh pr create \
  --base main \
  --title "feat(auth): add OAuth2 login" \
  --body "PR description" \
  --label "enhancement,feature" \
  --assignee "@me" \
  --milestone "v1.0"
```
