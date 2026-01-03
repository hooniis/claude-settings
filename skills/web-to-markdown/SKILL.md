---
name: generating-markdown-from-web
description: Fetches web page content and converts it to clean, well-structured markdown files. Use when the user provides a URL and asks to generate a markdown document, convert a webpage to markdown, or extract documentation content.
---

# Web to Markdown Generator

$ARGUMENTS

## Instructions

Convert web page content into clean, readable markdown files.

### Workflow

1. **Fetch the webpage** using WebFetch tool with the provided URL
2. **Extract the main content** - focus on the article/documentation body, ignore navigation, footers, ads
3. **Preserve the original language** - keep content in the source webpage's language by default
4. **Convert to markdown** following the format guidelines below
5. **Save the file** with an appropriate filename based on the page title or content

### Language Handling

- **Default behavior**: Preserve the original language of the web page content
- **Translation**: Only translate to another language when the user explicitly requests it
  - Example: "Convert to markdown in Korean" or "markdown으로 변환해줘"
- When translating, maintain technical terms and code examples in their original form

### Markdown Conversion Rules

#### Headings
- Preserve the heading hierarchy (h1 → `#`, h2 → `##`, etc.)
- Use a single `#` for the main title
- Add `---` separator after major sections for readability

#### Text Formatting
- **Bold** for emphasis or key terms
- *Italic* for definitions or secondary emphasis
- `inline code` for technical terms, file names, commands

#### Lists
- Use `-` for unordered lists
- Use `1.` for ordered/numbered lists
- Preserve nested list indentation

#### Code Blocks
- Use triple backticks with language identifier
- Preserve original indentation

```python
# Example code block
def example():
    pass
```

#### Tables
- Convert HTML tables to markdown table syntax
- Align columns appropriately

| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| Data | Data | Data |

#### Links
- Convert to markdown link syntax: `[text](url)`
- For internal documentation links, preserve relative paths
- For external links, use full URLs

#### Special Elements
- Notes, warnings, tips: Use blockquote with prefix

> **Note**: Important information here.

> **Warning**: Critical warning here.

- Collapsible sections: Use `<details>` HTML

<details>
<summary>Click to expand</summary>

Hidden content here.

</details>

#### Images
- Convert to markdown image syntax: `![alt text](url)`
- Include descriptive alt text

### Output Guidelines

1. **Clean structure**: Remove redundant whitespace, ensure consistent spacing
2. **Preserve meaning**: Keep all important content, don't summarize unless asked
3. **Readable formatting**: Add blank lines between sections
4. **No boilerplate**: Exclude navigation menus, footers, cookie banners, related links sections

### File Naming

Generate filename from:
- Page title (kebab-case): `agent-skills-overview.md`
- Or use the last path segment of the URL

## Example

**Input**: User provides URL `https://docs.example.com/guide/getting-started`

**Output**: File `getting-started.md` containing:

```markdown
# Getting Started

Brief introduction paragraph.

---

## Prerequisites

- Item 1
- Item 2

---

## Installation

Install the package:

```bash
npm install example-package
```

## Configuration

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `debug` | boolean | `false` | Enable debug mode |

> **Note**: Configuration is optional for basic usage.

---

## Next Steps

- [Advanced Guide](./advanced-guide.md)
- [API Reference](./api-reference.md)
```
