# Commit Message Template

Based on [Conventional Commits v1.0.0](https://www.conventionalcommits.org/en/v1.0.0/)

---

## Format

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

---

## Type (Required)

| Type | Description | SemVer |
|------|-------------|--------|
| `feat` | Introduces a new feature | MINOR |
| `fix` | Patches a bug | PATCH |
| `docs` | Documentation only changes | - |
| `style` | Code style (formatting, semicolons, etc.) | - |
| `refactor` | Code change that neither fixes nor adds | - |
| `perf` | Performance improvement | - |
| `test` | Adding or updating tests | - |
| `build` | Build system or external dependencies | - |
| `ci` | CI/CD configuration | - |
| `chore` | Other changes that don't modify src/test | - |
| `revert` | Reverts a previous commit | - |

---

## Scope (Optional)

Provides contextual information about what section of the codebase changed.

```
feat(parser): add ability to parse arrays
fix(api): handle null response
docs(readme): update installation guide
```

---

## Description (Required)

- Use imperative mood: "add" not "added" or "adds"
- Don't capitalize the first letter
- No period at the end
- Concise summary of the change

---

## Body (Optional)

- Explain **what** and **why**, not how
- Separate from description with a blank line
- Can be multiple paragraphs

---

## Footer (Optional)

Footers follow git trailer format: `token: value` or `token #value`

| Token | Description |
|-------|-------------|
| `BREAKING CHANGE` | Indicates breaking API change (MAJOR version) |
| `Fixes` | References fixed issue |
| `Closes` | References closed issue |
| `Refs` | References related issues |
| `Reviewed-by` | Reviewer attribution |
| `Co-authored-by` | Co-author attribution |

---

## Breaking Changes

Two ways to indicate breaking changes:

### 1. Using `!` after type/scope
```
feat!: send email to customer when product ships

feat(api)!: change response format for user endpoint
```

### 2. Using footer
```
feat: allow config object to extend other configs

BREAKING CHANGE: `extends` key in config file is now used for
extending other config files.
```

Both methods result in a **MAJOR** version bump.

---

## Examples

### Simple commit
```
feat(auth): add login with Google OAuth
```

### Commit with body
```
fix(api): handle null response from payment gateway

The payment gateway occasionally returns null instead of an error
response when the service is overloaded. This change adds proper
null checking to prevent NullPointerException.
```

### Commit with body and footer
```
fix(api): prevent racing of requests

Introduce a request id and reference to latest request. Dismiss
incoming responses other than from latest request.

Remove timeouts which were used to mitigate the racing issue but are
obsolete now.

Reviewed-by: Alice
Refs: #123
```

### Breaking change with `!`
```
feat(api)!: send email to customer when product ships
```

### Breaking change with `!` and footer
```
chore!: drop support for Node 6

BREAKING CHANGE: use JavaScript features not available in Node 6.
```

### Breaking change with body and footer
```
feat: allow config object to extend other configs

BREAKING CHANGE: `extends` key in config file is now used for
extending other config files.

Closes #456
```

### Commit with multiple footers
```
fix: prevent racing of requests

Introduce a request id and reference to latest request.

Fixes #123
Reviewed-by: Bob
Co-authored-by: Alice <alice@example.com>
```

### Revert commit
```
revert: let us never again speak of the noodle incident

Refs: 676104e, a]]215868
```

---

## Specification Summary

1. Commits MUST be prefixed with a type (`feat`, `fix`, etc.)
2. Scope MAY be provided after type: `feat(scope): description`
3. Description MUST immediately follow the colon and space after type/scope
4. Body MAY be provided after description, separated by blank line
5. Footer(s) MAY be provided after body, separated by blank line
6. Breaking changes MUST be indicated by `!` before `:` or `BREAKING CHANGE:` footer
7. `BREAKING CHANGE` footer MUST be uppercase
8. Types other than `feat` and `fix` MAY be used

---

## Best Practices

1. **One commit = one logical change**
2. **Write meaningful messages** - Future you will thank present you
3. **Reference issues** - Maintain traceability
4. **Keep description concise** - Details go in the body
5. **Use imperative mood** - "add" not "added"
6. **Document breaking changes** - Help consumers understand impact
