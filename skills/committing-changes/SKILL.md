---
name: committing-changes
description: Creates git commits following Conventional Commits format with optional Jira ticket integration. Analyzes changes, drafts commit message, and asks for user confirmation before committing. Use when user asks to commit changes.
---

# Committing Changes

$ARGUMENTS

## Instructions

1. **Analyze changes**
   - Run `git status` to see modified/new files
   - Run `git diff --staged` or `git diff` to understand the changes
   - Identify the type and scope of changes

2. **Extract Jira ticket (if applicable)**
   - Check current branch name for ticket pattern: `feature/TICKET-123-*`, `bugfix/TICKET-123-*`
   - Use regex: `(TICKET|[A-Z]+-\d+)` to extract ticket number

3. **Draft commit message**
   - Follow Conventional Commits format
   - Select appropriate type based on changes
   - Determine scope from affected module/component
   - Write clear, imperative description

4. **Ask user to confirm before committing**
   - Show changed files and proposed commit message
   - Use `AskUserQuestion` tool to get user approval
   - Wait for explicit confirmation before proceeding

5. **Create commit**
   - Stage files if needed
   - Execute git commit with the approved message

---

## Commit Message Format

```
<type>(<scope>): <description> [TICKET-123]

[optional body]

[optional footer(s)]
```

---

## Commit Types

| Type | Description | Example |
|------|-------------|---------|
| `feat` | New feature | `feat(auth): add OAuth2 login` |
| `fix` | Bug fix | `fix(cart): resolve quantity update issue` |
| `docs` | Documentation only | `docs: update API documentation` |
| `style` | Code style (formatting) | `style: apply ktlint formatting` |
| `refactor` | Code refactoring | `refactor(order): extract validation logic` |
| `perf` | Performance improvement | `perf(search): add query caching` |
| `test` | Adding/updating tests | `test(payment): add unit tests` |
| `build` | Build system/dependencies | `build: upgrade Spring Boot to 3.2` |
| `ci` | CI/CD configuration | `ci: add GitHub Actions workflow` |
| `chore` | Other changes | `chore: update .gitignore` |
| `revert` | Reverting a commit | `revert: feat(auth): add OAuth2 login` |

---

## Rules

### Do
- Use imperative mood: "add" not "added" or "adds"
- Keep subject line under 72 characters
- Capitalize first letter of description
- Include Jira ticket when applicable
- Separate subject from body with blank line

### Don't
- End subject line with period
- Use vague messages: "fix bug", "update code"
- Mix multiple changes in one commit

---

## Pre-Commit Confirmation

**IMPORTANT: Always use `AskUserQuestion` tool before committing**

1. Show the user:
   - Changed files list with status (modified/new/deleted)
   - Proposed commit message

2. Use `AskUserQuestion` tool with options like:
   - "Commit" - proceed with the commit
   - "Edit message" - let user modify the message
   - "Cancel" - abort the commit

### Example Output Before Asking

```markdown
**Changed Files:**
- path/to/file1.kt (modified)
- path/to/file2.kt (new file)
- path/to/file3.kt (deleted)

**Commit Message:**
<type>(<scope>): <description> [TICKET-123]

<body if needed>
```

---

## Jira Ticket Integration

### Extract from Branch Name

| Branch Pattern | Extracted Ticket |
|----------------|------------------|
| `feature/PROJ-123-add-feature` | `[PROJ-123]` |
| `bugfix/PROJ-456-fix-bug` | `[PROJ-456]` |
| `hotfix/PROJ-789-urgent` | `[PROJ-789]` |

### Ticket Placement

**In Subject (Preferred)**
```
feat(order): implement cancellation flow [PROJ-123]
```

**In Footer (Alternative)**
```
feat(order): implement cancellation flow

Refs: PROJ-123
```

---

## Examples

### Feature with Jira Ticket

```
feat(flight): add fare search caching [PROJ-123]

Implement Redis caching for fare search results
to reduce external API calls.

- Cache TTL: 5 minutes
- Cache key: origin_destination_date
```

### Bug Fix

```
fix(order): prevent duplicate order creation [PROJ-456]

Add idempotency check using order reference ID.
```

### Simple Changes

```
docs: update API documentation

refactor(booking): extract validation logic

test(fare): add unit tests for price calculator

chore: update gradle dependencies
```

### Breaking Change

```
feat(api)!: change response format for v2 [PROJ-789]

BREAKING CHANGE: Response wrapper structure changed.
Old: { data: {...} }
New: { result: {...}, meta: {...} }
```
