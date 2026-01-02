# Pull Request Template

## Format

```markdown
## Summary

[Brief description of what this PR does]

## Type of Change

- [ ] Bug fix (non-breaking change that fixes an issue)
- [ ] New feature (non-breaking change that adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to change)
- [ ] Refactoring (no functional changes)
- [ ] Documentation update
- [ ] CI/CD changes
- [ ] Dependency update

## Related Issues

- Closes #[issue_number]
- Related to #[issue_number]

## Changes Made

- [Change 1]
- [Change 2]
- [Change 3]

## Screenshots (if applicable)

| Before | After |
|--------|-------|
| [screenshot] | [screenshot] |

## Test Plan

- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manual testing performed

### Test Steps

1. [Step 1]
2. [Step 2]
3. [Expected result]

## Checklist

- [ ] My code follows the project's style guidelines
- [ ] I have performed a self-review of my code
- [ ] I have commented my code where necessary
- [ ] I have updated the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix/feature works
- [ ] All new and existing tests pass

## Additional Notes

[Any additional information reviewers should know]
```

---

## Examples

### Feature PR

```markdown
## Summary

Add user profile image upload functionality with S3 storage integration.

## Type of Change

- [ ] Bug fix
- [x] New feature
- [ ] Breaking change
- [ ] Refactoring
- [ ] Documentation update

## Related Issues

- Closes #123
- Related to #100

## Changes Made

- Add `ImageUploadService` for handling file uploads
- Integrate AWS S3 SDK for cloud storage
- Add image validation (size, format, dimensions)
- Create `/api/users/{id}/avatar` endpoint
- Add unit tests for upload service

## Test Plan

- [x] Unit tests added/updated
- [x] Integration tests added/updated
- [x] Manual testing performed

### Test Steps

1. Navigate to user profile settings
2. Click "Upload Photo" button
3. Select an image file (JPG/PNG, max 5MB)
4. Verify image appears in profile

## Checklist

- [x] My code follows the project's style guidelines
- [x] I have performed a self-review of my code
- [x] I have commented my code where necessary
- [x] I have updated the documentation
- [x] My changes generate no new warnings
- [x] I have added tests that prove my fix/feature works
- [x] All new and existing tests pass

## Additional Notes

AWS credentials need to be configured in production environment.
See `docs/s3-setup.md` for configuration details.
```

### Bug Fix PR

```markdown
## Summary

Fix null pointer exception when user has no email address.

## Type of Change

- [x] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Refactoring

## Related Issues

- Fixes #456

## Changes Made

- Add null check for email in `UserService.sendNotification()`
- Add fallback to username when email is missing
- Add test case for users without email

## Test Plan

- [x] Unit tests added/updated
- [ ] Integration tests added/updated
- [x] Manual testing performed

### Test Steps

1. Create a user without email address
2. Trigger notification send
3. Verify no exception is thrown
4. Verify fallback behavior works correctly

## Checklist

- [x] My code follows the project's style guidelines
- [x] I have performed a self-review of my code
- [x] I have added tests that prove my fix works
- [x] All new and existing tests pass
```

### Breaking Change PR

```markdown
## Summary

Migrate authentication from session-based to JWT tokens.

## Type of Change

- [ ] Bug fix
- [ ] New feature
- [x] Breaking change
- [ ] Refactoring

## Related Issues

- Closes #789
- Related to #750, #760

## Changes Made

- Remove session management code
- Implement JWT token generation and validation
- Add refresh token mechanism
- Update all API endpoints to use Bearer authentication
- Add token blacklist for logout functionality

## Breaking Changes

- All clients must update authentication headers
- Session cookies are no longer accepted
- Login response format changed to include `accessToken` and `refreshToken`

### Migration Guide

```kotlin
// Before
headers["Cookie"] = "SESSION=$sessionId"

// After
headers["Authorization"] = "Bearer $accessToken"
```

## Test Plan

- [x] Unit tests added/updated
- [x] Integration tests added/updated
- [x] Manual testing performed
- [x] Load testing performed

## Checklist

- [x] My code follows the project's style guidelines
- [x] I have updated the documentation
- [x] Migration guide is provided
- [x] All new and existing tests pass

## Additional Notes

- Frontend team has been notified of the changes
- Deployment requires coordination with mobile team
- Old sessions will be invalidated after deployment
```

---

## Best Practices

1. **Keep PRs small** - Easier to review, fewer conflicts
2. **One PR = one concern** - Don't mix features with refactoring
3. **Write clear descriptions** - Help reviewers understand context
4. **Link issues** - Maintain traceability
5. **Include test plan** - Show how to verify changes
6. **Add screenshots** - For UI changes
7. **Document breaking changes** - With migration guides
