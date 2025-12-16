---
name: code-refactor
description: Comprehensive code refactoring and cleanup. Use when asked to review code for bloat, consolidate duplicate code, extract helper functions, remove redundant comments, reduce lines of code, or make code more clean and readable. Applicable to files, folders, or entire repositories in any programming language.
---

# Code Refactor

## Overview

This skill provides systematic approaches for identifying and eliminating code bloat, extracting reusable functions, removing redundant comments, and improving code quality. Use this when working with codebases that need cleanup, consolidation, or readability improvements.

## Refactoring Workflow

Follow this systematic process when refactoring code:

### 1. Initial Analysis

**Scan the codebase structure:**
- Use `view` to explore directories and understand the file organization
- Identify which files contain the core logic vs configuration/tests
- Note the programming language(s) and frameworks in use

**For each file or module, analyze:**
- Total lines of code (LOC)
- Complexity indicators (nested loops, long functions, deep conditionals)
- Patterns of duplication
- Comment density and quality

Use the analysis script when available:
```bash
python scripts/analyze_code.py <path-to-file-or-directory>
```

### 2. Identify Refactoring Opportunities

Look for these specific patterns in order of impact:

**a) Duplicate Code Blocks**
- Nearly identical code repeated across functions or files
- Similar logic with minor variations (candidates for parameterization)
- Copy-pasted functions with small modifications

**b) Extract Helper Functions**
- Code blocks repeated 2+ times → extract to function
- Complex expressions used multiple times → extract to named function
- Long functions (>50 lines) → break into smaller, focused functions
- Nested loops/conditionals (>3 levels) → extract inner logic

**c) Consolidation Opportunities**
- Multiple functions doing similar things → merge with parameters
- Repeated patterns across classes → extract to base class or utility
- Similar conditional logic → extract to strategy pattern or lookup table

**d) Comment Cleanup**
Redundant comments to remove:
- Comments that restate obvious code (e.g., `# increment i` above `i += 1`)
- Outdated comments that no longer match the code
- Commented-out code blocks (unless marked as important examples)
- Auto-generated boilerplate comments with no added value
- TODO comments for completed work

Comments to keep:
- Complex algorithm explanations
- Non-obvious business logic rationale
- Important warnings or gotchas
- API documentation and type hints
- Context for why code is written a certain way

**e) Code Smell Detection**
- Magic numbers → extract to named constants
- Long parameter lists (>4 params) → use config objects or builder pattern
- Deep nesting → early returns or guard clauses
- Overly clever one-liners → expand for clarity
- Inconsistent naming → standardize conventions

### 3. Create Refactoring Plan

Before making changes, create a structured plan:

```markdown
## Refactoring Plan for [filename/module]

### Metrics
- Current LOC: X
- Target LOC: Y (Z% reduction)
- Functions to extract: N
- Duplicate blocks found: M

### Proposed Changes

1. **Extract helper function: `calculate_total`**
   - Location: Lines 45-67, 89-111, 134-156
   - Savings: ~50 lines
   - Parameters: items, tax_rate, discount

2. **Consolidate similar functions**
   - Merge: `process_user_data`, `process_admin_data`, `process_guest_data`
   - Into: `process_data(user_type, data)`
   - Savings: ~80 lines

3. **Remove redundant comments**
   - Lines: 23, 45-48, 67, 89-92, 110
   - Savings: ~15 lines

[Continue for all changes...]

### Risk Assessment
- Low risk: Comment removal, variable renaming
- Medium risk: Function extraction (ensure all call sites updated)
- High risk: Logic consolidation (requires thorough testing)
```

### 4. Implement Refactoring

Execute changes systematically:

**a) Start with low-risk changes:**
- Remove redundant comments
- Extract obvious constants
- Rename variables for clarity

**b) Extract helper functions:**
- Identify the most repeated block
- Create the function with clear name and parameters
- Replace all occurrences
- Test each replacement

**c) Consolidate duplicate logic:**
- Create the unified function/class
- Add parameters for variations
- Replace call sites one at a time
- Verify behavior matches

**d) Final cleanup:**
- Ensure consistent formatting
- Update remaining comments
- Remove unused imports
- Organize functions logically

### 5. Verification & Documentation

**Generate a refactoring summary:**
```markdown
## Refactoring Summary

### Changes Made
- Extracted X helper functions
- Consolidated Y similar functions
- Removed Z redundant comments
- Reduced LOC from A to B (C% reduction)

### New Helper Functions
1. `function_name(params)` - Purpose and usage
2. `another_function(params)` - Purpose and usage

### Files Modified
- file1.py: Major refactoring (150 → 95 lines)
- file2.py: Minor cleanup (80 → 75 lines)

### Testing Notes
[Note any areas that need extra testing attention]
```

## Refactoring Patterns by Language

### Python
- Extract list comprehensions from loops
- Use `@property` for simple getters
- Replace multiple similar `if-elif` with dictionaries
- Use dataclasses for data containers
- Extract complex lambda functions to named functions

### JavaScript/TypeScript
- Extract repeated DOM manipulations
- Use array methods (map, filter, reduce) over loops
- Extract inline callbacks to named functions
- Use object destructuring to reduce parameter counts
- Consolidate similar event handlers

### Java/C#
- Extract repeated try-catch blocks to utility methods
- Use streams/LINQ for collection operations
- Extract builder patterns for complex object creation
- Consolidate similar CRUD operations
- Use method overloading to reduce function count

### General Principles (all languages)
- Single Responsibility Principle: Each function does one thing
- Don't Repeat Yourself (DRY): Extract repeated logic
- Clear naming: Functions and variables should explain themselves
- Minimal parameters: Prefer 1-3 parameters, use objects for more
- Early returns: Reduce nesting with guard clauses

## Best Practices

**Do:**
- Test after each significant change
- Preserve existing functionality exactly
- Make incremental changes
- Keep functions under 30 lines when possible
- Use descriptive names even if longer
- Document non-obvious extracted functions

**Don't:**
- Over-optimize or make code too abstract
- Extract functions used only once
- Remove comments that explain "why" (keep these!)
- Change behavior while refactoring
- Make too many changes at once
- Sacrifice readability for brevity

## Working with Large Codebases

For repositories or large folders:

1. **Prioritize high-impact files:**
   - Start with files changed most frequently
   - Focus on files with most duplication
   - Address core business logic first

2. **Use the analysis script for metrics:**
   ```bash
   python scripts/analyze_code.py /path/to/repo --recursive --report
   ```

3. **Create separate branches for major refactorings**

4. **Document cross-file extractions in a central location**

## Resources

### scripts/analyze_code.py
Python script that analyzes code for complexity, duplication, and refactoring opportunities. Provides metrics and suggestions.

### references/refactoring_patterns.md
Detailed catalog of common refactoring patterns with before/after examples. Load this when encountering specific patterns or needing inspiration for how to restructure code.
