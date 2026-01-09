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

### Step 1: Initialize

Start by understanding the user's request and determining scope.

```markdown
**User Request**: [Summarize what user wants]
**Scope**: [file | module | project | system]
**Estimated Complexity**: [Low | Medium | High | Critical]
```

### Step 2: Analysis Phase

Invoke the **🔍 Analyzer Agent** using the Task tool:

```
Use Task agent with this prompt:
"You are the Analyzer agent for deep-dive planning. Your job is to thoroughly explore and analyze the codebase for [USER REQUEST].

Follow the Analysis Report format from REFERENCE.md. Focus on:
1. Current architecture and patterns
2. All dependencies (internal and external)
3. Technical constraints and limitations
4. Potential risks and blockers
5. Impact areas

Use Explore agent (subagent_type=Explore) for codebase exploration.
Output a comprehensive Analysis Report."
```

### Step 3: Planning Phase

Invoke the **📋 Planner Agent** using the Task tool:

```
Use Task agent with this prompt:
"You are the Planner agent for deep-dive planning. Review the Analyzer's findings and create a comprehensive implementation strategy.

Analysis Report:
[Paste the Analyzer's output here]

Follow the Implementation Strategy format from REFERENCE.md. Include:
1. Clear approach with rationale
2. Documented architectural decisions with trade-offs
3. Phased breakdown (Phase → Task → Actions)
4. Success criteria
5. Rollback strategy

Use Sequential thinking for complex reasoning."
```

### Step 4: Validation Phase

Invoke the **✅ Validator Agent** using the Task tool:

```
Use Task agent with this prompt:
"You are the Validator agent for deep-dive planning. Review both the Analysis and the Plan critically.

Analysis Report:
[Paste Analyzer's output]

Implementation Strategy:
[Paste Planner's output]

Follow the Validation Report format from REFERENCE.md. Assess:
1. Risk score (1-5 scale across 5 dimensions)
2. Validation checklist completion
3. Critical issues, major concerns, minor suggestions
4. Final decision: APPROVED, REJECTED, or NEEDS REVISION

Be thorough and critical. If anything is missing or risky, flag it."
```

### Step 5: Iteration (If Needed)

If Validator returns **REJECTED** or **NEEDS REVISION**:

1. **Analyze the feedback**: What specific issues were raised?
2. **Determine next action**:
   - Missing analysis? → Re-run Analyzer with specific focus areas
   - Flawed strategy? → Re-run Planner with constraints/feedback
   - Need clarification? → Ask user questions

3. **Iterate**: Run the appropriate agent(s) again with the feedback incorporated

4. **Re-validate**: Always re-run Validator after changes

### Step 6: Finalization

Once Validator returns **✅ APPROVED**:

1. **Consolidate documentation**: Combine all three reports into final plan
2. **Save to claudedocs/**: Write comprehensive planning document
3. **Present to user**: Summarize key decisions and next steps
4. **Ask for approval**: Use AskUserQuestion to confirm before any implementation

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

1. **Let agents work independently**: Don't inject opinions between agent phases
2. **Trust the process**: If Validator rejects, iterate - don't skip validation
3. **Document everything**: All decisions, trade-offs, and rationale must be captured
4. **Be thorough, not fast**: Deep dive means comprehensive, not quick
5. **User approval required**: Always confirm final plan before implementation
6. **One phase at a time**: When implementing, complete and validate each phase fully

## Anti-Patterns to Avoid

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
