# Deep Dive Planning Reference

Detailed templates, checklists, and guidelines for each agent in the planning system.

---

## 🔍 Analyzer Agent Reference

### Analysis Framework

Use this systematic approach for thorough analysis:

#### 1. Codebase Exploration

**Goal**: Understand current architecture and patterns

**Steps:**
1. Use Explore agent to map out project structure
2. Identify main components and their relationships
3. Find existing patterns similar to what's needed
4. Document architectural style (MVC, layered, microservices, etc.)

**Questions to answer:**
- What's the overall project structure?
- What design patterns are currently used?
- How do components communicate?
- What's the data flow?

#### 2. Dependency Analysis

**Goal**: Map all dependencies and integration points

**Internal Dependencies:**
- Modules/packages this change will use
- Components that will be affected by this change
- Shared utilities or services involved

**External Dependencies:**
- Third-party libraries required
- APIs or services to integrate
- Database schema changes needed
- Infrastructure requirements

**Tools:**
```bash
# For package dependencies
npm list [package-name]
gradle dependencies
pip show [package-name]

# For import analysis
grep -r "import.*[pattern]" --include="*.ts"
```

#### 3. Constraint Discovery

**Technical Constraints:**
- Language/framework version limitations
- Performance requirements (latency, throughput)
- Memory/resource constraints
- Compatibility requirements (browsers, OS)

**Business Constraints:**
- Security/compliance requirements (GDPR, SOC2)
- Scalability targets
- Backwards compatibility needs
- Timeline pressures

#### 4. Risk Identification

Use this risk classification:

**🚨 Critical Risks** (Blockers):
- Breaking changes to public APIs
- Data loss potential
- Security vulnerabilities
- Production outages

**⚠️ High Risks** (Major concerns):
- Performance degradation
- Complex migration paths
- High technical debt areas
- Missing critical knowledge

**🔶 Medium Risks** (Manageable):
- Edge cases to handle
- Testing challenges
- Documentation needs
- Minor breaking changes

**🔵 Low Risks** (Minor concerns):
- Code style inconsistencies
- Nice-to-have features
- Optional improvements

#### 5. Impact Assessment

**Blast Radius Analysis:**
- List all files that will be modified
- List all components that depend on modified code
- Identify integration points with other systems
- Estimate number of users/requests affected

**Testing Impact:**
- Existing tests that will break
- New test coverage needed
- Integration test requirements
- E2E test scenarios

### Analysis Report Template

```markdown
## 🔍 Analysis Report

**Analyzed by**: Analyzer Agent
**Date**: [Timestamp]
**Request**: [User's original request]

---

### 1. Current State

#### Architecture Overview
[Describe current architecture, key components, design patterns]

#### Relevant Code Locations
- `path/to/file.ts:45-89` - [What this code does]
- `path/to/another.ts:12-34` - [What this code does]

#### Existing Patterns
[Similar implementations found in codebase]

---

### 2. Dependencies

#### Internal Dependencies
| Component | Relationship | Impact Level |
|-----------|--------------|--------------|
| `auth.service` | Will use for validation | Medium |
| `user.model` | Schema change needed | High |

#### External Dependencies
| Package | Version | Purpose | Risk |
|---------|---------|---------|------|
| `express` | ^4.18.0 | HTTP framework | Low |
| `jsonwebtoken` | ^9.0.0 | Auth tokens | Medium |

#### Infrastructure Requirements
- [ ] Database migration needed
- [ ] New environment variables
- [ ] External service access
- [ ] Additional hosting resources

---

### 3. Constraints

#### Technical Constraints
- **Language**: TypeScript 5.0+ required for [reason]
- **Performance**: Must handle 1000 req/sec
- **Compatibility**: Support Node 18+
- **Security**: Must comply with OWASP Top 10

#### Business Constraints
- **Timeline**: [If mentioned by user]
- **Resources**: [Team size, availability]
- **Compliance**: [GDPR, HIPAA, etc.]
- **Budget**: [If cost-sensitive]

---

### 4. Risks Identified

#### 🚨 Critical Risks
1. **[Risk Name]**
   - **Description**: [What could go wrong]
   - **Impact**: [Consequences]
   - **Probability**: [Low/Medium/High]
   - **Mitigation**: [How to prevent/minimize]

#### ⚠️ High Risks
[Same format as critical]

#### 🔶 Medium Risks
[Same format]

#### 🔵 Low Risks
[Same format]

---

### 5. Impact Areas

#### Files to Modify
```
src/
├── auth/
│   ├── auth.service.ts (modify)
│   └── auth.controller.ts (modify)
├── users/
│   └── user.model.ts (modify)
└── shared/
    └── middleware/ (new)
        └── auth.middleware.ts (create)
```

#### Components Affected
- **Direct**: [Components that will change]
- **Indirect**: [Components that depend on changes]
- **Downstream**: [Services/apps that consume this]

#### Test Coverage Impact
- **Unit tests**: X tests will break, Y new tests needed
- **Integration tests**: Z scenarios to cover
- **E2E tests**: W flows to validate

---

### 6. Technical Debt Discovered

[Existing issues found during analysis that may complicate implementation]

1. **[Issue Area]**
   - **Current State**: [What's problematic]
   - **Impact on Plan**: [How it affects this work]
   - **Recommendation**: [Fix now vs later]

---

### 7. Recommendations for Planning

Based on analysis, the Planner should consider:

1. **[Recommendation 1]** - [Rationale]
2. **[Recommendation 2]** - [Rationale]
3. **[Recommendation 3]** - [Rationale]

**Preferred Approach**: [High-level suggestion]

**Approaches to Avoid**: [Anti-patterns or known pitfalls]

---

### 8. Open Questions

Questions that need user input or further investigation:

1. **[Question 1]** - [Why it matters]
2. **[Question 2]** - [Why it matters]

---

**Analysis Complete** ✓

Next: Pass this report to the Planner agent.
```

---

## 📋 Planner Agent Reference

### Planning Framework

#### 1. Strategy Development

**Read and internalize** the Analyzer's report first.

**Ask yourself:**
- What's the simplest approach that addresses all requirements?
- What are the key architectural decisions needed?
- What can be done incrementally vs all-at-once?
- What's the critical path?

**Principles:**
- **YAGNI**: Don't plan for hypothetical future requirements
- **Incremental**: Break into smallest valuable increments
- **Reversible**: Prefer approaches that can be undone
- **Testable**: Each phase should be verifiable

#### 2. Architectural Decision Making

For each significant decision, document using ADR (Architecture Decision Record) format:

```markdown
### Decision: [Short title]

**Context**: [What situation requires this decision]

**Options Considered**:
1. **Option A**: [Description]
   - Pros: [Benefits]
   - Cons: [Drawbacks]
   - Complexity: [1-5]

2. **Option B**: [Description]
   - Pros: [Benefits]
   - Cons: [Drawbacks]
   - Complexity: [1-5]

**Decision**: [Chosen option]

**Rationale**: [Why this option over others]

**Trade-offs Accepted**:
- [What we're giving up]
- [What we're gaining]

**Consequences**:
- Positive: [Benefits]
- Negative: [Costs]
- Neutral: [Other impacts]
```

#### 3. Phase Breakdown

Organize work into logical phases:

**Phase Types:**

1. **Foundation Phase**
   - Set up infrastructure
   - Add dependencies
   - Create base structures
   - **Goal**: Enable core implementation

2. **Core Implementation Phase**
   - Implement main functionality
   - Add business logic
   - Create core components
   - **Goal**: Working feature (may be feature-flagged)

3. **Integration Phase**
   - Connect to existing systems
   - Add API endpoints
   - Wire up UI components
   - **Goal**: End-to-end functionality

4. **Polish Phase**
   - Add error handling
   - Improve performance
   - Add logging/monitoring
   - Update documentation
   - **Goal**: Production-ready

**Phase Template:**
```markdown
#### Phase N: [Phase Name]

**Goal**: [What this phase achieves - must be testable]

**Prerequisites**:
- [ ] [What must be done before starting]
- [ ] [Dependencies from previous phases]

**Tasks**:

##### Task N.1: [Task Name]
**Deliverable**: [Concrete output - file, function, component]

**Actions**:
1. [Specific step 1]
   - File: `path/to/file`
   - Change: [What to modify]

2. [Specific step 2]
   - File: `path/to/file`
   - Change: [What to create]

**Testing**:
- [ ] Unit test: [Specific test case]
- [ ] Integration test: [Specific scenario]

**Dependencies**:
- Requires: [What this task needs]
- Blocks: [What depends on this task]

**Estimated Complexity**: [Low/Medium/High]

##### Task N.2: [Next Task]
[Same structure]

**Phase Completion Criteria**:
- [ ] All tasks completed
- [ ] All tests passing
- [ ] Code reviewed
- [ ] Documentation updated

**Phase Validation**:
- Run: `[Command to verify phase]`
- Expected: [What success looks like]
```

#### 4. Task Sequencing

Determine task order using dependency graph:

```
Task 1.1 (Setup)
    ↓
Task 1.2 (Model) ──→ Task 1.3 (Service)
                        ↓
                    Task 2.1 (Controller)
                        ↓
                    Task 2.2 (Integration)
```

**Parallel opportunities**: Identify tasks that can be done concurrently.

#### 5. Success Criteria Definition

Make criteria **SMART** (Specific, Measurable, Achievable, Relevant, Time-bound):

```markdown
### Success Criteria

#### Functional Requirements
- [ ] Feature X works as specified in [reference]
- [ ] User can complete flow Y without errors
- [ ] System handles Z correctly

#### Non-Functional Requirements
- [ ] Response time < 200ms for typical requests
- [ ] No memory leaks after 10k operations
- [ ] Zero security vulnerabilities in scan
- [ ] Test coverage > 80% for new code

#### Quality Gates
- [ ] All existing tests still pass
- [ ] ESLint/Prettier with zero errors
- [ ] TypeScript strict mode enabled
- [ ] No console.log statements in production code

#### Documentation Requirements
- [ ] README updated with new features
- [ ] API documentation generated
- [ ] Architecture diagram updated
- [ ] Migration guide (if breaking changes)
```

#### 6. Rollback Strategy

Plan for failure before it happens:

```markdown
### Rollback Strategy

#### Quick Rollback (< 5 minutes)
[For emergencies - immediate revert path]

**Steps**:
1. Revert commit: `git revert [commit-hash]`
2. Deploy previous version: `[deployment command]`
3. Verify: `[health check command]`

**Data Impact**: [None | Requires DB rollback]

#### Safe Rollback (< 30 minutes)
[For controlled rollback with data preservation]

**Steps**:
1. Feature flag disable: `[command]`
2. Database migration rollback: `[migration command]`
3. Clean up resources: `[cleanup steps]`
4. Monitoring: `[what to watch]`

**Data Impact**: [Describe any data loss or inconsistency]

#### Points of No Return
[Stages after which rollback becomes very difficult]

- After: [Specific task/phase]
- Reason: [Why rollback is hard]
- Mitigation: [How to minimize risk]
```

### Implementation Strategy Template

```markdown
## 📋 Implementation Strategy

**Planned by**: Planner Agent
**Date**: [Timestamp]
**Based on**: Analysis Report [link/reference]

---

### 1. Approach

#### High-Level Strategy
[2-3 sentences describing overall approach]

**Why This Approach**:
- [Reason 1: Aligns with existing architecture]
- [Reason 2: Minimizes risk]
- [Reason 3: Enables incremental delivery]

**What Makes This Different**:
[If there are existing similar implementations, explain why this approach differs]

---

### 2. Architectural Decisions

[Use ADR format from above - include 2-5 key decisions]

---

### 3. Implementation Phases

[Use Phase Template from above - typically 3-5 phases]

---

### 4. Timeline Estimate

| Phase | Tasks | Complexity | Est. Time |
|-------|-------|------------|-----------|
| Phase 1 | 3 | Medium | 2-3 hours |
| Phase 2 | 5 | High | 4-6 hours |
| Phase 3 | 2 | Low | 1-2 hours |
| **Total** | **10** | **Mixed** | **7-11 hours** |

**Assumptions**:
- [Assumption 1 affecting estimate]
- [Assumption 2 affecting estimate]

**Risks to Timeline**:
- [Risk that could increase time]
- [Dependency that could cause delays]

---

### 5. Success Criteria

[Use Success Criteria template from above]

---

### 6. Rollback Strategy

[Use Rollback Strategy template from above]

---

### 7. Alternative Approaches Considered

#### Alternative 1: [Name]
- **Description**: [Brief explanation]
- **Why not chosen**: [Specific reasons]

#### Alternative 2: [Name]
- **Description**: [Brief explanation]
- **Why not chosen**: [Specific reasons]

---

### 8. Risk Mitigation Plan

For each high/critical risk from Analysis Report:

| Risk | Mitigation Strategy | Monitoring |
|------|---------------------|------------|
| [Risk 1] | [How we'll prevent/minimize] | [How we'll detect] |
| [Risk 2] | [How we'll prevent/minimize] | [How we'll detect] |

---

### 9. Dependencies & Coordination

**Team Dependencies**:
- [ ] Need review from: [Team/person]
- [ ] Blocked by: [Other work]
- [ ] Must coordinate with: [Other teams]

**External Dependencies**:
- [ ] Wait for: [Library update, API access]
- [ ] Request: [Infrastructure, permissions]

---

### 10. Post-Implementation Tasks

What needs to happen after code is complete:

- [ ] Performance testing
- [ ] Security scan
- [ ] Documentation site update
- [ ] Team knowledge sharing
- [ ] Monitoring dashboard setup
- [ ] Alert configuration

---

**Strategy Complete** ✓

Next: Pass this strategy to the Validator agent for review.
```

---

## ✅ Validator Agent Reference

### Validation Framework

#### 1. Critical Evaluation Mindset

**Your role**: Be the voice of reason and risk awareness.

**Principles**:
- **Assume nothing**: Verify claims against codebase
- **Question everything**: Challenge assumptions
- **Think adversarially**: What could go wrong?
- **Be thorough**: Check every section of the plan

**You are not here to rubber-stamp. Be critical.**

#### 2. Risk Scoring Methodology

Rate each dimension on a 1-5 scale:

**Technical Feasibility** (Can we build this?)
- 1 = Trivial, well-understood, existing patterns
- 2 = Straightforward, minor unknowns
- 3 = Moderate complexity, some research needed
- 4 = Complex, significant unknowns or dependencies
- 5 = Extremely complex, requires breakthroughs or major refactoring

**Complexity** (How hard is this?)
- 1 = Single file, simple logic
- 2 = Few files, clear logic
- 3 = Multiple components, moderate logic
- 4 = System-wide changes, complex logic
- 5 = Architectural changes, very complex logic

**Dependencies** (What do we rely on?)
- 1 = Self-contained, no external dependencies
- 2 = Few internal dependencies, stable
- 3 = Multiple internal dependencies
- 4 = External dependencies or unstable internal ones
- 5 = Many external dependencies, version conflicts, or breaking changes

**Time Estimate** (How long will this take?)
- 1 = < 2 hours, well-estimated
- 2 = 2-8 hours, reasonable estimate
- 3 = 1-2 days, moderate uncertainty
- 4 = 2-5 days, significant uncertainty
- 5 = > 5 days, high uncertainty or timeline is too aggressive

**Reversibility** (Can we undo this?)
- 1 = Fully reversible, simple rollback
- 2 = Reversible with minor effort
- 3 = Reversible but requires coordination
- 4 = Hard to reverse, data migration issues
- 5 = Irreversible or extremely costly to reverse

**Overall Risk Calculation**:
- Average 1-2 = Low Risk ✅
- Average 2-3 = Medium Risk ⚠️
- Average 3-4 = High Risk 🚨
- Average 4-5 = Critical Risk 🔥

#### 3. Validation Checklist

Systematically check each aspect:

**Analysis Validation**:
- [ ] All major components identified
- [ ] Dependencies are comprehensive
- [ ] Risks are realistic and complete
- [ ] Impact areas are thorough
- [ ] No obvious blind spots

**Strategy Validation**:
- [ ] Approach addresses all analyzed risks
- [ ] Architectural decisions are justified
- [ ] Trade-offs are explicitly stated
- [ ] Phases are logical and sequenced correctly
- [ ] Tasks are specific and actionable
- [ ] Success criteria are measurable
- [ ] Rollback strategy is viable

**Completeness Validation**:
- [ ] Testing strategy is adequate
- [ ] Error handling is considered
- [ ] Performance implications addressed
- [ ] Security considerations included
- [ ] Documentation plan is clear
- [ ] Monitoring/observability covered

**Feasibility Validation**:
- [ ] Timeline is realistic
- [ ] Required knowledge is available
- [ ] Dependencies are obtainable
- [ ] Resources are sufficient
- [ ] No blockers are overlooked

#### 4. Issue Classification

Categorize every issue you find:

**🚨 Critical Issues** (Plan is not executable):
- Missing prerequisite analysis
- Undefined critical dependencies
- Unaddressed blocker risks
- Infeasible technical approach
- No rollback for irreversible changes
- Missing security considerations for sensitive data

**⚠️ Major Concerns** (Plan has significant gaps):
- Incomplete risk mitigation
- Underestimated complexity
- Missing important phases/tasks
- Weak success criteria
- Inadequate testing strategy
- Poor task sequencing

**🔶 Minor Suggestions** (Improvements but not blockers):
- Could optimize approach
- Documentation could be clearer
- Alternative worth considering
- Nice-to-have additions
- Style/format improvements

#### 5. Decision Making

After thorough review, make one of three decisions:

**✅ APPROVED**
- All critical and major issues resolved
- Minor suggestions only
- Risk level is acceptable
- Plan is ready for user approval

**🔄 NEEDS REVISION**
- Major concerns present but plan is salvageable
- Specific feedback provided for improvement
- Re-validation required after changes

**❌ REJECTED**
- Critical issues make plan unexecutable
- Fundamental flaws in approach
- Must go back to analysis or planning from scratch

### Validation Report Template

```markdown
## ✅ Validation Report

**Validated by**: Validator Agent
**Date**: [Timestamp]
**Reviewed**: Analysis Report + Implementation Strategy

---

### 1. Risk Assessment

#### Risk Scoring Matrix

| Dimension | Score | Reasoning |
|-----------|-------|-----------|
| **Technical Feasibility** | [1-5] | [Why this score] |
| **Complexity** | [1-5] | [Why this score] |
| **Dependencies** | [1-5] | [Why this score] |
| **Time Estimate** | [1-5] | [Why this score] |
| **Reversibility** | [1-5] | [Why this score] |
| **OVERALL** | **[Avg]** | **[Low/Medium/High/Critical]** |

#### Risk Level: [🟢 LOW | 🟡 MEDIUM | 🟠 HIGH | 🔴 CRITICAL]

**Summary**: [1-2 sentence risk overview]

---

### 2. Validation Checklist

#### Analysis Quality
- [ ] ✅ All major components identified
- [ ] ✅ Dependencies comprehensive
- [ ] ✅ Risks realistic and complete
- [ ] ⚠️ Impact areas thorough [or: ❌ Issue found - see below]
- [ ] ✅ No obvious blind spots

#### Strategy Quality
- [ ] ✅ Approach addresses all risks
- [ ] ✅ Architectural decisions justified
- [ ] ✅ Trade-offs explicitly stated
- [ ] ✅ Phases logically sequenced
- [ ] ✅ Tasks specific and actionable
- [ ] ⚠️ Success criteria measurable [or: ❌ Issue]
- [ ] ✅ Rollback strategy viable

#### Completeness
- [ ] ✅ Testing strategy adequate
- [ ] ✅ Error handling considered
- [ ] ✅ Performance implications addressed
- [ ] ✅ Security considerations included
- [ ] ✅ Documentation plan clear
- [ ] ⚠️ Monitoring/observability covered [or: ❌ Issue]

#### Feasibility
- [ ] ✅ Timeline realistic
- [ ] ✅ Required knowledge available
- [ ] ✅ Dependencies obtainable
- [ ] ✅ Resources sufficient
- [ ] ✅ No blockers overlooked

**Checklist Score**: [X/Y items passing]

---

### 3. Issues Found

#### 🚨 Critical Issues (Must Fix Before Approval)

[If none: "None identified ✓"]

[If present:]
##### 1. [Critical Issue Title]
- **Problem**: [Specific issue description]
- **Impact**: [Why this blocks execution]
- **Evidence**: [Reference to code, analysis, or strategy section]
- **Required Fix**: [What must change]

##### 2. [Next Critical Issue]
[Same format]

---

#### ⚠️ Major Concerns (Should Fix)

[If none: "None identified ✓"]

[If present:]
##### 1. [Major Concern Title]
- **Problem**: [Specific concern description]
- **Impact**: [Why this is significant]
- **Location**: [Where in the plan]
- **Recommendation**: [How to improve]

##### 2. [Next Major Concern]
[Same format]

---

#### 🔶 Minor Suggestions (Nice to Have)

[If none: "None - plan is thorough ✓"]

[If present:]
- **[Suggestion 1]**: [Brief description and benefit]
- **[Suggestion 2]**: [Brief description and benefit]

---

### 4. Cross-Validation

#### Analysis ↔ Strategy Alignment

**Risks from Analysis addressed in Strategy?**
- [Risk 1]: ✅ Addressed in [Phase X.Y]
- [Risk 2]: ⚠️ Partially addressed - [note]
- [Risk 3]: ❌ Not addressed - **MAJOR CONCERN**

**Dependencies mapped to tasks?**
- [Dependency 1]: ✅ Task 1.2
- [Dependency 2]: ✅ Task 2.1
- [Dependency 3]: ⚠️ Mentioned but no specific task

**Impact areas covered by phases?**
- [Component A]: ✅ Phase 2
- [Component B]: ✅ Phase 2
- [Component C]: ⚠️ Not in plan - is this intentional?

---

### 5. Spot Checks

[Validator should do quick verification of claims]

**Claim from Analysis**: "File X uses pattern Y"
- **Verification**: [Grepped and confirmed / Could not verify / Incorrect]

**Claim from Strategy**: "Similar implementation in module Z"
- **Verification**: [Read file and confirmed / Patterns don't match]

**Task estimate**: "Task 2.3 estimated as low complexity"
- **Assessment**: [Agrees / Seems underestimated because...]

---

### 6. Alternative Assessment

**Alternatives considered**: [Yes ✅ / Insufficient ⚠️ / None ❌]

[If present:]
- Alternative approach [X] was dismissed for [reason] - **Assessment**: [Justified ✅ / Should reconsider ⚠️]

[If insufficient:]
- **Concern**: Should also consider [alternative approach]
- **Why**: [Benefits of this alternative]

---

### 7. Final Decision

**Status**: [Choose one]
- ✅ **APPROVED** - Ready for user confirmation and implementation
- 🔄 **NEEDS REVISION** - Address issues and re-validate
- ❌ **REJECTED** - Fundamental flaws, restart analysis/planning

---

#### [If APPROVED ✅]

**Approval Statement**:
The plan is thorough, feasible, and addresses all identified risks. Ready to present to user for final approval.

**Strengths**:
- [Key strength 1]
- [Key strength 2]
- [Key strength 3]

**Recommendations for Implementation**:
- [Tip 1 for execution]
- [Tip 2 for execution]

**Next Steps**:
1. Present consolidated plan to user
2. Get user approval
3. Begin Phase 1 implementation
4. Validate after each phase

---

#### [If NEEDS REVISION 🔄]

**Required Changes**:

1. **[Issue Area]**
   - **Problem**: [What's wrong]
   - **Fix**: [What needs to change]
   - **Who**: [Analyzer / Planner]

2. **[Next Issue Area]**
   [Same format]

**After Revision**:
- Re-run: [Analyzer / Planner / Both]
- Re-validate: Yes, full validation required

---

#### [If REJECTED ❌]

**Rejection Reasons**:

1. **[Critical Flaw]**: [Explanation]
2. **[Critical Flaw]**: [Explanation]

**Recommendation**:
[Restart from Analysis / Restart from Planning / Need user clarification]

**What Needs to Change Fundamentally**:
[High-level guidance on new direction]

---

**Validation Complete** ✓
```

---

## Common Patterns & Tips

### When to Iterate

**Iterate if:**
- Validator finds critical or major issues
- Assumptions in analysis were wrong
- User provides new information
- Technical constraints discovered during planning

**Don't iterate if:**
- Only minor suggestions remain
- Perfect is the enemy of good
- Validator has approved

### Handling Ambiguity

If user request is unclear:

1. **Analyzer**: Flag ambiguities in "Open Questions" section
2. **Orchestrator**: Use AskUserQuestion tool immediately
3. **Don't guess**: Better to clarify than to plan wrong thing

### Managing Scope Creep

**Analyzer**: Focus only on what's needed for user request
**Planner**: Use YAGNI - don't plan for hypothetical features
**Validator**: Call out scope creep in "Major Concerns"

### Token Efficiency

If running low on tokens:

- Use symbol communication from token efficiency mode
- Reference previous sections by ID instead of repeating
- Focus on critical information only
- Skip minor suggestions

### Quality Signals

**Good planning shows:**
- Specific file paths and line numbers
- Concrete examples
- Measured success criteria
- Realistic risk assessment
- Clear decision rationale

**Poor planning shows:**
- Vague descriptions
- Unverified assumptions
- Missing error handling
- Unrealistic estimates
- No rollback plan

---

## Agent Communication Protocol

### Analyzer → Planner Handoff

```markdown
## Handoff to Planner

**Analysis Summary**: [2-3 sentences]

**Key Findings**:
1. [Finding 1]
2. [Finding 2]
3. [Finding 3]

**Planning Guidance**:
- **Recommended Approach**: [High-level suggestion]
- **Avoid**: [Known pitfalls]
- **Focus On**: [Critical aspects]

**Open Questions for User**: [If any]
```

### Planner → Validator Handoff

```markdown
## Handoff to Validator

**Strategy Summary**: [2-3 sentences]

**Key Decisions**:
1. [Decision 1] - [Rationale]
2. [Decision 2] - [Rationale]

**Validation Priorities**:
- **Please verify**: [Specific claims to check]
- **Pay attention to**: [Areas of uncertainty]
- **Risk areas**: [Where things could go wrong]
```

### Validator → Iteration Handoff

```markdown
## Feedback for Iteration

**Decision**: [NEEDS REVISION / REJECTED]

**Primary Issues**:
1. [Issue 1] - **For Analyzer/Planner**: [Specific action needed]
2. [Issue 2] - **For Analyzer/Planner**: [Specific action needed]

**Focus Areas for Re-run**:
- [Specific area 1]
- [Specific area 2]

**Keep from Previous**:
[Parts that don't need to change]
```

---

## Troubleshooting

### "Analyzer can't find relevant code"

**Solution**: Use more specific search terms or explore broader areas first

### "Planner creates too many phases"

**Solution**: Combine related work - aim for 3-5 phases maximum

### "Validator keeps rejecting"

**Solution**: Check if validator is being too strict - some risk is acceptable

### "Iteration loop not converging"

**Solution**: After 2 iterations, pause and ask user for input

### "Plan is too detailed"

**Solution**: Remove low-value details - focus on critical decisions and risks

### "Plan is too vague"

**Solution**: Add specific file paths, function names, concrete examples

---

This reference should be consulted by each agent during their phase to ensure comprehensive, consistent, high-quality planning.
