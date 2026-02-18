
# Kilo important worth knowing //Pulled from latest release kilo docs
# Table of Contents

- [Custom Modes](#custom-modes)
  - [Sticky Models for Efficient Workflow](#sticky-models-for-efficient-workflow)
  - [Why Use Custom Modes?](#why-use-custom-modes)
  - [What's Included in a Custom Mode?](#whats-included-in-a-custom-mode)
  - [Import/Export Modes](#importexport-modes)
    - [Key Features](#key-features)
    - [How it Works](#how-it-works)
    - [Changing Slugs on Import](#changing-slugs-on-import)
  - [Methods for Creating and Configuring Custom Modes](#methods-for-creating-and-configuring-custom-modes)
    - [1. Ask Kilo! (Recommended)](#1-ask-kilo-recommended)
    - [2. Using the Prompts Tab](#2-using-the-prompts-tab)
    - [3. Manual Configuration (YAML & JSON)](#3-manual-configuration-yaml--json)
  - [YAML Configuration Format (Preferred)](#yaml-configuration-format-preferred)
    - [YAML Example](#yaml-example)
    - [JSON Alternative](#json-alternative)
  - [`slug`](#slug)
  - [`name`](#name)
  - [`description`](#description)
  - [`roleDefinition`](#roledefinition)
  - [`groups`](#groups)
  - [`whenToUse` (Optional)](#whentouse-optional)
  - [`customInstructions` (Optional)](#custominstructions-optional)
  - [Benefits of YAML Format](#benefits-of-yaml-format)
  - [Migration to YAML Format](#migration-to-yaml-format)
  - [Mode-Specific Instructions via Files/Directories](#mode-specific-instructions-via-filesdirectories)
  - [Configuration Precedence](#configuration-precedence)
  - [Overriding Default Modes](#overriding-default-modes)
  - [Understanding Regex in Custom Modes](#understanding-regex-in-custom-modes)
    - [Important Rules for `fileRegex`](#important-rules-for-fileregex)
    - [Common Pattern Examples](#common-pattern-examples)
    - [Key Regex Building Blocks](#key-regex-building-blocks)
  - [Error Handling](#error-handling)
  - [Example Configurations](#example-configurations)
  - [Troubleshooting](#troubleshooting)
    - [Common Issues](#common-issues)
    - [Tips for Working with YAML](#tips-for-working-with-yaml)
  - [Community Gallery](#community-gallery)

- [Custom Rules](#custom-rules)
  - [Overview](#overview)
  - [Rule Format](#rule-format)
  - [Rule Types](#rule-types)
  - [Rule Location](#rule-location)
    - [Project Rules](#project-rules)
    - [Global Rules](#global-rules)
  - [Managing Rules Through the UI](#managing-rules-through-the-ui)
  - [Rule Loading Order](#rule-loading-order)
    - [General Rules (Any Mode)](#general-rules-any-mode)
    - [Mode-Specific Rules](#mode-specific-rules)
  - [Creating Custom Rules](#creating-custom-rules)
    - [Using the UI Interface](#using-the-ui-interface)
    - [Using the File System](#using-the-file-system)
  - [Example Rules](#example-rules)
  - [Use Cases](#use-cases)
  - [Examples of Custom Rules](#examples-of-custom-rules)
  - [Best Practices](#best-practices)
  - [Limitations](#limitations)
  - [Related Features](#related-features-1)

- [Custom Instructions](#custom-instructions)
  - [What Are Custom Instructions?](#what-are-custom-instructions)
  - [Setting Custom Instructions](#setting-custom-instructions)
    - [Mode-Specific Instructions](#mode-specific-instructions)
  - [Related Features](#related-features-2)

- [AGENTS.md](#agentsmd)
  - [What is AGENTS.md?](#what-is-agentsmd)
  - [Why Use AGENTS.md?](#why-use-agentsmd)
  - [File Location and Naming](#file-location-and-naming)
    - [Project-Level AGENTS.md](#project-level-agentsmd)
    - [Subdirectory AGENTS.md Files](#subdirectory-agentsmd-files)
  - [File Protection](#file-protection)
  - [Basic Syntax and Structure](#basic-syntax-and-structure)
    - [Recommended Structure](#recommended-structure)
  - [Best Practices](#best-practices-1)
  - [How AGENTS.md Works in Kilo Code](#how-agentsmd-works-in-kilo-code)
    - [Loading Behavior](#loading-behavior)
    - [Interaction with Other Rules](#interaction-with-other-rules)
    - [Enabling/Disabling AGENTS.md](#enablingdisabling-agentsmd)
  - [Related Features](#related-features-3)
  - [External Resources](#external-resources)

- [Skills](#skills)
  - [What Are Agent Skills?](#what-are-agent-skills)
    - [Key Benefits](#key-benefits)
  - [How Skills Work in Kilo Code](#how-skills-work-in-kilo-code)
    - [How the Agent Decides to Use a Skill](#how-the-agent-decides-to-use-a-skill)
  - [Skill Locations](#skill-locations)
    - [Global Skills (User-Level)](#global-skills-user-level)
    - [Project Skills (Workspace-Level)](#project-skills-workspace-level)
  - [Mode-Specific Skills](#mode-specific-skills-1)
  - [Priority and Overrides](#priority-and-overrides)
  - [When Skills Are Loaded](#when-skills-are-loaded)
  - [Using Symlinks](#using-symlinks)
  - [SKILL.md Format](#skillmd-format)
    - [Frontmatter Fields](#frontmatter-fields)
    - [Example with Optional Fields](#example-with-optional-fields)
    - [Name Matching Rule](#name-matching-rule)
  - [Optional Bundled Resources](#optional-bundled-resources)
  - [Example: Creating a Skill](#example-creating-a-skill)
  - [Finding Skills](#finding-skills)
  - [Troubleshooting](#troubleshooting-2)
    - [Skill Not Loading?](#skill-not-loading)
    - [Verifying a Skill is Available](#verifying-a-skill-is-available)
    - [Checking if a Skill Was Used](#checking-if-a-skill-was-used)
    - [Common Errors](#common-errors)
  - [Contributing to the Marketplace](#contributing-to-the-marketplace)
    - [How to Submit Your Skill](#how-to-submit-your-skill)
    - [Submission Guidelines](#submission-guidelines)
  - [Related](#related)

- [Workflows](#workflows)
  - [Creating Workflows](#creating-workflows)
    - [Basic Setup](#basic-setup)
    - [Workflow Capabilities](#workflow-capabilities)
  - [Common Workflow Patterns](#common-workflow-patterns)
  - [Example: PR Submission Workflow](#example-pr-submission-workflow)


  ____          _                    __  __           _           
 / ___|   _ ___| |_ ___  _ __ ___   |  \/  | ___   __| | ___  ___ 
| |  | | | / __| __/ _ \| '_ ` _ \  | |\/| |/ _ \ / _` |/ _ \/ __|
| |__| |_| \__ \ || (_) | | | | | | | |  | | (_) | (_| |  __/\__ \
 \____\__,_|___/\__\___/|_| |_| |_| |_|  |_|\___/ \__,_|\___||___/
                                                                  
---
title: "Custom Modes"
description: "Create and configure custom modes in Kilo Code"
---
---

# Custom Modes

Kilo Code allows you to create **custom modes** to tailor Kilo's behavior to specific tasks or workflows. Custom modes can be either **global** (available across all projects) or **project-specific** (defined within a single project).

## Sticky Models for Efficient Workflow

Each mode—including custom ones—features **Sticky Models**. This means Kilo Code automatically remembers and selects the last model you used with a particular mode. This lets you assign different preferred models to different tasks without constant reconfiguration, as Kilo switches between models when you change modes.

## Why Use Custom Modes?

- **Specialization:** Create modes optimized for specific tasks, like "Documentation Writer," "Test Engineer," or "Refactoring Expert"
- **Safety:** Restrict a mode's access to sensitive files or commands. For example, a "Review Mode" could be limited to read-only operations
- **Experimentation:** Safely experiment with different prompts and configurations without affecting other modes
- **Team Collaboration:** Share custom modes with your team to standardize workflows

{% callout type="tip" %}
**Keep custom modes on track:** Limit the types of files that they're allowed to edit using the `fileRegex` option in the `groups` configuration. This prevents modes from accidentally modifying files outside their intended scope.
{% /callout %}

{% image src="/docs/img/custom-modes/custom-modes.png" alt="Overview of custom modes interface" width="600" caption="Overview of custom modes interface" /%}

_Kilo Code's interface for creating and managing custom modes._

## What's Included in a Custom Mode?

Custom modes are defined by several key properties. Understanding these concepts will help you tailor Kilo's behavior effectively.

| UI Field / YAML Property                       | Conceptual Description                                                                                                                                                               |
| ---------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Slug** (`slug`)                              | A unique internal identifier for the mode. Used by Kilo Code to reference the mode, especially for associating mode-specific instruction files.                                      |
| **Name** (`name`)                              | The display name for the mode as it appears in the Kilo Code user interface. Should be human-readable and descriptive.                                                               |
| **Description** (`description`)                | A short, user-friendly summary of the mode's purpose displayed in the mode selector UI. Keep this concise and focused on what the mode does for the user.                            |
| **Role Definition** (`roleDefinition`)         | Defines the core identity and expertise of the mode. This text is placed at the beginning of the system prompt and defines Kilo's personality and behavior when this mode is active. |
| **Available Tools** (`groups`)                 | Defines the allowed toolsets and file access permissions for the mode. Corresponds to selecting which general categories of tools the mode can use.                                  |
| **When to Use** (`whenToUse`)                  | _(Optional)_ Provides guidance for Kilo's automated decision-making, particularly for mode selection and task orchestration. Used by the Orchestrator mode for task coordination.    |
| **Custom Instructions** (`customInstructions`) | _(Optional)_ Specific behavioral guidelines or rules for the mode. Added near the end of the system prompt to further refine Kilo's behavior.                                        |

{% callout type="tip" %}
**Power Steering for Better Mode Adherence**

If you find that models aren't following your custom mode's role definition or instructions closely enough, enable the [Power Steering](/docs/getting-started/settings#power-steering) experimental feature. This reminds the model about mode details more frequently, leading to stronger adherence to your custom configurations at the cost of increased token usage.
{% /callout %}

## Import/Export Modes

Easily share, back up, and template your custom modes. This feature lets you export any mode—and its associated rules—into a single, portable YAML file that you can import into any project.

### Key Features

- **Shareable Setups:** Package a mode and its rules into one file to easily share with your team
- **Easy Backups:** Save your custom mode configurations so you never lose them
- **Project Templates:** Create standardized mode templates for different types of projects
- **Simple Migration:** Move modes between your global settings and specific projects effortlessly
- **Flexible Slug Changes:** Change mode slugs in exported files without manual path editing

### How it Works

**Exporting a Mode:**

Modes are accessed from the Prompts tab (notebook icon), which contains the Modes section.

1. Open the Prompts Tab (click the <Codicon name="notebook" /> icon in the top menu bar)
2. Select the mode you wish to export
3. Click the Export Mode button (download icon)
4. Choose a location to save the `.yaml` file
5. Kilo packages the mode's configuration and any rules into the YAML file

**Importing a Mode:**

1. Open the Prompts Tab (click the <Codicon name="notebook" /> icon in the top menu bar)
2. Click the Import Mode button (upload icon)
3. Select the mode's YAML file
4. Choose the import level:
    - **Project:** Available only in current workspace (saved to `.kilocodemodes` file)
    - **Global:** Available in all projects (saved to global settings)

### Changing Slugs on Import

When importing modes, you can change the slug in the exported YAML file before importing:

1. Export a mode with slug `original-mode`
2. Edit the YAML file and change the slug to `new-mode`
3. Import the file - the import process will automatically update rule file paths to match the new slug

## Methods for Creating and Configuring Custom Modes

You can create and configure custom modes in several ways:

### 1. Ask Kilo! (Recommended)

You can quickly create a basic custom mode by asking Kilo Code to do it for you. For example:

```
Create a new mode called "Documentation Writer". It should only be able to read files and write Markdown files.
```

Kilo Code will guide you through the process, prompting for necessary information and creating the mode using the preferred YAML format.

{% callout type="tip" %}
**Create modes from job postings:** If there's a real world job posting for something you want a custom mode to do, try asking Code mode to `Create a custom mode based on the job posting at @[url]`. This can help you quickly create specialized modes with realistic role definitions.
{% /callout %}

### 2. Using the Prompts Tab

1. **Open Prompts Tab:** Click the <Codicon name="notebook" /> icon in the Kilo Code top menu bar
2. **Create New Mode:** Click the <Codicon name="add" /> button to the right of the Modes heading
3. **Fill in Fields:**

{% image src="/docs/img/custom-modes/custom-modes-2.png" alt="Custom mode creation interface in the Prompts tab" width="600" caption="Custom mode creation interface in the Prompts tab" /%}

_The custom mode creation interface showing fields for name, slug, description, save location, role definition, available tools, custom instructions._

The interface provides fields for Name, Slug, Description, Save Location, Role Definition, When to Use (optional), Available Tools, and Custom Instructions. After filling these, click the "Create Mode" button. Kilo Code will save the new mode in YAML format.

### 3. Manual Configuration (YAML & JSON)

You can directly edit the configuration files to create or modify custom modes. This method offers the most control over all properties. Kilo Code now supports both YAML (preferred) and JSON formats.

- **Global Modes:** Edit the `custom_modes.yaml` (preferred) or `custom_modes.json` file. Access it via Prompts Tab > <Codicon name="gear" /> (Settings Menu icon next to "Global Prompts") > "Edit Global Modes"
- **Project Modes:** Edit the `.kilocodemodes` file (which can be YAML or JSON) in your project root. Access it via Prompts Tab > <Codicon name="gear" /> (Settings Menu icon next to "Project Prompts") > "Edit Project Modes"

These files define an array/list of custom modes.

## YAML Configuration Format (Preferred)

YAML is now the preferred format for defining custom modes due to better readability, comment support, and cleaner multi-line strings.

### YAML Example

```yaml
customModes:
    - slug: docs-writer
      name: 📝 Documentation Writer
      description: A specialized mode for writing and editing technical documentation.
      roleDefinition: You are a technical writer specializing in clear documentation.
      whenToUse: Use this mode for writing and editing documentation.
      customInstructions: Focus on clarity and completeness in documentation.
      groups:
          - read
          - - edit # First element of tuple
            - fileRegex: \.(md|mdx)$ # Second element is the options object
              description: Markdown files only
          - browser
    - slug: another-mode
      name: Another Mode
      # ... other properties
```

### JSON Alternative

```json
{
	"customModes": [
		{
			"slug": "docs-writer",
			"name": "📝 Documentation Writer",
			"description": "A specialized mode for writing and editing technical documentation.",
			"roleDefinition": "You are a technical writer specializing in clear documentation.",
			"whenToUse": "Use this mode for writing and editing documentation.",
			"customInstructions": "Focus on clarity and completeness in documentation.",
			"groups": [
				"read",
				["edit", { "fileRegex": "\\.(md|mdx)$", "description": "Markdown files only" }],
				"browser"
			]
		}
	]
}
```

## YAML/JSON Property Details

### `slug`

- **Purpose:** A unique identifier for the mode
- **Format:** Must match the pattern `/^[a-zA-Z0-9-]+$/` (only letters, numbers, and hyphens)
- **Usage:** Used internally and in file/directory names for mode-specific rules (e.g., `.kilo/rules-{slug}/`)
- **Recommendation:** Keep it short and descriptive

**YAML Example:** `slug: docs-writer`
**JSON Example:** `"slug": "docs-writer"`

### `name`

- **Purpose:** The display name shown in the Kilo Code UI
- **Format:** Can include spaces and proper capitalization

**YAML Example:** `name: 📝 Documentation Writer`
**JSON Example:** `"name": "Documentation Writer"`

### `description`

- **Purpose:** A short, user-friendly summary displayed below the mode name in the mode selector UI
- **Format:** Keep this concise and focused on what the mode does for the user
- **UI Display:** This text appears in the redesigned mode selector

**YAML Example:** `description: A specialized mode for writing and editing technical documentation.`
**JSON Example:** `"description": "A specialized mode for writing and editing technical documentation."`

### `roleDefinition`

- **Purpose:** Detailed description of the mode's role, expertise, and personality
- **Placement:** This text is placed at the beginning of the system prompt when the mode is active

**YAML Example (multi-line):**

```yaml
roleDefinition: >-
    You are a test engineer with expertise in:
    - Writing comprehensive test suites
    - Test-driven development
```

**JSON Example:** `"roleDefinition": "You are a technical writer specializing in clear documentation."`

### `groups`

- **Purpose:** Array/list defining which tool groups the mode can access and any file restrictions
- **Available Tool Groups:** `"read"`, `"edit"`, `"browser"`, `"command"`, `"mcp"`
- **Structure:**
    - Simple string for unrestricted access: `"edit"`
    - Tuple (two-element array) for restricted access: `["edit", { fileRegex: "pattern", description: "optional" }]`

**File Restrictions for "edit" group:**

- `fileRegex`: A regular expression string to control which files the mode can edit
- In YAML, typically use single backslashes for regex special characters (e.g., `\.md$`)
- In JSON, backslashes must be double-escaped (e.g., `\\.md$`)
- `description`: An optional string describing the restriction

**YAML Example:**

```yaml
groups:
    - read
    - - edit # First element of tuple
      - fileRegex: \.(js|ts)$ # Second element is the options object
        description: JS/TS files only
    - command
```

**JSON Example:**

```json
"groups": [
  "read",
  ["edit", { "fileRegex": "\\.(js|ts)$", "description": "JS/TS files only" }],
  "command"
]
```

### `whenToUse` (Optional)

- **Purpose:** Provides guidance for Kilo's automated decision-making, particularly for mode selection and task orchestration
- **Format:** A string describing ideal scenarios or task types for this mode
- **Usage:** Used by Kilo for automated decisions and not displayed in the mode selector UI

**YAML Example:** `whenToUse: This mode is best for refactoring Python code.`
**JSON Example:** `"whenToUse": "This mode is best for refactoring Python code."`

### `customInstructions` (Optional)

- **Purpose:** A string containing additional behavioral guidelines for the mode
- **Placement:** This text is added near the end of the system prompt

**YAML Example (multi-line):**

```yaml
customInstructions: |-
    When writing tests:
    - Use describe/it blocks
    - Include meaningful descriptions
```

**JSON Example:** `"customInstructions": "Focus on explaining concepts and providing examples."`

## Benefits of YAML Format

YAML is now the preferred format for defining custom modes due to several advantages:

- **Readability:** YAML's indentation-based structure is easier for humans to read and understand
- **Comments:** YAML allows for comments (lines starting with `#`), making it possible to annotate your mode definitions
- **Multi-line Strings:** YAML provides cleaner syntax for multi-line strings using `|` (literal block) or `>` (folded block)
- **Less Punctuation:** YAML generally requires less punctuation compared to JSON, reducing syntax errors
- **Editor Support:** Most modern code editors provide excellent syntax highlighting and validation for YAML files

While JSON is still fully supported, new modes created via the UI or by asking Kilo will default to YAML.

## Migration to YAML Format

### Global Modes

Automatic migration from `custom_modes.json` to `custom_modes.yaml` happens when:

- Kilo Code starts up
- A `custom_modes.json` file exists
- No `custom_modes.yaml` file exists yet

The migration process preserves the original JSON file for rollback purposes.

### Project Modes (`.kilocodemodes`)

- No automatic startup migration occurs for project-specific files
- Kilo Code can read `.kilocodemodes` files in either YAML or JSON format
- When editing through the UI, JSON files will be converted to YAML format
- For manual conversion, you can ask Kilo to help reformat configurations

## Mode-Specific Instructions via Files/Directories

You can provide instructions for custom modes using dedicated files or directories within your workspace, allowing for better organization and version control.

### Preferred Method: Directory (`.kilo/rules-{mode-slug}/`)

```
.
├── .kilo/
│   └── rules-docs-writer/  # Example for mode slug "docs-writer"
│       ├── 01-style-guide.md
│       └── 02-formatting.txt
└── ... (other project files)
```

### Fallback Method: Single File (`.kilorules-{mode-slug}`)

```
.
├── .kilorules-docs-writer  # Example for mode slug "docs-writer"
└── ... (other project files)
```

**Rules Directory Scope:**

- **Global modes:** Rules are stored in `~/.kilo/rules-{slug}/`
- **Project modes:** Rules are stored in `{workspace}/.kilo/rules-{slug}/`

The directory method takes precedence if it exists and contains files. Files within the directory are read recursively and appended in alphabetical order.

## Configuration Precedence

Mode configurations are applied in this order:

1. **Project-level mode configurations** (from `.kilocodemodes` - YAML or JSON)
2. **Global mode configurations** (from `custom_modes.yaml`, then `custom_modes.json` if YAML not found)
3. **Default mode configurations**

**Important:** When modes with the same slug exist in both `.kilocodemodes` and global settings, the `.kilocodemodes` version completely overrides the global one for ALL properties.

## Overriding Default Modes

You can override Kilo Code's built-in modes (like 💻 Code, 🪲 Debug, ❓ Ask, 🏗️ Architect, 🪃 Orchestrator) by creating a custom mode with the same slug.

### Global Override Example

```yaml
customModes:
    - slug: code # Matches the default 'code' mode slug
      name: 💻 Code (Global Override)
      roleDefinition: You are a software engineer with global-specific constraints.
      whenToUse: This globally overridden code mode is for JS/TS tasks.
      customInstructions: Focus on project-specific JS/TS development.
      groups:
          - read
          - - edit
            - fileRegex: \.(js|ts)$
              description: JS/TS files only
```

### Project-Specific Override Example

```yaml
customModes:
    - slug: code # Matches the default 'code' mode slug
      name: 💻 Code (Project-Specific)
      roleDefinition: You are a software engineer with project-specific constraints for this project.
      whenToUse: This project-specific code mode is for Python tasks within this project.
      customInstructions: Adhere to PEP8 and use type hints.
      groups:
          - read
          - - edit
            - fileRegex: \.py$
              description: Python files only
          - command
```

## Understanding Regex in Custom Modes

Regular expressions (`fileRegex`) offer fine-grained control over file editing permissions.

{% callout type="tip" %}

**Let Kilo Build Your Regex Patterns**

Instead of writing complex regex manually, ask Kilo:

```
Create a regex pattern that matches JavaScript files but excludes test files
```

Kilo will generate the pattern. Remember to adapt it for YAML (usually single backslashes) or JSON (double backslashes).

{% /callout %}

### Important Rules for `fileRegex`

- **Escaping in JSON:** In JSON strings, backslashes (`\`) must be double-escaped (e.g., `\\.md$`)
- **Escaping in YAML:** In unquoted or single-quoted YAML strings, a single backslash is usually sufficient for regex special characters (e.g., `\.md$`)
- **Path Matching:** Patterns match against the full relative file path from your workspace root
- **Case Sensitivity:** Regex patterns are case-sensitive by default
- **Validation:** Invalid regex patterns are rejected with an "Invalid regular expression pattern" error message

### Common Pattern Examples

| Pattern (YAML-like)              | JSON fileRegex Value                | Matches                                   | Doesn't Match                      |
| -------------------------------- | ----------------------------------- | ----------------------------------------- | ---------------------------------- |
| `\.md$`                          | `"\\.md$"`                          | `readme.md`, `docs/guide.md`              | `script.js`, `readme.md.bak`       |
| `^src/.*`                        | `"^src/.*"`                         | `src/app.js`, `src/components/button.tsx` | `lib/utils.js`, `test/src/mock.js` |
| `\.(css\|scss)$`                 | `"\\.(css\|scss)$"`                 | `styles.css`, `theme.scss`                | `styles.less`, `styles.css.map`    |
| `docs/.*\.md$`                   | `"docs/.*\\.md$"`                   | `docs/guide.md`, `docs/api/reference.md`  | `guide.md`, `src/docs/notes.md`    |
| `^(?!.*(test\|spec))\.(js\|ts)$` | `"^(?!.*(test\|spec))\\.(js\|ts)$"` | `app.js`, `utils.ts`                      | `app.test.js`, `utils.spec.js`     |

### Key Regex Building Blocks

- `\.`: Matches a literal dot (YAML: `\.`, JSON: `\\.`)
- `$`: Matches the end of the string
- `^`: Matches the beginning of the string
- `.*`: Matches any character (except newline) zero or more times
- `(a|b)`: Matches either "a" or "b"
- `(?!...)`: Negative lookahead

## Error Handling

When a mode attempts to edit a file that doesn't match its `fileRegex` pattern, you'll see a `FileRestrictionError` that includes:

- The mode name
- The allowed file pattern
- The description (if provided)
- The attempted file path
- The tool that was blocked

## Example Configurations

### Basic Documentation Writer (YAML)

```yaml
customModes:
    - slug: docs-writer
      name: 📝 Documentation Writer
      description: Specialized for writing and editing technical documentation
      roleDefinition: You are a technical writer specializing in clear documentation
      groups:
          - read
          - - edit
            - fileRegex: \.md$
              description: Markdown files only
      customInstructions: Focus on clear explanations and examples
```

### Test Engineer with File Restrictions (YAML)

```yaml
customModes:
    - slug: test-engineer
      name: 🧪 Test Engineer
      description: Focused on writing and maintaining test suites
      roleDefinition: You are a test engineer focused on code quality
      whenToUse: Use for writing tests, debugging test failures, and improving test coverage
      groups:
          - read
          - - edit
            - fileRegex: \.(test|spec)\.(js|ts)$
              description: Test files only
          - command
```

### Security Review Mode (YAML)

```yaml
customModes:
    - slug: security-review
      name: 🔒 Security Reviewer
      description: Read-only security analysis and vulnerability assessment
      roleDefinition: You are a security specialist reviewing code for vulnerabilities
      whenToUse: Use for security reviews and vulnerability assessments
      customInstructions: |-
          Focus on:
          - Input validation issues
          - Authentication and authorization flaws
          - Data exposure risks
          - Injection vulnerabilities
      groups:
          - read
          - browser
```

## Troubleshooting

### Common Issues

- **Mode not appearing:** After creating or importing a mode, you may need to reload the VS Code window
- **Invalid regex patterns:** Test your patterns using online regex testers before applying them
- **Precedence confusion:** Remember that project modes completely override global modes with the same slug
- **YAML syntax errors:** Use proper indentation (spaces, not tabs) and validate your YAML

### Tips for Working with YAML

- **Indentation is Key:** YAML uses indentation (spaces, not tabs) to define structure
- **Colons for Key-Value Pairs:** Keys must be followed by a colon and a space (e.g., `slug: my-mode`)
- **Hyphens for List Items:** List items start with a hyphen and a space (e.g., `- read`)
- **Validate Your YAML:** Use online YAML validators or your editor's built-in validation

## Community Gallery

Ready to explore more? Check out the [Show and Tell](https://github.com/Kilo-Org/kilocode/discussions/categories/show-and-tell) to discover and share custom modes created by the community!


===============================================================================================================================================================================================================================

                _                               _           
  ___ _   _ ___| |_ ___  _ __ ___    _ __ _   _| | ___  ___ 
 / __| | | / __| __/ _ \| '_ ` _ \  | '__| | | | |/ _ \/ __|
| (__| |_| \__ \ || (_) | | | | | | | |  | |_| | |  __/\__ \
 \___|\__,_|___/\__\___/|_| |_| |_| |_|   \__,_|_|\___||___/
                                                            
---
title: "Custom Rules"
description: "Define custom rules for Kilo Code behavior"
---

# Custom Rules

Custom rules provide a powerful way to define project-specific and global behaviors and constraints for the Kilo Code AI agent. With custom rules, you can ensure consistent formatting, restrict access to sensitive files, enforce coding standards, and customize the AI's behavior for your specific project needs or across all projects.

## Overview

Custom rules allow you to create text-based instructions that all AI models will follow when interacting with your project. These rules act as guardrails and conventions that are consistently respected across all interactions with your codebase. Rules can be managed through both the file system and the built-in UI interface.

## Rule Format

Custom rules can be written in plain text, but Markdown format is recommended for better structure and comprehension by the AI models. The structured nature of Markdown helps the models parse and understand your rules more effectively.

- Use Markdown headers (`#`, `##`, etc.) to define rule categories
- Use lists (`-`, `*`) to enumerate specific items or constraints
- Use code blocks (` `) to include code examples when needed

## Rule Types

Kilo Code supports two types of custom rules:

- **Project Rules**: Apply only to the current project workspace
- **Global Rules**: Apply across all projects and workspaces

{% callout type="note" title="UI Support" %}
The built-in rules management UI is available for general rules only. Mode-specific rules must be managed through the file system.
{% /callout %}

## Rule Location

### Project Rules

Custom rules are primarily loaded from the **`.kilocode/rules/` directory**. This is the recommended approach for organizing your project-specific rules. Each rule is typically placed in its own Markdown file with a descriptive name:

```
project/
├── .kilocode/
│   ├── rules/
│   │   ├── formatting.md
│   │   ├── restricted_files.md
│   │   └── naming_conventions.md
├── src/
└── ...
```

### Global Rules

Global rules are stored in your home directory and apply to all projects:

```
~/.kilocode/
├── rules/
│   ├── coding_standards.md
│   ├── security_guidelines.md
│   └── documentation_style.md
```

## Managing Rules Through the UI

Kilo Code provides a built-in interface for managing your custom rules without manually editing files in the `.kilocode/rules/` directories. To access the UI, click on the <Codicon name="law" /> icon in the **bottom right corner** of the Kilo Code window.

You can access the rules management UI to:

- View all active rules (both project and global)
- Toggle rules on/off without deleting them
- Create and edit rules directly in the interface
- Organize rules by category and priority

## Rule Loading Order

### General Rules (Any Mode)

Rules are loaded in the following priority order:

1. **Global rules** from `~/.kilocode/rules/` directory
2. **Project rules** from `.kilocode/rules/` directory
3. **Legacy fallback files** (for backward compatibility):
    - `.roorules`
    - `.clinerules`
    - `.kilocoderules` (deprecated)

When both global and project rules exist, they are combined with project rules taking precedence over global rules for conflicting directives.

{% callout type="note" %}
We strongly recommend keeping your rules in the `.kilocode/rules/` folder as it provides better organization and is the preferred approach for future versions. The folder-based structure allows for more granular rule organization and clearer separation of concerns. The legacy file-based approach is maintained for backward compatibility but may be subject to change in future releases.
{% /callout %}

### Mode-Specific Rules

Additionally, the system supports mode-specific rules, which are loaded separately and have their own priority order:

1. First, it checks for `.kilocode/rules-${mode}/` directory
2. If that doesn't exist or is empty, it falls back to `.kilocoderules-${mode}` file (deprecated)

Currently, mode-specific rules are only supported at the project level.
When both generic rules and mode-specific rules exist, the mode-specific rules are given priority in the final output.

## Creating Custom Rules

### Using the UI Interface

{% image src="/docs/img/custom-rules/rules-ui.png" alt="Rules tab in Kilo Code" width="400" /%}

The easiest way to create and manage rules is through the built-in UI:

1. Access the rules management interface from the Kilo Code panel
2. Choose between creating project-specific or global rules
3. Use the interface to create, edit, or toggle rules
4. Rules are automatically saved and applied immediately

### Using the File System

To create rules manually:

**For Project Rules:**

1. Create the `.kilocode/rules/` directory if it doesn't already exist
2. Create a new Markdown file with a descriptive name in this directory
3. Write your rule using Markdown formatting
4. Save the file

**For Global Rules:**

1. Create the `~/.kilocode/rules/` directory if it doesn't already exist
2. Create a new Markdown file with a descriptive name in this directory
3. Write your rule using Markdown formatting
4. Save the file

Rules will be automatically applied to all future Kilo Code interactions. Any new changes will be applied immediately.

## Example Rules

### Example 1: Table Formatting

```markdown
# Tables

When printing tables, always add an exclamation mark to each column header
```

This simple rule instructs the AI to add exclamation marks to all table column headers when generating tables in your project.

### Example 2: Restricted File Access

```markdown
# Restricted files

Files in the list contain sensitive data, they MUST NOT be read

- supersecrets.txt
- credentials.json
- .env
```

This rule prevents the AI from reading or accessing sensitive files, even if explicitly requested to do so.

{% image src="/docs/img/custom-rules/custom-rules.png" alt="Kilo Code ignores request to read sensitive file" width="600" /%}

## Use Cases

Custom rules can be applied to a wide variety of scenarios:

- **Code Style**: Enforce consistent formatting, naming conventions, and documentation styles
- **Security Controls**: Prevent access to sensitive files or directories
- **Project Structure**: Define where different types of files should be created
- **Documentation Requirements**: Specify documentation formats and requirements
- **Testing Patterns**: Define how tests should be structured
- **API Usage**: Specify how APIs should be used and documented
- **Error Handling**: Define error handling conventions

## Examples of Custom Rules

- "Strictly follow code style guide [your project-specific code style guide]"
- "Always use spaces for indentation, with a width of 4 spaces"
- "Use camelCase for variable names"
- "Write unit tests for all new functions"
- "Explain your reasoning before providing code"
- "Focus on code readability and maintainability"
- "Prioritize using the most common library in the community"
- "When adding new features to websites, ensure they are responsive and accessible"

## Best Practices

- **Be Specific**: Clearly define the scope and intent of each rule
- **Use Categories**: Organize related rules under common headers
- **Separate Concerns**: Use different files for different types of rules
- **Use Examples**: Include examples to illustrate the expected behavior
- **Keep It Simple**: Rules should be concise and easy to understand
- **Update Regularly**: Review and update rules as project requirements change

{% callout type="tip" title="Pro Tip: File-Based Team Standards" %}
When working in team environments, placing `.kilocode/rules/codestyle.md` files under version control allows you to standardize Kilo's behavior across your entire development team. This ensures consistent code style, documentation practices, and development workflows for everyone on the project.
{% /callout %}

## Limitations

- Rules are applied on a best-effort basis by the AI models
- Complex rules may require multiple examples for clear understanding
- Project rules apply only to the project in which they are defined
- Global rules apply across all projects

## Troubleshooting

If your custom rules aren't being properly followed:

1. **Check rule status in the UI**: Use the rules management interface to verify that your rules are active and properly loaded
1. **Verify rule formatting**: Ensure that your rules are properly formatted with clear Markdown structure
1. **Check rule locations**: Ensure that your rules are located in supported locations:
    - Global rules: `~/.kilocode/rules/` directory
    - Project rules: `.kilocode/rules/` directory
    - Legacy files: `.kilocoderules`, `.roorules`, or `.clinerules`
1. **Rule specificity**: Verify that the rules are specific and unambiguous
1. **Restart VS Code**: Restart VS Code to ensure the rules are properly loaded

## Related Features

- [Custom Modes](/docs/customize/custom-modes)
- [Custom Instructions](/docs/customize/custom-instructions)
- [Settings Management](/docs/getting-started/settings)
- [Auto-Approval Settings](/docs/features/auto-approving-actions)

===============================================================================
============================================================================================

   ____          _                  
 / ___|   _ ___| |_ ___  _ __ ___  
| |  | | | / __| __/ _ \| '_ ` _ \ 
| |__| |_| \__ \ || (_) | | | | | |
 \____\__,_|___/\__\___/|_| |_| |_|
                                   
 ___           _                   _   _                 
|_ _|_ __  ___| |_ _ __ _   _  ___| |_(_) ___  _ __  ___ 
 | || '_ \/ __| __| '__| | | |/ __| __| |/ _ \| '_ \/ __|
 | || | | \__ \ |_| |  | |_| | (__| |_| | (_) | | | \__ \
|___|_| |_|___/\__|_|   \__,_|\___|\__|_|\___/|_| |_|___/
                                                         
---
title: "Custom Instructions"
description: "Provide custom instructions to guide Kilo Code"
---

# Custom Instructions

Custom Instructions allow you to personalize how Kilo Code behaves, providing specific guidance that shapes responses, coding style, and decision-making processes.

## What Are Custom Instructions?

Custom Instructions define specific Extension behaviors, preferences, and constraints beyond Kilo's basic role definition. Examples include coding style, documentation standards, testing requirements, and workflow guidelines.

{% callout type="info" title="Custom Instructions vs Rules" %}
Custom Instructions are IDE-wide and are applied across all workspaces and maintain your preferences regardless of which project you're working on. Unlike Instructions, [Custom Rules](/docs/customize/custom-rules) are project specific and allow you to setup workspace-based ruleset.
{% /callout %}

## Setting Custom Instructions

**How to set them:**

{% image src="/docs/img/custom-instructions/custom-instructions.png" alt="Kilo Code Modes tab showing global custom instructions interface" width="600" caption="Kilo Code Modes tab showing global custom instructions interface" /%}

1.  **Open Modes Tab:** Click the <Codicon name="organization" /> icon in the Kilo Code top menu bar
2.  **Find Section:** Find the "Custom Instructions for All Modes" section
3.  **Enter Instructions:** Enter your instructions in the text area
4.  **Save Changes:** Click "Done" to save your changes

#### Mode-Specific Instructions

Mode-specific instructions can be set using the Modes Tab

    {% image src="/docs/img/custom-instructions/custom-instructions-3.png" alt="Kilo Code Modes tab showing mode-specific custom instructions interface" width="600" caption="Kilo Code Modes tab showing mode-specific custom instructions interface" /%}
    * **Open Tab:** Click the <Codicon name="organization" /> icon in the Kilo Code top menu bar
    * **Select Mode:** Under the Modes heading, click the button for the mode you want to customize
    * **Enter Instructions:** Enter your instructions in the text area under "Mode-specific Custom Instructions (optional)"
    * **Save Changes:** Click "Done" to save your changes

        {% callout type="info" title="Global Mode Rules" %}
        If the mode itself is global (not workspace-specific), any custom instructions you set for it will also apply globally for that mode across all workspaces.
        {% /callout %}

## Related Features

- [Custom Modes](/docs/customize/custom-modes)
- [Custom Rules](/docs/customize/custom-rules)
- [Settings Management](/docs/getting-started/settings)
- [Auto-Approval Settings](/docs/features/auto-approving-actions)

===============================================================================
===============================================================================

                        _                       _ 
  __ _  __ _  ___ _ __ | |_ ___   _ __ ___   __| |
 / _` |/ _` |/ _ \ '_ \| __/ __| | '_ ` _ \ / _` |
| (_| | (_| |  __/ | | | |_\__ \_| | | | | | (_| |
 \__,_|\__, |\___|_| |_|\__|___(_)_| |_| |_|\__,_|
       |___/                                      

# AGENTS.md
---
title: "Agents.md"
description: "Project-level configuration with agents.md files"
---

# agents.md

AGENTS.md files provide a standardized way to configure AI agent behavior across different AI coding tools. They allow you to define project-specific instructions, coding standards, and guidelines that AI agents should follow when working with your codebase.

{% callout type="note" title="Memory Bank Deprecation" %}
The Kilo Code **memory bank** feature has been deprecated in favor of AGENTS.md.

**Existing memory bank rules will continue to work.**

Legacy Memory Bank status indicators such as `[Memory Bank: Active]` and `[Memory Bank: Missing]` can still appear, but they are not guaranteed across all clients or modes.

If you'd like to migrate your memory bank content to AGENTS.md:

1. Examine the contents in `.kilocode/rules/memory-bank/`
2. Move that content into your project's `AGENTS.md` file (or ask Kilo to do it for you)
   {% /callout %}

## What is AGENTS.md?

AGENTS.md is an open standard for configuring AI agent behavior in software projects. It's a simple Markdown file placed at the root of your project that contains instructions for AI coding assistants. The standard is supported by multiple AI coding tools, including Kilo Code, Cursor, and Windsurf.

Think of AGENTS.md as a "README for AI agents" - it tells the AI how to work with your specific project, what conventions to follow, and what constraints to respect.

## Why Use AGENTS.md?

- **Portability**: Works across multiple AI coding tools without modification
- **Version Control**: Lives in your repository alongside your code
- **Team Consistency**: Ensures all team members' AI assistants follow the same guidelines
- **Project-Specific**: Tailored to your project's unique requirements and conventions
- **Simple Format**: Plain Markdown - no special syntax or configuration required

## File Location and Naming

### Project-Level AGENTS.md

Place your AGENTS.md file at the **root of your project**:

```
my-project/
├── AGENTS.md          # Primary filename (recommended)
├── src/
├── package.json
└── README.md
```

**Supported filenames** (in order of precedence):

1. `AGENTS.md` (uppercase, plural - recommended)
2. `AGENT.md` (uppercase, singular - fallback)

{% callout type="warning" title="Case Sensitivity" %}
The filename must be uppercase (`AGENTS.md`), not lowercase (`agents.md`). This ensures consistency across different operating systems and tools.
{% /callout %}

### Subdirectory AGENTS.md Files

You can also place AGENTS.md files in subdirectories to provide context-specific instructions:

```
my-project/
├── AGENTS.md                    # Root-level instructions
├── src/
│   └── backend/
│       └── AGENTS.md            # Backend-specific instructions
└── docs/
    └── AGENTS.md                # Documentation-specific instructions
```

When working in a subdirectory, Kilo Code will load both the root AGENTS.md and any subdirectory AGENTS.md files, with subdirectory files taking precedence for conflicting instructions.

## File Protection

Both `AGENTS.md` and `AGENT.md` are **write-protected files** in Kilo Code. This means:

- The AI agent cannot modify these files without explicit user approval
- You'll be prompted to confirm any changes to these files
- This prevents accidental modifications to your project's AI configuration

## Basic Syntax and Structure

AGENTS.md files use standard Markdown syntax. There's no required structure, but organizing your content with headers and lists makes it easier for AI models to parse and understand.

### Recommended Structure

```markdown
# Project Name

Brief description of the project and its purpose.

## Code Style

- Use TypeScript for all new files
- Follow ESLint configuration
- Use 2 spaces for indentation

## Architecture

- Follow MVC pattern
- Keep components under 200 lines
- Use dependency injection

## Testing

- Write unit tests for all business logic
- Maintain >80% code coverage
- Use Jest for testing

## Security

- Never commit API keys or secrets
- Validate all user inputs
- Use parameterized queries for database access
```

## Best Practices

- **Be specific and clear** - Use concrete rules like "limit cyclomatic complexity to < 10" instead of vague guidance like "write good code"
- **Include code examples** - Show patterns for error handling, naming conventions, or architecture decisions
- **Organize by category** - Group related guidelines under clear headers (Code Style, Architecture, Testing, Security)
- **Keep it concise** - Use bullet points and direct language; avoid long paragraphs
- **Update regularly** - Review and revise as your project's conventions evolve

## How AGENTS.md Works in Kilo Code

### Loading Behavior

When you start a task in Kilo Code:

1. Kilo Code checks for `AGENTS.md` or `AGENT.md` at the project root
2. If found, the content is loaded and included in the AI's context
3. The AI follows these instructions throughout the conversation
4. Changes to AGENTS.md take effect in new tasks (reload may be required)

### Interaction with Other Rules

AGENTS.md works alongside Kilo Code's other configuration systems:

| Feature                                                        | Scope   | Location                  | Purpose                                   | Priority    |
| -------------------------------------------------------------- | ------- | ------------------------- | ----------------------------------------- | ----------- |
| **[Mode-specific Custom Rules](/docs/customize/custom-rules)** | Project | `.kilocode/rules-{mode}/` | Mode-specific rules and constraints       | 1 (Highest) |
| **[Custom Rules](/docs/customize/custom-rules)**               | Project | `.kilocode/rules/`        | Kilo Code-specific rules and constraints  | 2           |
| **[AGENTS.md](/docs/customize/agents-md)**                     | Project | `AGENTS.md`               | Universal standard for any AI coding tool | 3           |
| **[Global Custom Rules](/docs/customize/custom-rules)**        | Global  | `~/.kilocode/rules/`      | Global Kilo Code rules                    | 4           |
| **[Custom Instructions](/docs/customize/custom-instructions)** | Global  | IDE settings              | Personal preferences across all projects  | 5 (Lowest)  |

### Enabling/Disabling AGENTS.md

AGENTS.md support is **enabled by default** in Kilo Code. To disable it, edit `settings.json`:

```json
{
	"kilocode.useAgentRules": false
}
```

## Related Features

- **[Custom Rules](/docs/customize/custom-rules)** - Kilo Code-specific rules with more control
- **[Custom Modes](/docs/customize/custom-modes)** - Specialized workflows with specific permissions
- **[Custom Instructions](/docs/customize/custom-instructions)** - Personal preferences across all projects
- **[Migrating from Cursor or Windsurf](/docs/getting-started/migrating)** - Migration guide for other tools

## External Resources

- [AGENTS.md Specification](https://agents.md) - Official standard documentation
- [dotagent](https://github.com/johnlindquist/dotagent) - Universal converter tool for agent configuration files
- [awesome-cursorrules](https://github.com/PatrickJS/awesome-cursorrules) - 700+ example rules you can adapt

===================================================================================
========================

 ____  _  _____ _     _     ____  
/ ___|| |/ /_ _| |   | |   / ___| 
\___ \| ' / | || |   | |   \___ \ 
 ___) | . \ | || |___| |___ ___) |
|____/|_|\_\___|_____|_____|____/ 
                                  
# SKILLS.md
---
title: "Skills"
description: "Extend Kilo Code capabilities with skills"
---

# Skills

Kilo Code implements [Agent Skills](https://agentskills.io/), a lightweight, open format for extending AI agent capabilities with specialized knowledge and workflows.

## What Are Agent Skills?

Agent Skills package domain expertise, new capabilities, and repeatable workflows that agents can use. At its core, a skill is a folder containing a `SKILL.md` file with metadata and instructions that tell an agent how to perform a specific task.

This approach keeps agents fast while giving them access to more context on demand. When a task matches a skill's description, the agent reads the full instructions into context and follows them—optionally loading referenced files or executing bundled code as needed.

### Key Benefits

- **Self-documenting**: A skill author or user can read a `SKILL.md` file and understand what it does, making skills easy to audit and improve
- **Interoperable**: Skills work across any agent that implements the [Agent Skills specification](https://agentskills.io/specification)
- **Extensible**: Skills can range in complexity from simple text instructions to bundled scripts, templates, and reference materials
- **Shareable**: Skills are portable and can be easily shared between projects and developers

## How Skills Work in Kilo Code

Skills can be:

- **Generic** - Available in all modes
- **Mode-specific** - Only loaded when using a particular mode (e.g., `code`, `architect`)

The workflow is:

1. **Discovery**: Skills are scanned from designated directories when Kilo Code initializes. Only the metadata (name, description, and file path) is read at this stage—not the full instructions.
2. **Prompt inclusion**: When a mode is active, the metadata for relevant skills is included in the system prompt. The agent sees a list of available skills with their descriptions.
3. **On-demand loading**: When the agent determines that a task matches a skill's description, it reads the full `SKILL.md` file into context and follows the instructions.

### How the Agent Decides to Use a Skill

The agent (LLM) decides whether to use a skill based on the skill's `description` field. There's no keyword matching or semantic search—the agent evaluates your request against all available skill descriptions and determines if one "clearly and unambiguously applies."

This means:

- **Description wording matters**: Write descriptions that match how users phrase requests
- **Explicit invocation always works**: Saying "use the api-design skill" will trigger it since the agent sees the skill name
- **Vague descriptions lead to uncertain matching**: Be specific about when the skill should be used

## Skill Locations

Skills are loaded from multiple locations, allowing both personal skills and project-specific instructions.

### Global Skills (User-Level)

Global skills are located in the `.kilocode` directory within your Home directory.

- Mac and Linux: `~/.kilocode/skills/`
- Windows: `\Users\<yourUser>\.kilocode\`

```
~/.kilocode/
├── skills/                    # Generic skills (all modes)
│   ├── my-skill/
│   │   └── SKILL.md
│   └── another-skill/
│       └── SKILL.md
├── skills-code/              # Code mode only
│   └── refactoring/
│       └── SKILL.md
└── skills-architect/         # Architect mode only
    └── system-design/
        └── SKILL.md
```

### Project Skills (Workspace-Level)

Located in `.kilocode/skills/` within your project:

```
your-project/
└── .kilocode/
    ├── skills/               # Generic skills for this project
    │   └── project-conventions/
    │       └── SKILL.md
    └── skills-code/          # Code mode skills for this project
        └── linting-rules/
            └── SKILL.md
```

## Mode-Specific Skills

To create a skill that only appears in a specific mode:

```bash
# For Code mode only
mkdir -p ~/.kilocode/skills-code/typescript-patterns

# For Architect mode only
mkdir -p ~/.kilocode/skills-architect/microservices
```

The directory naming pattern is `skills-{mode-slug}` where `{mode-slug}` matches the mode's identifier (e.g., `code`, `architect`, `ask`, `debug`).

## Priority and Overrides

When multiple skills share the same name, Kilo Code uses these priority rules:

1. **Project skills override global skills** - A project skill with the same name takes precedence
2. **Mode-specific skills override generic skills** - A skill in `skills-code/` overrides the same skill in `skills/` when in Code mode

This allows you to:

- Define global skills for personal use
- Override them per-project when needed
- Customize behavior for specific modes

## When Skills Are Loaded

Skills are discovered when Kilo Code initializes:

- When VSCode starts
- When you reload the VSCode window (`Cmd+Shift+P` → "Developer: Reload Window")

Skills directories are monitored for changes to `SKILL.md` files. However, the most reliable way to pick up new skills is to reload VS or the Kilo Code extension.

**Adding or modifying skills requires reloading VSCode for changes to take effect.**

## Using Symlinks

You can symlink skills directories to share skills across machines or from a central repository. When using symlinks, the skill's `name` field must match the **symlink name**, not the target directory name.

## SKILL.md Format

The `SKILL.md` file uses YAML frontmatter followed by Markdown content containing the instructions:

```markdown
---
name: my-skill-name
description: A brief description of what this skill does and when to use it
---

# Instructions

Your detailed instructions for the AI agent go here.

The agent will read this content when it decides to use the skill based on
your request matching the description above.

## Example Usage

You can include examples, guidelines, code snippets, etc.
```

### Frontmatter Fields

Per the [Agent Skills specification](https://agentskills.io/specification):

| Field           | Required | Description                                                                                           |
| --------------- | -------- | ----------------------------------------------------------------------------------------------------- |
| `name`          | Yes      | Max 64 characters. Lowercase letters, numbers, and hyphens only. Must not start or end with a hyphen. |
| `description`   | Yes      | Max 1024 characters. Describes what the skill does and when to use it.                                |
| `license`       | No       | License name or reference to a bundled license file                                                   |
| `compatibility` | No       | Environment requirements (intended product, system packages, network access, etc.)                    |
| `metadata`      | No       | Arbitrary key-value mapping for additional metadata                                                   |

### Example with Optional Fields

```markdown
---
name: pdf-processing
description: Extract text and tables from PDF files, fill forms, merge documents.
license: Apache-2.0
metadata:
    author: example-org
    version: 1.0.0
---

## How to extract text

1. Use pdfplumber for text extraction...

## How to fill forms

...
```

### Name Matching Rule

In Kilo Code, the `name` field **must match** the parent directory name:

```
✅ Correct:
skills/
└── frontend-design/
    └── SKILL.md  # name: frontend-design

❌ Incorrect:
skills/
└── frontend-design/
    └── SKILL.md  # name: my-frontend-skill  (doesn't match!)
```

## Optional Bundled Resources

While `SKILL.md` is the only required file, you can optionally include additional directories to support your skill:

```
my-skill/
├── SKILL.md           # Required: instructions + metadata
├── scripts/           # Optional: executable code
├── references/        # Optional: documentation
└── assets/            # Optional: templates, resources
```

These additional files can be referenced from your skill's instructions, allowing the agent to read documentation, execute scripts, or use templates as needed.

## Example: Creating a Skill

1. Create the skill directory:

    ```bash
    mkdir -p ~/.kilocode/skills/api-design
    ```

2. Create `SKILL.md`:

    ```markdown
    ---
    name: api-design
    description: REST API design best practices and conventions
    ---

    # API Design Guidelines

    When designing REST APIs, follow these conventions:

    ## URL Structure

    - Use plural nouns for resources: `/users`, `/orders`
    - Use kebab-case for multi-word resources: `/order-items`
    - Nest related resources: `/users/{id}/orders`

    ## HTTP Methods

    - GET: Retrieve resources
    - POST: Create new resources
    - PUT: Replace entire resource
    - PATCH: Partial update
    - DELETE: Remove resource

    ## Response Codes

    - 200: Success
    - 201: Created
    - 400: Bad Request
    - 404: Not Found
    - 500: Server Error
    ```

3. Reload VSCode to load the skill

4. The skill will now be available in all modes

## Finding Skills

You can discover and install community-created skills through:

- **Kilo Marketplace** - Browse skills directly in the Kilo Code extension via the Marketplace tab, or explore the [Kilo Marketplace repository](https://github.com/Kilo-Org/kilo-marketplace) on GitHub
- [Agent Skills Specification](https://agentskills.io/home) - The open specification that skills follow, enabling interoperability across different AI agents

## Troubleshooting

### Skill Not Loading?

1. **Check the Output panel**: Open `View` → `Output` → Select "Kilo Code" from dropdown. Look for skill-related errors.

2. **Verify frontmatter**: Ensure `name` exactly matches the directory name and `description` is present.

3. **Reload VSCode**: Skills are loaded at startup. Use `Cmd+Shift+P` → "Developer: Reload Window".

4. **Check file location**: Ensure `SKILL.md` is directly inside the skill directory, not nested further.

### Verifying a Skill is Available

To confirm a skill is properly loaded and available to the agent, you can ask the agent directly. Simply send a message like:

- "Do you have access to skill X?"
- "Is the skill called X loaded?"
- "What skills do you have available?"

The agent will respond with information about whether the skill is loaded and accessible. This is the most reliable way to verify that a skill is available after adding it or reloading VSCode.

If the agent confirms the skill is available, you're ready to use it. If not, check the troubleshooting steps above to identify and resolve the issue.

### Checking if a Skill Was Used

To see if a skill was actually used during a conversation, look for a `read_file` tool call in the chat that targets a `SKILL.md` file. When the agent decides to use a skill, it reads the full skill file into context—this appears as a file read operation in the conversation.

There's currently no dedicated UI indicator showing "Skill X was activated." The `read_file` call is the most reliable way to confirm a skill was used.

### Common Errors

| Error                           | Cause                                        | Solution                                         |
| ------------------------------- | -------------------------------------------- | ------------------------------------------------ |
| "missing required 'name' field" | No `name` in frontmatter                     | Add `name: your-skill-name`                      |
| "name doesn't match directory"  | Mismatch between frontmatter and folder name | Make `name` match exactly                        |
| Skill not appearing             | Wrong directory structure                    | Verify path follows `skills/skill-name/SKILL.md` |

## Contributing to the Marketplace

Have you created a skill that others might find useful? Share it with the community by contributing to the [Kilo Marketplace](https://github.com/Kilo-Org/kilo-marketplace)!

### How to Submit Your Skill

1. **Prepare your skill**: Ensure your skill directory contains a valid `SKILL.md` file with proper frontmatter
2. **Test thoroughly**: Verify your skill works correctly across different scenarios and modes
3. **Fork the marketplace repository**: Visit [github.com/Kilo-Org/kilo-marketplace](https://github.com/Kilo-Org/kilo-marketplace) and create a fork
4. **Add your skill**: Place your skill directory in the appropriate location following the repository's structure
5. **Submit a pull request**: Create a PR with a clear description of what your skill does and when it's useful

### Submission Guidelines

- Follow the [Agent Skills specification](https://agentskills.io/specification) for your `SKILL.md` file
- Include a clear `name` and `description` in the frontmatter
- Document any dependencies or requirements (scripts, external tools, etc.)
- If your skill includes bundled resources (scripts, templates), ensure they are well-documented
- Follow the [contribution guidelines](https://github.com/Kilo-Org/kilo-marketplace/blob/main/CONTRIBUTING.md) in the marketplace repository

For more details on contributing to Kilo Code, see the [Contributing Guide](/docs/contributing).

## Related

- [Custom Modes](/docs/customize/custom-modes) - Create custom modes that can use specific skills
- [Custom Instructions](/docs/customize/custom-instructions) - Global instructions vs. skill-based instructions
- [Custom Rules](/docs/customize/custom-rules) - Project-level rules complementing skills


===============================================================================
============================
===================================================


                    _     __ _                   
__      _____  _ __| | __/ _| | _____      _____ 
\ \ /\ / / _ \| '__| |/ / |_| |/ _ \ \ /\ / / __|
 \ V  V / (_) | |  |   <|  _| | (_) \ V  V /\__ \
  \_/\_/ \___/|_|  |_|\_\_| |_|\___/ \_/\_/ |___/
                                                 
---
title: "Workflows"
description: "Create automated workflows with Kilo Code"
---

# Workflows

Workflows automate repetitive tasks by defining step-by-step instructions for Kilo Code to execute. Invoke any workflow by typing `/[workflow-name.md]` in the chat.

{% image src="/docs/img/slash-commands/workflows.png" alt="Workflows tab in Kilo Code" width="600" caption="Workflows tab in Kilo Code" /%}

## Creating Workflows

Workflows are markdown files stored in `.kilocode/workflows/`:

- **Global workflows**: `~/.kilocode/workflows/` (available in all projects)
- **Project workflows**: `[project]/.kilocode/workflows/` (project-specific)

### Basic Setup

1. Create a `.md` file with step-by-step instructions
2. Save it in your workflows directory
3. Type `/filename.md` to execute

### Workflow Capabilities

Workflows can leverage:

- [Built-in tools](/docs/features/tools/tool-use-overview): [`read_file()`](/docs/features/tools/read-file), [`search_files()`](/docs/features/tools/search-files), [`execute_command()`](/docs/features/tools/execute-command)
- CLI tools: `gh`, `docker`, `npm`, custom scripts
- [MCP integrations](/docs/automate/mcp/overview): Slack, databases, APIs
- [Mode switching](/docs/code-with-ai/agents/using-modes): [`new_task()`](/docs/features/tools/new-task) for specialized contexts

## Common Workflow Patterns

**Release Management**

```markdown
1. Gather merged PRs since last release
2. Generate changelog from commit messages
3. Update version numbers
4. Create release branch and tag
5. Deploy to staging environment
```

**Project Setup**

```markdown
1. Clone repository template
2. Install dependencies (`npm install`, `pip install -r requirements.txt`)
3. Configure environment files
4. Initialize database/services
5. Run initial tests
```

**Code Review Preparation**

```markdown
1. Search for TODO comments and debug statements
2. Run linting and formatting
3. Execute test suite
4. Generate PR description from recent commits
```

## Example: PR Submission Workflow

Let's walk through creating a workflow for submitting a pull request. This workflow handles the entire process from code review to deployment notification.

Create a file called `submit-pr.md` in your `.kilocode/workflows` directory:

```markdown
# Submit PR Workflow

You are helping submit a pull request. Follow these steps:

1. First, use `search_files` to check for any TODO comments or console.log statements that shouldn't be committed
2. Run tests using `execute_command` with `npm test` or the appropriate test command
3. If tests pass, stage and commit changes with a descriptive commit message
4. Push the branch and create a pull request using `gh pr create`
5. Use `ask_followup_question` to get the PR title and description from the user

Parameters needed (ask if not provided):

- Branch name
- Reviewers to assign
```

Now you can trigger this workflow by typing `/submit-pr.md` in the chat. Kilo Code will:

- Scan your code for common issues before committing
- Run your test suite to catch problems early
- Handle the Git operations and PR creation
- Notify your team automatically
- Set up follow-up tasks for deployment

This saves you from manually running the same 7-step process every time you want to submit code for review.
