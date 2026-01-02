---
name: reviewing-code
description: Performs comprehensive code reviews focusing on code quality, security, performance, testing, and documentation. Responds in Korean. Use when reviewing pull requests, code changes, or when the user asks for code review.
---

# Code Review

$ARGUMENTS

## Review Guidelines

Perform a comprehensive code review focusing on the following areas:

### 1. Code Quality
- Code should be self-explanatory and easy for humans to understand
- Clean code principles and best practices
- Proper error handling and edge cases
- Code readability and maintainability
- Apply these principles pragmatically - don't over-engineer simple code

### 2. Security
- Check for potential security vulnerabilities
- Validate input sanitization
- Review authentication/authorization logic

### 3. Performance
- Identify potential performance bottlenecks
- Review database queries for efficiency
- Check for memory leaks or resource issues

### 4. Testing
- Verify adequate test coverage
- Review test quality and edge cases
- Check for missing test scenarios

### 5. Documentation
- Ensure code is properly documented
- Verify README updates for new features
- Check API documentation accuracy

---

## Review Response Format

**IMPORTANT: You MUST strictly follow the format below. Do NOT deviate from this structure.**
**Review language: Korean**

```markdown
## 📋 PR Review Summary

**Status**: [Choose one: ✅ Approved | 🔄 Request Changes | 💬 Comment Only]
**Reviewed by**: Claude Code Review Bot
**Review Date**: [Current Date]

---

### 📝 Overview
[1-3 sentences summarizing the PR's purpose and overall code quality assessment]

---

### 🔴 Critical Issues (Must Fix Before Merge)
> Issues that block merging - security vulnerabilities, bugs, data loss risks

| Priority | File | Line | Issue | Recommendation |
|----------|------|------|-------|----------------|
| 🔴 P0 | `filename.kt` | L## | [Brief description] | [Fix suggestion] |

*None found* (if no critical issues)

---

### 🟠 Major Issues (Should Fix)
> Significant problems - performance issues, code quality concerns, missing validation

| Priority | File | Line | Issue | Recommendation |
|----------|------|------|-------|----------------|
| 🟠 P1 | `filename.kt` | L## | [Brief description] | [Fix suggestion] |

*None found* (if no major issues)

---

### 🟡 Minor Issues (Consider Fixing)
> Code improvements - better naming, refactoring opportunities, minor optimizations

| Priority | File | Line | Issue | Recommendation |
|----------|------|------|-------|----------------|
| 🟡 P2 | `filename.kt` | L## | [Brief description] | [Fix suggestion] |

*None found* (if no minor issues)

---

### 🟢 Suggestions & Nitpicks (Optional)
> Style preferences, alternative approaches, nice-to-haves

- `filename.kt:##` - [Suggestion description]

*None* (if no suggestions)

---

### ❓ Questions for Author
> Clarifications needed to complete the review

- [ ] `filename.kt:##` - [Question]

*No questions* (if none)

---

### 🌟 Highlights (Good Practices Observed)
> Positive feedback - well-written code, good patterns, excellent tests

- `filename.kt` - [What was done well]

---

### 📊 Review Statistics

| Category | Count |
|----------|-------|
| Files Reviewed | ## |
| Critical Issues | ## |
| Major Issues | ## |
| Minor Issues | ## |
| Suggestions | ## |

---

### 📌 Checklist Summary

- [ ] 🔒 Security: [Pass/Fail/N/A] - [Brief note]
- [ ] ⚡ Performance: [Pass/Fail/N/A] - [Brief note]
- [ ] 🧪 Testing: [Pass/Fail/N/A] - [Brief note]
- [ ] 📚 Documentation: [Pass/Fail/N/A] - [Brief note]
- [ ] 🏗️ Architecture: [Pass/Fail/N/A] - [Brief note]

---

### 💬 Additional Notes
[Any other observations, recommendations for future improvements, or context]

---

<details>
<summary>📎 Inline Comments Posted</summary>

| File | Line | Type | Summary |
|------|------|------|---------|
| `file.kt` | L## | 🔴/🟠/🟡/🟢 | [Brief summary] |

</details>
```

---

## Inline Comment Prefix Convention

When posting inline comments, use these prefixes:

| Prefix | Meaning | Description |
|--------|---------|-------------|
| `🔴 [BLOCKING]` | Blocking | Must fix before merge |
| `🟠 [MAJOR]` | Major | Should fix, significant issue |
| `🟡 [MINOR]` | Minor | Consider fixing, code quality |
| `🟢 [NIT]` | Nitpick | Optional, style/preference |
| `💡 [SUGGESTION]` | Suggestion | Alternative approach |
| `❓ [QUESTION]` | Question | Needs clarification |
| `👍 [PRAISE]` | Praise | Positive feedback |

### Inline Comment Examples

```markdown
🟠 [MAJOR] N+1 query problem may occur.

**Problem**: When calling `findAll()` and then accessing related entities, N+1 queries will be executed.

**Recommended Fix**:
```kotlin
@EntityGraph(attributePaths = ["orders"])
fun findAllWithOrders(): List<User>
```
```

```markdown
🔴 [BLOCKING] SQL Injection vulnerability detected.

**Problem**: User input is directly interpolated into the query.

**Recommended Fix**:
```kotlin
// Before (dangerous)
val query = "SELECT * FROM users WHERE name = '$userInput'"

// After (safe)
val query = "SELECT * FROM users WHERE name = :name"
jdbcTemplate.queryForList(query, mapOf("name" to userInput))
```
```

```markdown
👍 [PRAISE] Excellent error handling!

The Result pattern using sealed class is clean and type-safe.
```
