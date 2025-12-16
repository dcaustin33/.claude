---
name: code-documenter
description: Automatically generate concise documentation for code projects. Creates a high-level DOCUMENTATION.md file that outlines the purpose and structure of all relevant files, plus brief markdown files in a documentation/ folder for each code file with overviews and 1-2 key highlights. Use when users request code documentation, ask to "document this codebase/project/repository", want to generate documentation for files, or need to create technical documentation for software projects.
---

# Code Documenter

Generate concise, readable documentation for code projects with a high-level overview and brief per-file documentation that focuses on purpose and key highlights.

## Documentation Structure

Create documentation in two parts:

1. **DOCUMENTATION.md** - High-level overview at the project root
2. **documentation/** folder - Brief per-file documentation with overviews and key highlights

## Step 1: Analyze the Codebase

Before generating documentation, analyze the project structure:

```bash
# View project structure (adjust extensions for the language)
find . -type f \( -name "*.py" -o -name "*.js" -o -name "*.ts" -o -name "*.jsx" -o -name "*.tsx" -o -name "*.java" -o -name "*.cpp" -o -name "*.c" -o -name "*.h" -o -name "*.go" -o -name "*.rs" -o -name "*.rb" \) | grep -v node_modules | grep -v __pycache__ | head -50
```

Identify:
- Main entry points and core modules
- Directory organization and purpose
- Dependencies and relationships between files
- Configuration files and build scripts

## Step 2: Create DOCUMENTATION.md

Generate a high-level overview file at the project root:

### DOCUMENTATION.md Structure

```markdown
# Project Documentation

## Overview
[Brief description of the project and its purpose]

## Project Structure

### Core Files
- `file1.py` - [Brief purpose]
- `file2.py` - [Brief purpose]

### Directories
- `src/` - [Purpose]
- `tests/` - [Purpose]
- `utils/` - [Purpose]

## Architecture
[High-level architecture description]

## Key Components
[Overview of main components and their interactions]

## Getting Started
[How to use/run the project]

## Documentation Index
Detailed documentation for each file can be found in the `documentation/` directory:
- [file1.py](documentation/file1.md)
- [file2.py](documentation/file2.md)
```

**Guidelines for DOCUMENTATION.md:**
- Keep it concise - one line per file explaining its purpose
- Focus on the "why" and high-level "what"
- Describe the overall architecture and how pieces fit together
- Include links to brief per-file documentation
- Use relative paths for all links

## Step 3: Create documentation/ Folder

Create the documentation directory at the project root:

```bash
mkdir -p documentation
```

## Step 4: Generate Per-File Documentation

For each relevant code file, create a brief markdown file in `documentation/`:

### Per-File Documentation Template

```markdown
# [Filename]

## Purpose
[1-2 sentence overview of what this file does and why it exists]

## Key Components

[Pick the 1-2 most important elements to highlight]

**Main Class/Function: `ComponentName`**
[Brief description of what it does and key parameters/returns if relevant]

## Related Files
- [file1.py](file1.md) - How it relates
```

### Documentation Guidelines

**Be concise:**
- Each file doc should be readable in under a minute
- Focus on high-level purpose and role in the project
- Only drill down on 1-2 most important/complex elements
- Skip obvious implementations and boilerplate

**Be selective:**
- Don't document every method or function
- Highlight what makes this file unique or critical
- Mention key algorithms or design patterns only if notable
- Link to related files for context

**Be clear:**
- Start with a simple overview in 1-2 sentences
- Use plain language
- Explain the "why" more than the "what"

## Step 5: Handle Special Files

### Configuration Files
For config files (JSON, YAML, TOML, etc.):
```markdown
# [config_file.yaml]

## Purpose
[One sentence: what this configuration controls]

## Key Settings
[Highlight only the 1-2 most important or non-obvious options]
```

### Test Files
For test files:
```markdown
# [test_file.py]

## Purpose
Tests for [module_name]

## Coverage
[Brief summary of what's tested and any notable test patterns]
```

## Step 6: Document Relationships

In both DOCUMENTATION.md and individual files, highlight:
- How modules depend on each other
- Data flow between components
- Shared utilities and common patterns
- Entry points and main execution paths

## Naming Convention

Save per-file documentation as:
- Source file: `src/utils/helper.py` → Doc file: `documentation/src_utils_helper.md`
- Or maintain directory structure: `documentation/src/utils/helper.md`

Use the approach that best matches the project structure. For flat structures, use underscores. For nested structures, maintain the hierarchy.

## Iteration Process

1. Start with DOCUMENTATION.md for the big picture
2. Generate brief docs for core files (focus on purpose + 1-2 key elements)
3. Document utilities and helpers (keep even briefer)
4. Document tests and configs (minimal, purpose-focused)
5. Add cross-links between related files
6. Review: each file doc should be readable in under 60 seconds

## Language-Specific Considerations

When documenting files, adapt the "Key Components" section to the language:
- Focus on the most important language-specific feature (e.g., decorators in Python, async patterns in JS, traits in Rust)
- Only mention language specifics if they're critical to understanding the file
- Keep it brief - 1-2 sentences maximum

## Output Format

Always create files in this order:
1. DOCUMENTATION.md in the project root
2. documentation/ folder
3. Individual .md files for each code file

After completion, provide a summary with links to the main documentation file.