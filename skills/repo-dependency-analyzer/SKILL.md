---
name: repo-dependency-analyzer
description: Comprehensive repository analysis for correctness and critical issues. Use when given a focus file (like a training script, main module, or entry point) to trace and analyze the entire dependency chain for bugs, type mismatches, import errors, configuration issues, and other critical problems that could cause failures or incorrect behavior. Particularly useful for ML training scripts, large codebases, and pre-deployment verification.
---

# Repo Dependency Analyzer

Analyze entire repository dependency chains starting from a focus file to identify critical bugs and issues that could cause runtime failures or incorrect behavior.

## When to Use This Skill

Use this skill when:
- User provides a focus file and asks to check for bugs in the repo
- User wants to verify a training script or main module is correctly configured
- User asks to analyze dependencies or find issues in files that feed into a target
- User requests pre-deployment verification or correctness review
- User mentions checking "the entire repo" or "all files that affect X"

## Analysis Workflow

### Step 1: Identify and Validate Focus File

Identify the focus file from the user's request. This is typically:
- A training script (train.py, main.py)
- An entry point or main module
- A file explicitly mentioned by the user

Verify the focus file exists in the repository.

### Step 2: Trace Dependency Chain

Use the trace_dependencies.py script to identify all files that the focus file depends on:

```bash
python scripts/trace_dependencies.py <repo_path> <focus_file>
```

This script:
- Traces imports/requires across Python, JavaScript, TypeScript, Go, Java, C/C++
- Follows the entire dependency chain recursively
- Returns a complete list of dependent files

If the repo is already uploaded and available, use view tool to explore structure first, then run the tracer.

### Step 3: Load Bug Pattern Reference

Read references/bug_patterns.md to understand critical issue categories:

```bash
view references/bug_patterns.md
```

This reference provides:
- Common bug patterns by category
- Language-specific issues
- Priority levels for findings
- Training-specific problems (for ML code)

### Step 4: Analyze Each Dependency

For each file in the dependency chain (starting with most critical):

1. **Read the file content**
   - Use view tool to read each dependency
   - Understand its purpose and interface

2. **Check for critical issues** by looking for patterns from bug_patterns.md:
   - Import/dependency problems (missing imports, circular deps)
   - Type and shape mismatches (especially for ML tensors)
   - Configuration issues (missing files, env vars)
   - Resource management (memory leaks, unclosed files)
   - API misuse (deprecated functions, wrong parameters)
   - Language-specific issues (null checks, error handling)

3. **Trace data flow**
   - For functions called by focus file: verify inputs/outputs match expectations
   - For classes instantiated: verify initialization parameters are correct
   - For ML code: trace tensor shapes and device placement through pipeline

4. **Verify integration points**
   - Check function signatures match call sites
   - Verify return values are used correctly
   - Ensure configuration is loaded before use

### Step 5: Analyze Focus File

Finally, analyze the focus file itself:
- Verify it correctly uses all imported dependencies
- Check for issues in the main execution flow
- For training scripts: verify data loading, model training, checkpointing logic
- Ensure proper error handling for critical operations

### Step 6: Report Findings

Create a structured report with:

1. **Executive Summary**
   - Number of dependencies analyzed
   - Critical issues found (if any)
   - Overall assessment

2. **Critical Issues** (will cause failures)
   - File location
   - Issue description
   - Impact on execution
   - Suggested fix

3. **High Priority Issues** (will cause incorrect behavior)
   - Similar structure to critical

4. **Medium/Low Priority Issues** (optional, if requested)

Format findings clearly:
```
CRITICAL: Missing import in src/model.py
  Line 45: Imports 'NetworkLayer' from utils.layers
  Problem: NetworkLayer is not defined in utils/layers.py
  Impact: Will cause ImportError when model.py loads
  Fix: Add NetworkLayer class to utils/layers.py or correct import path
```

## Special Considerations

### Large Repositories

For repos with >50 dependencies:
- Focus on direct dependencies first
- Prioritize files that appear in critical paths
- Group similar issues together

### Training Scripts

Pay extra attention to:
- Data loading configuration and batch processing
- Gradient computation and optimizer setup
- Loss function compatibility with model outputs
- Device placement (CPU/GPU) consistency
- Checkpoint save/load logic

### Multi-Language Repositories

When analyzing repos with multiple languages:
- Trace dependencies within each language separately
- Check interfaces between languages (FFI, API boundaries)
- Verify data serialization/deserialization at boundaries

## Limitations

- Script traces static imports; doesn't catch dynamic imports or runtime dependencies
- Cannot verify external package versions without requirements/package files
- Cannot execute code to verify runtime behavior
- May miss metaprogramming or reflection-based dependencies

## Example Usage

**User request:** "Check my training script for bugs - I keep getting shape mismatches"

**Workflow:**
1. Identify focus file: train.py
2. Run: `python scripts/trace_dependencies.py . train.py`
3. Read bug_patterns.md, focus on "Shape Mismatches" section
4. Analyze dependencies (dataset.py, model.py, utils.py, etc.)
5. Trace tensor shapes through data pipeline
6. Identify shape mismatch in data preprocessing
7. Report finding with specific file, line, and fix

## Tips for Effective Analysis

- Start with files closest to focus file in dependency chain
- Look for patterns, not just individual bugs
- Consider how components interact, not just individual correctness
- Be specific about line numbers and exact issues when possible
- Prioritize issues that will definitely cause failures
- For unclear issues, explain assumptions and reasoning
