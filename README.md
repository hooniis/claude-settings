# Claude Settings

A collection of Claude Code configuration templates, rules, and skills.

## Overview

This repository provides reusable configurations for Claude Code to maintain consistent coding standards and workflows across projects.

## Structure

```
claude-settings/
├── .claude/
│   ├── settings.json       # Project settings
│   └── settings.local.json # Local overrides (gitignored)
├── rules/                  # Coding style guides
│   ├── kotlin.md
│   └── typescript.md
├── skills/                 # Custom skills
│   └── code-review/
│       └── SKILL.md
├── templates/              # Reusable templates
│   ├── skill-template.md
│   ├── commit-template.md
│   └── pr-template.md
└── CLAUDE.md               # Project instructions
```

## Rules

Language-specific style guides emphasizing clean, readable code.

| Language | File | Based On |
|----------|------|----------|
| Kotlin | `rules/kotlin.md` | [Kotlin Coding Conventions](https://kotlinlang.org/docs/coding-conventions.html) |
| TypeScript | `rules/typescript.md` | [Google TypeScript Style Guide](https://google.github.io/styleguide/tsguide.html) |

### Core Principles

- Write human-readable, clean code
- Follow OOP, SOLID, and functional principles pragmatically
- **Do not over-engineer** - simple is best
- Do not duplicate code - write reusable code

## Skills

Custom skills for Claude Code automation.

| Skill | Description |
|-------|-------------|
| `code-review` | Comprehensive code review with structured output format |

### Creating a New Skill

1. Copy `templates/skill-template.md`
2. Create folder in `skills/` with skill name
3. Name the file `SKILL.md`

```
skills/
└── my-skill/
    └── SKILL.md
```

## Templates

| Template | Description |
|----------|-------------|
| `skill-template.md` | Template for creating new skills |
| `commit-template.md` | [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) format |
| `pr-template.md` | Pull request template with checklist |

## Usage

### Copy to Your Project

```bash
# Copy rules to your project
cp -r rules/ /path/to/your/project/

# Copy CLAUDE.md
cp CLAUDE.md /path/to/your/project/
```

### Use as Reference

Reference these files in your project's `CLAUDE.md`:

```markdown
## Coding Standards

Follow the Kotlin style guide: [link to rules/kotlin.md]
```

