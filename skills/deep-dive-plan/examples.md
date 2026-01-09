# Deep Dive Planning Examples

Real-world scenarios demonstrating the three-agent planning workflow.

---

## Example 1: Adding JWT Authentication System

### User Request

> "I want to add JWT-based authentication to our Express API. Users should be able to register, login, and access protected routes."

### Workflow Execution

#### Step 1: Analyzer Agent Output

```markdown
## 🔍 Analysis Report

**Request**: Add JWT authentication to Express API

---

### 1. Current State

#### Architecture Overview
- Express 4.18.2 with TypeScript
- REST API with 15 existing endpoints
- MongoDB for data persistence
- No authentication currently - all routes are open

#### Relevant Code Locations
- `src/server.ts:1-50` - Express app setup, middleware chain
- `src/routes/index.ts:10-30` - Route registration
- `src/models/User.ts` - Exists but minimal (id, email, name only)
- `src/middleware/` - Directory exists, only has `errorHandler.ts`

#### Existing Patterns
- Middleware pattern already used for error handling
- Service layer pattern for business logic
- Repository pattern for database access

---

### 2. Dependencies

#### Internal Dependencies
| Component | Relationship | Impact Level |
|-----------|--------------|--------------|
| `User.ts` model | Need to add password field | High |
| All route handlers | Need to add auth middleware | High |
| `errorHandler.ts` | Need to add auth error cases | Medium |

#### External Dependencies
| Package | Version | Purpose | Risk |
|---------|---------|---------|------|
| `jsonwebtoken` | ^9.0.2 | JWT creation/verification | Low - stable |
| `bcrypt` | ^5.1.1 | Password hashing | Low - standard |
| `express-validator` | ^7.0.1 | Input validation | Low - already used |

#### Infrastructure Requirements
- [x] No new infrastructure needed
- [ ] Need JWT_SECRET environment variable
- [ ] Need TOKEN_EXPIRY environment variable

---

### 3. Constraints

#### Technical Constraints
- **TypeScript**: Strict mode enabled - need proper types
- **Performance**: Auth check must be < 10ms
- **Compatibility**: Must work with existing error handling
- **Security**: Must follow OWASP guidelines for password storage

#### Business Constraints
- **Timeline**: User wants this completed in one session
- **Backwards Compatibility**: Existing routes must still work (with auth)
- **User Experience**: Token refresh not needed initially (YAGNI)

---

### 4. Risks Identified

#### 🚨 Critical Risks
1. **Breaking All Existing Routes**
   - **Description**: Adding auth middleware could break all existing endpoints
   - **Impact**: API becomes unusable
   - **Probability**: High if not careful
   - **Mitigation**: Phase implementation - add middleware selectively first

#### ⚠️ High Risks
1. **Password Storage Vulnerability**
   - **Description**: If bcrypt not used correctly, passwords could be compromised
   - **Impact**: Security breach
   - **Probability**: Medium
   - **Mitigation**: Use bcrypt.hash with salt rounds >= 10, review before commit

2. **JWT Secret Management**
   - **Description**: Weak or exposed secret could compromise all tokens
   - **Impact**: Authentication bypass
   - **Probability**: Medium
   - **Mitigation**: Strong secret generation, environment variable only

#### 🔶 Medium Risks
1. **Token Expiry Too Short/Long**
   - **Description**: Balance between security and user experience
   - **Impact**: User frustration or security risk
   - **Probability**: Low
   - **Mitigation**: Start with 24h, make configurable

2. **No Rate Limiting on Auth Endpoints**
   - **Description**: Brute force attacks possible
   - **Impact**: Security risk
   - **Probability**: Medium
   - **Mitigation**: Note for future - not in scope now

---

### 5. Impact Areas

#### Files to Modify
```
src/
├── models/
│   └── User.ts (modify - add password field, hash method)
├── middleware/
│   ├── auth.middleware.ts (create - JWT verification)
│   └── errorHandler.ts (modify - add auth errors)
├── routes/
│   ├── auth.routes.ts (create - login, register)
│   └── index.ts (modify - add auth routes)
├── services/
│   └── auth.service.ts (create - token generation, validation)
├── types/
│   └── express.d.ts (create - extend Request with user)
└── server.ts (modify - add auth routes)

.env (modify - add JWT_SECRET, TOKEN_EXPIRY)
```

#### Components Affected
- **Direct**: All route handlers (need to add auth middleware)
- **Indirect**: Error handling, logging
- **Downstream**: Frontend will need to store and send tokens

#### Test Coverage Impact
- **Unit tests**: Need 8 new test files for auth components
- **Integration tests**: Need 5 scenarios (register, login, protected access, etc.)
- **E2E tests**: At least 2 full flows (happy path, unauthorized)

---

### 6. Technical Debt Discovered

1. **User Model Incomplete**
   - **Current State**: Missing email validation, password field
   - **Impact**: Need to add migration for password field
   - **Recommendation**: Fix now - required for auth

2. **No Input Validation Pattern**
   - **Current State**: Inconsistent validation across routes
   - **Impact**: Auth endpoints need strong validation
   - **Recommendation**: Use express-validator consistently

---

### 7. Recommendations for Planning

1. **Incremental Approach** - Don't apply auth middleware globally at first
2. **Test Thoroughly** - Auth is security-critical, need comprehensive tests
3. **Follow OWASP** - Use established patterns, don't invent crypto
4. **Make Configurable** - Token expiry, secret rotation should be env-based

**Preferred Approach**: Middleware-based auth with JWT in Authorization header

**Approaches to Avoid**:
- Session-based auth (stateless is better for API)
- Storing passwords in plain text (obvious but worth stating)
- Rolling own crypto (use bcrypt, jsonwebtoken libraries)

---

### 8. Open Questions

1. **Should existing routes require auth immediately?** - Need user decision
2. **Email verification required?** - Adds complexity, YAGNI?

---

**Analysis Complete** ✓
```

#### Step 2: Orchestrator Asks User Questions

```markdown
Before planning, I need clarification on two points from the analysis:

1. **Should existing routes require authentication immediately?**
   - This will break any existing clients
   - Alternative: Add auth middleware gradually, route by route

2. **Do you want email verification for new registrations?**
   - Adds complexity (email service, verification tokens)
   - Could defer to future iteration (YAGNI)

Your preferences?
```

**User Response**: "Yes, require auth on all routes immediately - no active clients yet. No email verification for now, keep it simple."

#### Step 3: Planner Agent Output

```markdown
## 📋 Implementation Strategy

**Based on**: Analysis Report + User clarifications

---

### 1. Approach

Build JWT authentication using middleware pattern with Express, following OWASP guidelines for password storage and token management. Apply auth middleware globally to all routes except auth endpoints themselves.

**Why This Approach**:
- Middleware pattern is idiomatic Express and already used in codebase
- JWT is stateless - no session storage needed
- bcrypt + jsonwebtoken are industry-standard libraries
- Can be implemented incrementally in one session

---

### 2. Architectural Decisions

#### Decision 1: JWT vs Session-Based Auth

**Context**: Need to choose authentication mechanism for REST API

**Options Considered**:
1. **JWT (Stateless)**
   - Pros: No server-side session storage, scales horizontally, works across services
   - Cons: Can't invalidate tokens before expiry, slightly larger payload
   - Complexity: 2/5

2. **Session-Based (Stateful)**
   - Pros: Easy to invalidate, smaller payload
   - Cons: Requires session store (Redis), sticky sessions for load balancing
   - Complexity: 3/5

**Decision**: JWT (stateless)

**Rationale**:
- API is stateless REST
- No session infrastructure available
- User wants simple solution
- Token invalidation not required initially

**Trade-offs Accepted**:
- Can't revoke tokens early (accepted - tokens are short-lived 24h)
- Slightly more bandwidth (minimal impact)

---

#### Decision 2: Password Hashing Strategy

**Decision**: bcrypt with salt rounds = 12

**Rationale**:
- OWASP recommended
- Adaptive - can increase rounds as hardware improves
- Widely tested and secure

**Alternatives Considered**: argon2, scrypt - more modern but bcrypt sufficient for this use case

---

#### Decision 3: Auth Middleware Placement

**Decision**: Global middleware with route exclusions

**Rationale**:
- Secure by default - new routes automatically protected
- Explicit exclusions for public routes (register, login)
- Follows "fail secure" principle

---

### 3. Implementation Phases

#### Phase 1: Foundation (Setup and Models)

**Goal**: Database and authentication dependencies ready

**Tasks**:

##### Task 1.1: Update User Model
**Deliverable**: User model with password field and hash method

**Actions**:
1. Add password field to User interface
   - File: `src/models/User.ts`
   - Change: Add `password: string` (private, not returned in JSON)

2. Add password hashing method
   - File: `src/models/User.ts`
   - Change: `async hashPassword()` method using bcrypt

3. Add password comparison method
   - File: `src/models/User.ts`
   - Change: `async comparePassword(plaintext)` method

**Testing**:
- [ ] Unit test: password hashing works
- [ ] Unit test: password comparison works (correct password)
- [ ] Unit test: password comparison fails (wrong password)

**Dependencies**: Requires bcrypt installed

**Estimated Complexity**: Low

---

##### Task 1.2: Install Dependencies
**Deliverable**: Required packages installed and types available

**Actions**:
1. Install runtime dependencies
   - Command: `npm install jsonwebtoken bcrypt`

2. Install type definitions
   - Command: `npm install -D @types/jsonwebtoken @types/bcrypt`

3. Add environment variables
   - File: `.env`
   - Add: `JWT_SECRET=<generate-strong-secret>`
   - Add: `TOKEN_EXPIRY=24h`

**Testing**:
- [ ] Verify imports work in TypeScript

**Dependencies**: None

**Estimated Complexity**: Low

---

##### Task 1.3: Create TypeScript Type Extensions
**Deliverable**: Express Request type includes authenticated user

**Actions**:
1. Create type declaration file
   - File: `src/types/express.d.ts` (create)
   - Change: Extend Express.Request with optional `user` property

**Testing**:
- [ ] TypeScript compilation succeeds

**Dependencies**: None

**Estimated Complexity**: Low

---

**Phase Completion Criteria**:
- [ ] User model has password field
- [ ] All dependencies installed
- [ ] TypeScript types in place
- [ ] Tests passing

**Phase Validation**:
- Run: `npm run build && npm test`
- Expected: Zero TypeScript errors, all tests pass

---

#### Phase 2: Core Authentication Logic

**Goal**: JWT generation and verification working

**Tasks**:

##### Task 2.1: Create Auth Service
**Deliverable**: Service for token generation and validation

**Actions**:
1. Create auth service file
   - File: `src/services/auth.service.ts` (create)

2. Implement `generateToken(userId: string)`
   - Returns JWT signed with secret
   - Includes expiry from env

3. Implement `verifyToken(token: string)`
   - Verifies JWT signature
   - Returns decoded payload or throws

4. Implement `hashPassword(password: string)`
   - Wrapper for bcrypt.hash with salt rounds = 12

5. Implement `comparePasswords(plain: string, hashed: string)`
   - Wrapper for bcrypt.compare

**Testing**:
- [ ] Unit test: generate token creates valid JWT
- [ ] Unit test: verify token validates correct token
- [ ] Unit test: verify token rejects invalid token
- [ ] Unit test: verify token rejects expired token
- [ ] Unit test: hash password creates different hash each time
- [ ] Unit test: compare passwords works correctly

**Dependencies**: Task 1.2 (dependencies installed)

**Estimated Complexity**: Medium

---

##### Task 2.2: Create Auth Middleware
**Deliverable**: Middleware that verifies JWT on requests

**Actions**:
1. Create middleware file
   - File: `src/middleware/auth.middleware.ts` (create)

2. Implement `authenticate` middleware
   - Extract token from Authorization header (Bearer scheme)
   - Verify token using auth.service
   - Attach user to request object
   - Pass to next() or return 401

**Testing**:
- [ ] Unit test: allows valid token
- [ ] Unit test: rejects missing token
- [ ] Unit test: rejects invalid token
- [ ] Unit test: rejects malformed Authorization header
- [ ] Unit test: attaches user to request

**Dependencies**: Task 2.1 (auth service)

**Estimated Complexity**: Medium

---

**Phase Completion Criteria**:
- [ ] Auth service implemented and tested
- [ ] Auth middleware implemented and tested
- [ ] All unit tests passing

**Phase Validation**:
- Run: `npm test src/services/auth.service.test.ts src/middleware/auth.middleware.test.ts`
- Expected: All tests pass

---

#### Phase 3: Auth Endpoints

**Goal**: Register and login endpoints working

**Tasks**:

##### Task 3.1: Create Register Endpoint
**Deliverable**: POST /auth/register endpoint

**Actions**:
1. Create auth routes file
   - File: `src/routes/auth.routes.ts` (create)

2. Implement POST /register handler
   - Validate input (email, password)
   - Check if user exists
   - Hash password
   - Create user in database
   - Generate token
   - Return token + user info

**Testing**:
- [ ] Integration test: successful registration
- [ ] Integration test: duplicate email rejected
- [ ] Integration test: invalid email rejected
- [ ] Integration test: weak password rejected

**Dependencies**: Task 2.1 (auth service)

**Estimated Complexity**: Medium

---

##### Task 3.2: Create Login Endpoint
**Deliverable**: POST /auth/login endpoint

**Actions**:
1. Implement POST /login handler in auth.routes.ts
   - Validate input (email, password)
   - Find user by email
   - Compare password with hash
   - Generate token
   - Return token + user info

**Testing**:
- [ ] Integration test: successful login
- [ ] Integration test: wrong password rejected
- [ ] Integration test: non-existent user rejected
- [ ] Integration test: token is valid JWT

**Dependencies**: Task 2.1 (auth service)

**Estimated Complexity**: Medium

---

##### Task 3.3: Register Auth Routes
**Deliverable**: Auth routes connected to Express app

**Actions**:
1. Update route registration
   - File: `src/routes/index.ts`
   - Change: Import and register auth routes at /auth

2. Update server
   - File: `src/server.ts`
   - Change: Ensure routes registered before error handler

**Testing**:
- [ ] Manual test: POST /auth/register works
- [ ] Manual test: POST /auth/login works

**Dependencies**: Tasks 3.1, 3.2

**Estimated Complexity**: Low

---

**Phase Completion Criteria**:
- [ ] Register endpoint works
- [ ] Login endpoint works
- [ ] Endpoints integrated into app
- [ ] All tests passing

**Phase Validation**:
- Run: `npm run dev` then test with curl/Postman
- Expected: Can register, login, receive tokens

---

#### Phase 4: Protected Routes

**Goal**: All existing routes require authentication

**Tasks**:

##### Task 4.1: Apply Global Auth Middleware
**Deliverable**: Auth middleware protecting all routes except /auth/*

**Actions**:
1. Update server middleware chain
   - File: `src/server.ts`
   - Change: Add auth.middleware before route registration
   - Change: Exclude /auth/* routes from auth check

2. Update error handler
   - File: `src/middleware/errorHandler.ts`
   - Change: Add handling for 401 Unauthorized
   - Change: Add handling for JWT errors

**Testing**:
- [ ] Integration test: protected route requires token
- [ ] Integration test: protected route works with valid token
- [ ] Integration test: protected route rejects invalid token
- [ ] Integration test: auth routes work without token

**Dependencies**: Task 2.2 (auth middleware)

**Estimated Complexity**: Low

---

##### Task 4.2: Update Existing Route Handlers
**Deliverable**: Route handlers use authenticated user

**Actions**:
1. Update route handlers to access req.user
   - Files: All route handlers in `src/routes/*.ts`
   - Change: Use `req.user` for user context (instead of passing in requests)

**Testing**:
- [ ] Integration test: each route works with authenticated user
- [ ] Integration test: user context is correct

**Dependencies**: Task 4.1

**Estimated Complexity**: Medium

---

**Phase Completion Criteria**:
- [ ] All routes protected
- [ ] Auth routes excluded
- [ ] Error handling works
- [ ] All tests passing

**Phase Validation**:
- Run: `npm test`
- Expected: Full test suite passes

---

#### Phase 5: Final Polish

**Goal**: Production-ready with documentation

**Tasks**:

##### Task 5.1: Add Request Validation
**Deliverable**: Input validation on auth endpoints

**Actions**:
1. Add validation middleware to register
   - Email format validation
   - Password strength (min 8 chars, complexity)

2. Add validation middleware to login
   - Email format validation
   - Password presence

**Testing**:
- [ ] Test: weak password rejected
- [ ] Test: invalid email rejected

**Dependencies**: None (uses existing express-validator)

**Estimated Complexity**: Low

---

##### Task 5.2: Documentation
**Deliverable**: README and API docs updated

**Actions**:
1. Update README
   - Add auth setup instructions
   - Document environment variables

2. Add API documentation
   - Document POST /auth/register
   - Document POST /auth/login
   - Document Authorization header format

**Testing**:
- [ ] Manual review: docs are clear

**Dependencies**: None

**Estimated Complexity**: Low

---

**Phase Completion Criteria**:
- [ ] Validation working
- [ ] Documentation complete
- [ ] All tests passing

**Phase Validation**:
- Run: `npm run build && npm test`
- Expected: Clean build, all tests pass

---

### 4. Timeline Estimate

| Phase | Tasks | Complexity | Est. Time |
|-------|-------|------------|-----------|
| Phase 1 | 3 | Low | 30-45 min |
| Phase 2 | 2 | Medium | 45-60 min |
| Phase 3 | 3 | Medium | 45-60 min |
| Phase 4 | 2 | Medium | 30-45 min |
| Phase 5 | 2 | Low | 20-30 min |
| **Total** | **12** | **Mixed** | **2.5-4 hours** |

**Assumptions**:
- Familiar with Express and JWT concepts
- Test writing is quick (using existing patterns)
- No unexpected bcrypt or JWT issues

**Risks to Timeline**:
- Database migration issues could add time
- TypeScript type issues might require debugging

---

### 5. Success Criteria

#### Functional Requirements
- [ ] Users can register with email and password
- [ ] Users can login and receive JWT token
- [ ] All existing routes require valid JWT
- [ ] Invalid/missing tokens return 401

#### Non-Functional Requirements
- [ ] Passwords hashed with bcrypt (salt rounds >= 10)
- [ ] JWTs signed with strong secret
- [ ] Auth middleware adds < 10ms latency
- [ ] No passwords in logs or error messages

#### Quality Gates
- [ ] All existing tests still pass
- [ ] New code has >= 80% test coverage
- [ ] No TypeScript errors in strict mode
- [ ] ESLint passes with no warnings

#### Documentation Requirements
- [ ] README updated with auth setup
- [ ] API endpoints documented
- [ ] Environment variables documented

---

### 6. Rollback Strategy

#### Quick Rollback (< 5 minutes)
**Steps**:
1. Revert commits: `git revert HEAD~5..HEAD` (5 commits for 5 phases)
2. Reinstall dependencies: `npm install`
3. Restart server: `npm run dev`

**Data Impact**:
- User table may have password field but it's optional
- No data loss, worst case users can't login (no active users yet)

#### Safe Rollback (< 15 minutes)
**Steps**:
1. Remove auth middleware from server.ts
2. Comment out auth routes
3. Keep database changes (harmless)
4. Restart server

**Data Impact**: None

#### Points of No Return
- After Phase 3: User passwords are in database (hashed)
- Mitigation: Hashed passwords are safe to keep, just disable auth if needed

---

### 7. Alternative Approaches Considered

#### Alternative 1: OAuth2 with Third-Party Provider
- **Description**: Use Auth0, Firebase, or similar
- **Why not chosen**: Overkill for simple API, adds external dependency, costs money

#### Alternative 2: Session-Based Auth
- **Description**: Traditional cookie-based sessions
- **Why not chosen**: Requires session store (Redis), not ideal for stateless REST API

#### Alternative 3: API Keys
- **Description**: Generate API keys for users
- **Why not chosen**: Less flexible, no expiry, can't carry user metadata

---

### 8. Risk Mitigation Plan

| Risk | Mitigation Strategy | Monitoring |
|------|---------------------|------------|
| Passwords leaked | Never log passwords, use bcrypt | Code review before commit |
| Weak JWT secret | Generate 256-bit random secret | Document in .env.example |
| Breaking existing routes | Test all routes after phase 4 | Run full integration test suite |
| Token theft | Use HTTPS only, short expiry | Document HTTPS requirement |

---

### 9. Dependencies & Coordination

**Team Dependencies**:
- [ ] Need review from: Security engineer (if available)
- [ ] Not blocked by other work

**External Dependencies**:
- [ ] None - all dependencies are npm packages

---

### 10. Post-Implementation Tasks

- [ ] Security scan (npm audit)
- [ ] Performance test auth middleware latency
- [ ] Update API documentation site
- [ ] Add monitoring for failed auth attempts
- [ ] Consider rate limiting for future iteration

---

**Strategy Complete** ✓
```

#### Step 4: Validator Agent Output

```markdown
## ✅ Validation Report

**Validated by**: Validator Agent
**Date**: [Timestamp]

---

### 1. Risk Assessment

#### Risk Scoring Matrix

| Dimension | Score | Reasoning |
|-----------|-------|-----------|
| **Technical Feasibility** | 2 | Well-understood JWT pattern, good libraries available |
| **Complexity** | 3 | Multiple components but clear dependencies, moderate logic |
| **Dependencies** | 2 | Stable npm packages, no external services |
| **Time Estimate** | 2 | 2.5-4 hours is reasonable for this scope |
| **Reversibility** | 2 | Easy to rollback, minimal data impact |
| **OVERALL** | **2.2** | **🟢 LOW-MEDIUM RISK** |

#### Risk Level: 🟢 LOW-MEDIUM

**Summary**: Solid plan with manageable risks. Auth is security-critical but approach follows best practices and uses battle-tested libraries.

---

### 2. Validation Checklist

#### Analysis Quality
- [x] ✅ All major components identified
- [x] ✅ Dependencies comprehensive
- [x] ✅ Risks realistic and complete
- [x] ✅ Impact areas thorough
- [x] ✅ No obvious blind spots

#### Strategy Quality
- [x] ✅ Approach addresses all risks
- [x] ✅ Architectural decisions justified
- [x] ✅ Trade-offs explicitly stated
- [x] ✅ Phases logically sequenced
- [x] ✅ Tasks specific and actionable
- [x] ✅ Success criteria measurable
- [x] ✅ Rollback strategy viable

#### Completeness
- [x] ✅ Testing strategy adequate
- [x] ✅ Error handling considered
- [ ] ⚠️ Performance implications addressed (minor gap)
- [x] ✅ Security considerations included
- [x] ✅ Documentation plan clear
- [ ] ⚠️ Monitoring/observability covered (future iteration)

#### Feasibility
- [x] ✅ Timeline realistic
- [x] ✅ Required knowledge available
- [x] ✅ Dependencies obtainable
- [x] ✅ Resources sufficient
- [x] ✅ No blockers overlooked

**Checklist Score**: 18/20 items passing

---

### 3. Issues Found

#### 🚨 Critical Issues

None identified ✓

---

#### ⚠️ Major Concerns

None identified ✓

---

#### 🔶 Minor Suggestions

1. **Add performance benchmark**: Consider adding a simple benchmark in Phase 5 to verify auth middleware is < 10ms as specified in success criteria.

2. **Rate limiting mentioned but not planned**: Analysis correctly identified this as future work, but might want to add a TODO comment in code for visibility.

3. **Password strength validation**: Task 5.1 mentions "complexity" but doesn't specify requirements. Suggest: at least 1 number, 1 special char.

---

### 4. Cross-Validation

#### Risks from Analysis addressed in Strategy?

- [x] Breaking existing routes → ✅ Phase 4 applies middleware carefully with exclusions
- [x] Password storage vulnerability → ✅ bcrypt with 12 rounds, documented in Decision 2
- [x] JWT secret management → ✅ Environment variable, strong generation documented
- [x] Token expiry → ✅ Configurable via env, defaulting to 24h
- [x] Rate limiting → ✅ Acknowledged as future work, not in scope

**All critical risks addressed** ✓

#### Dependencies mapped to tasks?

- [x] User model update → Task 1.1
- [x] bcrypt, jsonwebtoken → Task 1.2
- [x] TypeScript types → Task 1.3
- [x] Auth middleware → Task 2.2
- [x] Route handlers → Task 4.2

**All dependencies mapped** ✓

#### Impact areas covered by phases?

- [x] User.ts → Phase 1
- [x] Auth middleware → Phase 2
- [x] Auth routes → Phase 3
- [x] Existing routes → Phase 4
- [x] Error handler → Phase 4

**All impact areas covered** ✓

---

### 5. Spot Checks

**Claim from Analysis**: "express-validator already used"
- **Verification**: Analysis mentions it's already used, so Task 5.1 is feasible ✓

**Claim from Strategy**: "Middleware pattern already used in codebase"
- **Verification**: Analysis confirmed errorHandler.ts uses middleware ✓

**Task estimate**: "Phase 1 estimated 30-45 min for 3 low-complexity tasks"
- **Assessment**: Reasonable - simple model changes and npm installs ✓

**Task 2.2 complexity**: "Auth middleware marked Medium"
- **Assessment**: Correct - token extraction and verification has edge cases ✓

---

### 6. Alternative Assessment

**Alternatives considered**: Yes ✅

Alternatives (OAuth2, sessions, API keys) were all dismissed with clear reasoning:
- OAuth2: Too complex for requirements
- Sessions: Doesn't fit stateless REST API
- API keys: Less flexible

**Assessment**: Justified ✅ - JWT is the right choice for this use case

---

### 7. Final Decision

**Status**: ✅ **APPROVED** - Ready for user confirmation and implementation

---

**Approval Statement**:

This plan is comprehensive, well-structured, and ready for implementation. The approach follows security best practices, uses industry-standard libraries, and includes thorough testing strategy. Risk level is low-medium and manageable.

**Strengths**:
1. **Security-first approach**: bcrypt, JWT best practices, OWASP compliance
2. **Clear phase boundaries**: Each phase has testable completion criteria
3. **Thorough testing**: Unit, integration, and manual test coverage
4. **Good task granularity**: 12 tasks is manageable, each with specific actions
5. **Risk mitigation**: All critical risks from analysis addressed in strategy

**Recommendations for Implementation**:
1. **Test after each phase**: Don't proceed to next phase until tests pass
2. **Generate strong JWT secret**: Use `openssl rand -base64 32` or similar
3. **Code review focus**: Have someone review password handling and JWT implementation
4. **Manual testing**: After Phase 3, test register/login flows manually before moving on

**Next Steps**:
1. Present consolidated plan to user for final approval
2. Get user confirmation on JWT secret generation
3. Begin Phase 1 implementation
4. Run tests after each phase before proceeding

---

**Validation Complete** ✓
```

#### Step 5: Final Presentation to User

```markdown
## Deep Dive Plan: JWT Authentication - Ready for Approval

I've completed a thorough analysis and planning process using three specialized agents (Analyzer, Planner, Validator). Here's the summary:

### 📊 Overview

**What we're building**: JWT-based authentication with register, login, and protected routes

**Risk Level**: 🟢 Low-Medium
**Estimated Time**: 2.5-4 hours
**Phases**: 5 (Foundation → Core Logic → Endpoints → Protection → Polish)
**Tasks**: 12 specific tasks with clear deliverables

### ✅ Key Decisions

1. **JWT over sessions** - Stateless, scales better for REST API
2. **bcrypt for passwords** - Industry standard, OWASP recommended
3. **Global middleware** - Secure by default, explicit exclusions for public routes

### 🛡️ Security Highlights

- Passwords hashed with bcrypt (salt rounds = 12)
- JWT secrets from environment variables
- Input validation on auth endpoints
- Auth middleware adds < 10ms latency

### 📋 Implementation Plan

**Phase 1**: Set up User model with password field, install dependencies
**Phase 2**: Build auth service (token gen/verify) and middleware
**Phase 3**: Create register and login endpoints
**Phase 4**: Protect all existing routes with auth middleware
**Phase 5**: Add validation and documentation

Each phase has specific tasks, tests, and validation criteria.

### 🎯 Success Criteria

- Users can register and login
- All routes require valid JWT
- Comprehensive test coverage (>80%)
- Full documentation

### 📄 Full Plan

I've documented the complete analysis, strategy, and validation in detail. The plan includes:
- Current state analysis with file locations
- All architectural decisions with rationales
- Step-by-step implementation tasks
- Rollback strategy if needed
- Risk mitigation for all identified risks

**Ready to proceed?**

If you approve, I'll save the full plan to `claudedocs/` and we can start implementation with Phase 1.
```

---

## Example 2: Refactoring Monolithic Service

### User Request

> "Our OrderService has grown to 2000 lines and is becoming unmaintainable. Help me refactor it."

### Abbreviated Workflow

#### Analyzer Findings (Summary)

```markdown
## 🔍 Key Analysis Findings

**Current State**:
- OrderService.ts: 2000 lines, 45 methods
- Mixes concerns: validation, business logic, database, email, payments
- No clear separation of responsibilities
- Testing is difficult due to tight coupling

**Major Risks**:
- 🚨 Breaking existing functionality during refactor
- ⚠️ Service is used in 23 places across codebase
- ⚠️ No comprehensive test coverage (only 40%)

**Recommendation**: Extract services following Single Responsibility Principle
```

#### Planner Strategy (Summary)

```markdown
## 📋 Key Planning Decisions

**Approach**: Extract to 5 specialized services incrementally

**Architecture Decision**:
- OrderService (orchestration)
  ├─ ValidationService (input validation)
  ├─ PaymentService (payment processing)
  ├─ InventoryService (stock management)
  ├─ NotificationService (emails, webhooks)
  └─ OrderRepository (database)

**Phases**:
1. Add comprehensive tests to existing OrderService (safety net)
2. Extract ValidationService (lowest risk)
3. Extract PaymentService (high value)
4. Extract remaining services
5. Slim down OrderService to orchestrator

**Key Strategy**: Test-first refactoring - each extraction validated before next
```

#### Validator Decision (Summary)

```markdown
## ✅ Validation Decision

**Risk Level**: 🟠 HIGH
- Score: 3.6/5
- High complexity, many dependencies
- But: Approach is sound, incremental is safe

**Status**: 🔄 NEEDS REVISION

**Issue Found**:
⚠️ **Major Concern**: Phase 1 says "add comprehensive tests" but doesn't specify what coverage target or which scenarios. This is critical for safety net.

**Required Change**:
Planner must detail specific test scenarios for Phase 1:
- Happy path for each major method
- Edge cases (empty cart, invalid payment, out of stock)
- Error handling for each external service
- Target: 80% coverage before refactoring

**After revision**: Will re-validate
```

#### Iteration: Planner Revises Phase 1

```markdown
## 📋 Revised Phase 1: Comprehensive Test Coverage

**Goal**: Achieve 80% test coverage as safety net

**Tasks**:

##### Task 1.1: Test Order Creation Flow
- Happy path: valid order successfully created
- Edge case: empty cart
- Edge case: invalid items
- Edge case: out of stock items
- Error case: payment service down
- Error case: database failure

##### Task 1.2: Test Order Updates
[... specific scenarios ...]

##### Task 1.3: Test Payment Processing
[... specific scenarios ...]

**Completion Criteria**:
- [ ] Coverage report shows >= 80%
- [ ] All critical paths tested
- [ ] All external service failures mocked and tested

**Phase Validation**:
- Run: `npm run test:coverage`
- Expected: OrderService.ts >= 80% coverage
```

#### Re-Validation: Approved

```markdown
## ✅ Validation Decision (Round 2)

**Status**: ✅ APPROVED

Phase 1 now has specific test scenarios and measurable coverage target. This provides the safety net needed for high-risk refactoring. Ready to proceed.
```

---

## Example 3: Simple Bug Fix (When NOT to Use This Skill)

### User Request

> "Fix the bug where user names are displaying as 'undefined' on the profile page"

### Correct Response

```markdown
This is a straightforward bug fix and doesn't need deep dive planning. I'll just:

1. Find where user names are displayed (likely 1-2 files)
2. Check if data is being fetched correctly
3. Fix the issue
4. Test the fix

This is better suited for direct implementation or the regular `/software-engineer` skill.

**Deep dive planning** is overkill for simple bugs - use it for:
- Complex features requiring architectural decisions
- Large refactoring efforts
- Multi-component system changes
- Situations with unclear implementation paths

For this bug, let's just fix it directly.
```

---

## Key Lessons from Examples

### When Deep Dive Planning Shines

1. **Complex Features** (Example 1: JWT Auth)
   - Multiple components to build
   - Security implications
   - Architectural decisions needed
   - Benefits: Thorough risk assessment, clear implementation path

2. **High-Risk Refactoring** (Example 2: Service Extraction)
   - Breaking existing functionality is likely
   - Many dependencies across codebase
   - Benefits: Safety net strategy, incremental approach

3. **Unclear Requirements**
   - User request is vague ("improve performance", "modernize architecture")
   - Benefits: Analysis phase clarifies scope, planning phase proposes concrete approach

### When to Skip Deep Dive Planning

1. **Simple bugs** - Direct fix is faster
2. **Well-understood patterns** - Follow existing implementation
3. **Prototypes/experiments** - Don't need comprehensive planning
4. **Tight deadlines** - Planning overhead may not be justified

### Success Patterns

1. **User clarification**: Analyzer asks questions, Orchestrator gets answers before planning
2. **Iteration works**: Validator catches gaps, Planner revises, plan improves
3. **Phased approach**: Breaking into phases makes complex work manageable
4. **Test-driven**: Safety nets (tests, rollback) catch issues early

### Anti-Patterns to Avoid

1. **Analysis paralysis**: If Validator approves, stop iterating
2. **Planning without analysis**: Planner needs Analyzer's findings
3. **Skipping validation**: Even if you're confident, validate the plan
4. **Over-planning simple tasks**: Use judgment on when deep dive is overkill

---

These examples demonstrate the three-agent system in action. The key is thoroughness without over-engineering - invest planning time proportional to implementation risk and complexity.
