---
name: creating-branch-from-jira
description: Creates a git feature branch based on a Jira ticket. Fetches ticket info using jira_get_issue tool and creates branch with format feature/{ticket-number}-{short-name}. Use when user wants to start work on a Jira ticket.
---

# Creating Branch from Jira Ticket

$ARGUMENTS

## Instructions

1. **Get Jira ticket information**
   - Use `mcp__mcp-atlassian__jira_get_issue` tool to fetch the ticket details
   - Extract the issue key (e.g., `PROJ-123`) and summary

2. **Generate branch name**
   - Format: `feature/{issue-key}-{short-name}`
   - Convert the summary to a short, kebab-case name (2-4 words max)
   - Remove special characters and Korean text
   - Use only lowercase letters, numbers, and hyphens

3. **Create the branch**
   - Run `git checkout -b {branch-name}` to create and switch to the new branch
   - Confirm the branch was created successfully

## Branch Naming Rules

| Element | Rule | Example |
|---------|------|---------|
| Prefix | Always `feature/` | `feature/` |
| Issue Key | Uppercase, as-is from Jira | `PROJ-123` |
| Short Name | Kebab-case, 2-4 words, lowercase | `add-user-auth` |

### Short Name Generation

- Extract key nouns/verbs from the summary
- Remove articles (a, an, the), prepositions, Korean text
- Keep it concise and descriptive
- Max 30 characters for the short name part

## Examples

### Example 1: English Summary

**Jira Ticket**: `DEV-456`
**Summary**: "Add user authentication feature"

**Generated Branch**: `feature/DEV-456-add-user-auth`

### Example 2: Korean Summary

**Jira Ticket**: `PROJ-789`
**Summary**: "로그인 기능 구현"

**Generated Branch**: `feature/PROJ-789-login-feature`

### Example 3: Long Summary

**Jira Ticket**: `API-101`
**Summary**: "Implement REST API endpoint for fetching user profile data with pagination support"

**Generated Branch**: `feature/API-101-user-profile-api`

## Output Format

```
Jira Ticket: {issue-key}
Summary: {summary}

Branch created: feature/{issue-key}-{short-name}
```
