---
name: generating-asciidoc-from-web
description: Fetches web page content and converts it to clean, well-structured AsciiDoc (.adoc) files. Use when the user provides a URL and asks to generate an AsciiDoc document, convert a webpage to adoc format, or extract documentation content in AsciiDoc.
---

# Web to AsciiDoc Generator

$ARGUMENTS

## Instructions

Convert web page content into clean, readable AsciiDoc files.

### Workflow

1. **Fetch the webpage** using WebFetch tool with the provided URL
2. **Extract the main content** - focus on the article/documentation body, ignore navigation, footers, ads
3. **Convert to AsciiDoc** following the syntax guidelines below
4. **Save the file** with `.adoc` extension based on the page title or content

---

## AsciiDoc Conversion Rules

### Document Header

```asciidoc
= Document Title
:toc: auto
:source-highlighter: highlight.js
```

### Headings

Use `=` for headings. Document title uses single `=`, sections start at `==`.

```asciidoc
= Document Title (Level 0)
== Section Level 1
=== Section Level 2
==== Section Level 3
===== Section Level 4
```

### Text Formatting

| HTML/Style | AsciiDoc |
|------------|----------|
| Bold | `*bold text*` |
| Italic | `_italic text_` |
| Bold + Italic | `*_bold italic_*` |
| Inline code | `` `monospace` `` |
| Highlight | `#highlighted#` |
| Strikethrough | `[.line-through]#text#` |
| Underline | `[.underline]#text#` |
| Superscript | `^super^` |
| Subscript | `~sub~` |

For text spanning word boundaries, use doubled markers:

```asciidoc
**bold across**multiple words
__italic across__words
``mono across``words
```

### Lists

**Unordered list:**

```asciidoc
* Item 1
* Item 2
** Nested item
*** Deeper nested
* Item 3
```

**Ordered list:**

```asciidoc
. Step 1
. Step 2
.. Nested step 2a
.. Nested step 2b
. Step 3
```

**Checklist:**

```asciidoc
* [x] Completed task
* [ ] Incomplete task
```

**Description list:**

```asciidoc
Term 1:: Definition of term 1
Term 2:: Definition of term 2
Nested Term::: Nested definition
```

### Links

```asciidoc
https://example.com[Link Text]
link:relative/path.html[Relative Link]
mailto:user@example.com[Email Link]
<<section-id,Cross Reference>>
xref:other-doc.adoc#section[Cross-document Reference]
```

### Images

**Block image (on its own line):**

```asciidoc
.Image Caption
image::path/to/image.png[Alt text, width, height]
```

**Inline image:**

```asciidoc
Click the image:icon.png[icon] button.
```

### Code Blocks

**Source block with syntax highlighting:**

```asciidoc
[source,python]
----
def hello():
    print("Hello, World!")
----
```

**With line numbers:**

```asciidoc
[source,javascript,linenums]
----
function greet(name) {
    return `Hello, ${name}!`;
}
----
```

**With callouts:**

```asciidoc
[source,java]
----
public class Main {
    public static void main(String[] args) { // <1>
        System.out.println("Hello"); // <2>
    }
}
----
<1> Entry point method
<2> Print to console
```

**Literal block (no highlighting):**

```asciidoc
....
Literal text preserved exactly
    including whitespace
....
```

### Tables

**Basic table:**

```asciidoc
[cols="1,2,3"]
|===
|Header 1 |Header 2 |Header 3

|Cell 1A
|Cell 1B
|Cell 1C

|Cell 2A
|Cell 2B
|Cell 2C
|===
```

**Table with header row:**

```asciidoc
[%header,cols="1,1,2"]
|===
|Name |Type |Description
|id |integer |Unique identifier
|name |string |Display name
|===
```

**Table with AsciiDoc content:**

```asciidoc
[cols="1,2a"]
|===
|Column 1
|Column with *bold* and:

* List item 1
* List item 2
|===
```

### Admonitions

**Inline admonitions:**

```asciidoc
NOTE: This is a note.

TIP: This is a helpful tip.

IMPORTANT: This is important information.

WARNING: This is a warning.

CAUTION: Proceed with caution.
```

**Block admonitions (for multi-line content):**

```asciidoc
[NOTE]
====
This is a multi-paragraph note.

It can contain multiple lines and other elements.
====

[WARNING]
====
This warning has multiple paragraphs.

* With a list
* Inside it
====
```

### Blockquotes

```asciidoc
[quote, Author Name, Source]
____
This is the quoted text.
It can span multiple lines.
____
```

**Simple quote (no attribution):**

```asciidoc
____
Anonymous quote text.
____
```

### Sidebar

```asciidoc
.Sidebar Title
****
Sidebar content that appears visually distinct from main content.
****
```

### Example Block

```asciidoc
.Example Title
====
Example content demonstrating something.
====
```

### Collapsible Content

```asciidoc
.Click to expand
[%collapsible]
====
Hidden content revealed on click.
====
```

### Breaks

**Thematic break (horizontal rule):**

```asciidoc
'''
```

**Page break:**

```asciidoc
<<<
```

### IDs and Anchors

**Section with custom ID:**

```asciidoc
[#custom-id]
== Section Title
```

**Inline anchor:**

```asciidoc
[[anchor-name]]This text can be linked to.
```

### Comments

```asciidoc
// Single-line comment (not rendered)

////
Multi-line comment block.
None of this is rendered.
////
```

---

## Output Guidelines

1. **Document header**: Include title with `= Title` and optional attributes (`:toc:`, `:source-highlighter:`)
2. **Clean structure**: Use consistent blank lines between sections
3. **Preserve meaning**: Keep all important content, don't summarize unless asked
4. **No boilerplate**: Exclude navigation menus, footers, cookie banners
5. **Semantic markup**: Use appropriate admonitions for notes, warnings, tips

### File Naming

Generate filename from:
- Page title (kebab-case): `getting-started-guide.adoc`
- Or use the last path segment of the URL

---

## Example

**Input**: User provides URL `https://docs.example.com/guide/quick-start`

**Output**: File `quick-start.adoc` containing:

```asciidoc
= Quick Start Guide
:toc: auto
:source-highlighter: highlight.js

Getting started with Example Framework in minutes.

== Prerequisites

* Node.js 18 or higher
* npm or yarn package manager

== Installation

Install the package using npm:

[source,bash]
----
npm install example-framework
----

Or using yarn:

[source,bash]
----
yarn add example-framework
----

== Basic Usage

[source,javascript]
----
import { createApp } from 'example-framework';

const app = createApp({
  name: 'My App'
});

app.start();
----

NOTE: The `createApp` function returns a Promise in async mode.

== Configuration

[%header,cols="1,1,2"]
|===
|Option |Type |Description
|name |string |Application display name
|debug |boolean |Enable debug logging
|port |number |Server port (default: 3000)
|===

WARNING: Never expose debug mode in production environments.

== Next Steps

* <<advanced-configuration,Advanced Configuration>>
* xref:api-reference.adoc[API Reference]
* https://example.com/examples[Example Projects]
```
