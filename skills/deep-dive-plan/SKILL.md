---
name: deep-dive-plan
description: Multi-agent collaborative planning system using Analyzer, Planner, and Validator agents for thorough pre-implementation analysis. Use when complex features need deep analysis before coding.
---

# Deep Dive Planning System

$ARGUMENTS

## Overview

This skill orchestrates three specialized agents to produce comprehensive implementation plans before writing any code. The agents collaborate iteratively to ensure thorough analysis, solid planning, and validated strategies.

**Use this skill when:**
- Complex features requiring architectural decisions
- High-risk changes needing careful analysis
- Multi-component system modifications
- Unclear implementation paths requiring exploration
- Need for documented decision-making process

**Do NOT use for:**
- Simple bug fixes or trivial changes
- Well-understood patterns with clear implementation
- Quick prototypes or experiments

## Three-Agent System

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  🔍 ANALYZER  →  📋 PLANNER  →  ✅ VALIDATOR               │
│      ↓             ↓              ↓                         │
│   Findings    →  Strategy   →  Approval/Reject             │
│      ↑             ↑              ↓                         │
│      └─────────────┴──────────────┘                        │
│            Iterate until validated                          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 🔍 Analyzer Agent

**Role**: Deep codebase exploration and current state analysis

**Responsibilities:**
1. Explore existing code patterns and architecture
2. Identify dependencies and integration points
3. Discover constraints and technical debt
4. Assess risks and potential blockers
5. Map out impact areas

**Tools to use:**
- Task agent with subagent_type=Explore for codebase exploration
- Grep for pattern searching
- Read for understanding existing implementations
- Bash for running analysis commands (git log, dependency checks)

**Output format:**
```markdown
## 🔍 Analysis Report

### Current State
[What exists now, architecture overview]

### Dependencies
- Internal: [Components/modules affected]
- External: [Libraries, services, APIs]

### Constraints
- Technical: [Language, framework limitations]
- Business: [Performance, compliance requirements]

### Risks Identified
- 🚨 Critical: [Blockers, breaking changes]
- ⚠️ High: [Major technical debt, complex refactors]
- 🔶 Medium: [Minor issues, edge cases]

### Impact Areas
[Files, components, systems affected]
```

### 📋 Planner Agent

**Role**: Strategic implementation planning based on analysis

**Responsibilities:**
1. Review Analyzer's findings
2. Design implementation strategy
3. Break down into phases and tasks
4. Prioritize and sequence work
5. Document architectural decisions
6. Identify alternative approaches

**Tools to use:**
- Sequential thinking for complex reasoning
- Read for reviewing Analyzer's report
- Write for creating strategy documents

**Output format:**
```markdown
## 📋 Implementation Strategy

### Approach
[High-level strategy and rationale]

### Architectural Decisions
1. **Decision**: [What was decided]
   - **Rationale**: [Why this approach]
   - **Trade-offs**: [Pros and cons]
   - **Alternatives considered**: [Other options]

### Implementation Phases

#### Phase 1: [Foundation/Preparation]
**Goal**: [What this phase achieves]
**Tasks:**
1. Task 1.1: [Specific deliverable]
   - Actions: [Concrete steps]
   - Files: [What to modify]
   - Dependencies: [Prerequisites]
2. Task 1.2: [Next deliverable]
   ...

#### Phase 2: [Core Implementation]
...

#### Phase 3: [Integration/Testing]
...

### Success Criteria
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

### Rollback Strategy
[How to undo changes if needed]
```

### ✅ Validator Agent

**Role**: Critical evaluation and risk assessment

**Responsibilities:**
1. Review Planner's strategy
2. Verify against Analyzer's findings
3. Check for missing considerations
4. Assess feasibility and risks
5. Approve or request revision with specific feedback

**Tools to use:**
- Read for reviewing both Analysis and Plan
- Grep for verifying claims about codebase
- Bash for running quick validation checks

**Output format:**
```markdown
## ✅ Validation Report

### Risk Assessment
**Overall Risk Score**: [Low/Medium/High/Critical]

**Risk Breakdown:**
- **Technical Feasibility**: [1-5] - [Reasoning]
- **Complexity**: [1-5] - [Reasoning]
- **Dependencies**: [1-5] - [Reasoning]
- **Time Estimate**: [1-5] - [Reasoning]
- **Reversibility**: [1-5] - [Reasoning]

### Validation Checklist
- [ ] All risks from Analysis addressed in Plan
- [ ] Dependencies properly sequenced
- [ ] Success criteria are measurable
- [ ] Rollback strategy is viable
- [ ] Architecture decisions are justified
- [ ] Alternative approaches considered
- [ ] Impact areas all covered

### Issues Found
#### 🚨 Critical Issues (Must Fix)
[Issues that make plan unexecutable]

#### ⚠️ Major Concerns (Should Fix)
[Significant gaps or risks]

#### 🔶 Minor Suggestions (Nice to Have)
[Improvements but not blockers]

### Decision
**Status**: [✅ APPROVED | ❌ REJECTED | 🔄 NEEDS REVISION]

**Reasoning**: [Why this decision]

**Required Actions**: [If rejected/needs revision, what must change]
```

## Workflow

**CRITICAL: Multi-Agent Execution Rules**

1. **ALWAYS use Task tool** - Never execute agent logic directly
2. **Run Analyzer → Planner sequentially** - Planner needs Analyzer output
3. **Validator runs after both** - Reviews both Analysis and Plan
4. **Store agent outputs** - Save each agent's output to reference in next agent
5. **Iterate based on Validator** - Only re-run failed agents, not all three

### Step 1: Initialize

Start by understanding the user's request and determining scope.

```markdown
**User Request**: [Summarize what user wants]
**Scope**: [file | module | project | system]
**Estimated Complexity**: [Low | Medium | High | Critical]
```

### Step 2: Launch Analyzer Agent

**IMPORTANT**: Use the Task tool to invoke the Analyzer agent. Do NOT perform analysis yourself.

Invoke the **🔍 Analyzer Agent**:

```
Use Task tool with subagent_type="general-purpose" and this prompt:

"You are the Analyzer agent for deep-dive planning. Your job is to thoroughly explore and analyze the codebase for: [USER REQUEST]

**Your Role**: Deep codebase exploration and current state analysis

**Required Tasks**:
1. Use Task agent with subagent_type=Explore to map project structure and patterns
2. Use Grep to find relevant code patterns and dependencies
3. Use Read to understand existing implementations
4. Use Bash for analysis commands (git log, dependency checks)

**Output Requirements**:
Produce a comprehensive Analysis Report following this structure:

## 🔍 Analysis Report

### 1. Current State
- Architecture overview
- Relevant code locations with file paths and line numbers
- Existing patterns similar to what's needed

### 2. Dependencies
- Internal: Components/modules affected
- External: Libraries, services, APIs needed
- Infrastructure: Database, environment, hosting

### 3. Constraints
- Technical: Language, framework, performance
- Business: Timeline, compliance, compatibility

### 4. Risks Identified
- 🚨 Critical: Blockers, breaking changes
- ⚠️ High: Major technical debt, complex refactors
- 🔶 Medium: Edge cases, testing challenges
- 🔵 Low: Minor concerns

### 5. Impact Areas
- Files to modify/create
- Components affected (direct/indirect)
- Test coverage impact

### 6. Recommendations for Planner
- Preferred approach
- Approaches to avoid
- Open questions for user

Be thorough. Use Explore agent for codebase discovery. The Planner agent will use your findings to create the strategy."
```

**Wait for Analyzer output before proceeding.**

### Step 3: Launch Planner Agent

**IMPORTANT**: Only run after Analyzer completes. Pass Analyzer's full output to Planner.

Invoke the **📋 Planner Agent**:

```
Use Task tool with subagent_type="general-purpose" and this prompt:

"You are the Planner agent for deep-dive planning. Review the Analyzer's findings and create a comprehensive implementation strategy.

**Your Role**: Strategic implementation planning based on analysis

**Analyzer's Report**:
[PASTE THE COMPLETE ANALYZER OUTPUT HERE]

**Required Tasks**:
1. Review all findings from Analyzer thoroughly
2. Design implementation approach addressing all identified risks
3. Break down work into logical phases (3-5 phases)
4. Document architectural decisions with rationales
5. Create detailed task breakdown for each phase

**Output Requirements**:
Produce an Implementation Strategy following this structure:

## 📋 Implementation Strategy

### 1. Approach
High-level strategy and why this approach

### 2. Architectural Decisions
For each major decision:
- **Decision**: What was decided
- **Options Considered**: Alternatives with pros/cons
- **Rationale**: Why this choice
- **Trade-offs**: What we're accepting

### 3. Implementation Phases
For each phase (typically 3-5):
- **Phase N: [Name]**
  - Goal: What this achieves
  - Tasks: Specific deliverables with actions
  - Testing: How to verify
  - Completion Criteria: When phase is done

### 4. Timeline Estimate
Realistic time estimates per phase

### 5. Success Criteria
Measurable, testable criteria for completion

### 6. Rollback Strategy
How to undo changes if needed

### 7. Risk Mitigation Plan
Address each high/critical risk from Analysis

Be specific. Include file paths, function names, concrete examples. The Validator will review your strategy against the Analysis."
```

**Wait for Planner output before proceeding.**

### Step 4: Launch Validator Agent

**IMPORTANT**: Only run after both Analyzer and Planner complete. Validator reviews both outputs.

Invoke the **✅ Validator Agent**:

```
Use Task tool with subagent_type="general-purpose" and this prompt:

"You are the Validator agent for deep-dive planning. Review both the Analysis and the Plan critically to ensure feasibility and completeness.

**Your Role**: Critical evaluation and risk assessment

**Analyzer's Report**:
[PASTE COMPLETE ANALYZER OUTPUT]

**Planner's Strategy**:
[PASTE COMPLETE PLANNER OUTPUT]

**Required Tasks**:
1. Verify all risks from Analysis are addressed in Plan
2. Check that dependencies are properly sequenced
3. Assess technical feasibility of proposed approach
4. Calculate overall risk score (5 dimensions, 1-5 scale each)
5. Identify critical issues, major concerns, minor suggestions
6. Make final decision: APPROVED, NEEDS REVISION, or REJECTED

**Output Requirements**:
Produce a Validation Report following this structure:

## ✅ Validation Report

### 1. Risk Assessment
Risk scoring matrix (5 dimensions):
- Technical Feasibility: [1-5] - [reasoning]
- Complexity: [1-5] - [reasoning]
- Dependencies: [1-5] - [reasoning]
- Time Estimate: [1-5] - [reasoning]
- Reversibility: [1-5] - [reasoning]
- **Overall**: [average] - [Low/Medium/High/Critical]

### 2. Validation Checklist
- [ ] All risks from Analysis addressed
- [ ] Dependencies properly sequenced
- [ ] Success criteria measurable
- [ ] Rollback strategy viable
- [ ] Architectural decisions justified
- [ ] Alternative approaches considered

### 3. Issues Found
- 🚨 Critical Issues: [Must fix before approval]
- ⚠️ Major Concerns: [Should fix]
- 🔶 Minor Suggestions: [Nice to have]

### 4. Cross-Validation
- Check: Are all risks from Analysis addressed in Plan?
- Check: Are all dependencies mapped to tasks?
- Check: Are all impact areas covered?

### 5. Decision
**Status**: [✅ APPROVED | 🔄 NEEDS REVISION | ❌ REJECTED]

**Reasoning**: [Why this decision]

**Required Actions**: [If not approved, what must change and which agent should re-run]

Be thorough and critical. Don't rubber-stamp. If something is missing or risky, flag it. Your job is to catch problems before implementation."
```

**Wait for Validator output before proceeding.**

### Step 5: Iteration (If Needed)

**Analyze Validator's Decision**:

If Validator returns **✅ APPROVED**: Proceed to Step 6 (Finalization)

If Validator returns **🔄 NEEDS REVISION** or **❌ REJECTED**:

1. **Read Validator's feedback** carefully
2. **Identify which agent(s) need to re-run**:
   - Missing analysis / wrong assumptions → Re-run **Analyzer** with specific focus
   - Flawed strategy / poor decisions → Re-run **Planner** with feedback
   - Need user clarification → Use **AskUserQuestion** tool

3. **Re-run appropriate agent(s)**:
   - Include Validator's specific feedback in the agent prompt
   - Reference original outputs: "Previous analysis showed X, but Validator identified gap Y"
   - Only re-run agents that need changes (don't restart entire process)

4. **Re-run Validator** after changes:
   - Always validate again after any changes
   - Use updated outputs from re-run agents
   - Validator should see iteration history

**Iteration Limit**: Maximum 3 iterations. If still not approved after 3 rounds, ask user for guidance.

### Step 6: Finalization

Once Validator returns **✅ APPROVED**:

1. **Consolidate all three reports** into single comprehensive document
2. **Save to claudedocs/**: `claudedocs/deep-dive-plan-[feature-name].md`
3. **Create executive summary**: 2-3 sentences covering What, Why, How, Risk Level
4. **Present to user**: Show summary with key decisions and recommendations
5. **Get user approval**: Use AskUserQuestion to confirm before any implementation begins

## Output Structure

Save the final approved plan to `claudedocs/deep-dive-plan-[feature-name].md`:

```markdown
# Deep Dive Plan: [Feature Name]

**Created**: [Date]
**Status**: ✅ Validated and Approved
**Overall Risk**: [Low/Medium/High/Critical]

---

## Executive Summary
[2-3 sentences: What, Why, How]

---

## 🔍 Analysis Report
[Full Analyzer output]

---

## 📋 Implementation Strategy
[Full Planner output]

---

## ✅ Validation Report
[Full Validator output]

---

## Next Steps

Ready to implement? Use this plan with:
- `/software-engineer` for implementation
- `/commit` for incremental commits following phases
- `/review` for code review after each phase

**Recommendation**: Implement one phase at a time, validate, then proceed.
```

## Best Practices

1. **Always use Task tool for agents**: Never perform agent work yourself - delegate to Task agents
2. **Sequential execution**: Analyzer → Planner → Validator, never skip or parallelize agents
3. **Pass complete outputs**: Each agent needs full context from previous agents
4. **Let agents work independently**: Don't inject opinions between agent phases
5. **Trust the process**: If Validator rejects, iterate - don't skip validation
6. **Document everything**: All decisions, trade-offs, and rationale must be captured
7. **Be thorough, not fast**: Deep dive means comprehensive, not quick
8. **User approval required**: Always confirm final plan before implementation
9. **One phase at a time**: When implementing, complete and validate each phase fully

## Anti-Patterns to Avoid

❌ **Doing agent work yourself**: Never perform analysis/planning/validation directly - always use Task tool
❌ **Parallel agent execution**: Agents depend on each other's outputs - must run sequentially
❌ **Incomplete context passing**: Each agent needs full output from previous agents
❌ **Skipping Validator**: Never implement without validation approval
❌ **Rushing to code**: This skill is about planning, not implementation
❌ **Ignoring feedback**: Validator feedback must be addressed, not dismissed
❌ **Over-simplifying**: Don't reduce complex problems to simple tasks
❌ **Analysis paralysis**: If Validator approves, move forward - don't over-iterate

## Integration with Other Skills

- **After deep-dive-plan**: Use `/software-engineer` for implementation
- **During implementation**: Use `/review` after each phase
- **For commits**: Use `/commit` with phase-based messages
- **For PRs**: Use `/create-pr` referencing the plan document

---

**Remember**: The goal is to have a validated, comprehensive plan that makes implementation straightforward and low-risk. Invest time in planning to save time in implementation.
