---
name: github-code-review
description: Intelligent code review using git diff between current branch and main. Analyzes diffs to identify the branch's purpose, validate implementation correctness, find potential bugs, security vulnerabilities, performance issues, and suggest improvements. Use when reviewing code changes, pull requests, or feature branches.
---

# GitHub Code Review

Perform comprehensive code reviews by analyzing git diffs between the current branch and main branch. This skill helps identify what changes are trying to accomplish, validates implementation quality, finds bugs, and suggests improvements.

## Process Overview

Follow this structured review process:

1. **Get the diff**: Use `scripts/get_diff.py` to retrieve changes
2. **Understand intent**: Analyze what the branch is trying to accomplish
3. **Review implementation**: Check correctness and approach
4. **Identify issues**: Find bugs, security problems, and code smells
5. **Suggest improvements**: Recommend enhancements for quality and maintainability
6. **Provide actionable feedback**: Summarize findings with specific recommendations

## Step 1: Get the Diff

Execute the diff script to retrieve changes:

```bash
cd <repository-path>
python /home/claude/github-code-review/scripts/get_diff.py
```

Optional flags:
- `--base <branch>`: Compare against a different base branch (default: main)
- `--stats`: Include file statistics
- `--files-only`: Show only changed files with status codes

The script outputs:
- Current branch and base branch names
- Merge base commit
- Full unified diff
- File statistics and change types

## Step 2: Understand the Intent

Before diving into details, determine what this branch is trying to accomplish:

**Questions to answer:**
- What feature is being added or bug is being fixed?
- What is the scope of changes (localized vs widespread)?
- Are changes focused or scattered across unrelated concerns?
- Does the commit history or branch name provide context?

**Look for indicators:**
- New files: Feature additions, new modules
- Modified files: Bug fixes, enhancements, refactoring
- Deleted files: Cleanup, deprecation
- Test files: What behavior is being tested?
- Configuration changes: New dependencies, environment updates
- Documentation updates: API changes, new features

**Branch name patterns:**
- `feature/*`: New functionality
- `bugfix/*` or `fix/*`: Bug corrections
- `refactor/*`: Code improvements without behavior change
- `hotfix/*`: Urgent production fixes
- `chore/*`: Maintenance tasks

## Step 3: Review Implementation Correctness

Evaluate whether the implementation achieves its stated goal properly:

### Core Questions
- Does the code accomplish what it's supposed to?
- Are the changes minimal and focused?
- Is the approach sound and idiomatic for the language?
- Are edge cases handled?
- Is error handling appropriate?

### Implementation Validation
- Check logic flow and control structures
- Verify data transformations are correct
- Ensure API contracts are respected
- Validate algorithm correctness
- Confirm proper use of language features

### Test Coverage
- Are tests included for new functionality?
- Do tests cover happy paths and edge cases?
- Are error conditions tested?
- Is test coverage adequate?

## Step 4: Identify Issues

Read `references/review_guidelines.md` for comprehensive patterns, then systematically check for:

### Critical Issues (Must Fix)
- **Security vulnerabilities**: SQL injection, XSS, authentication bypass, sensitive data exposure
- **Data corruption risks**: Race conditions, transaction issues, data loss scenarios
- **Crashes**: Null pointer exceptions, unhandled errors, resource exhaustion
- **Correctness bugs**: Wrong outputs, incorrect state transitions, logic errors

### High-Priority Issues (Should Fix)
- **Performance problems**: N+1 queries, unnecessary loops, memory leaks
- **Resource leaks**: Unclosed files, connections, or handles
- **Concurrency issues**: Race conditions, deadlocks, thread safety
- **Missing validation**: Unchecked inputs, missing authentication
- **Error handling gaps**: Silent failures, generic error messages

### Medium-Priority Issues (Consider Fixing)
- **Code smells**: Long methods, deep nesting, duplicate code
- **Maintainability concerns**: Poor naming, magic numbers, unclear logic
- **Testing gaps**: Missing edge case tests, insufficient coverage
- **Documentation needs**: Complex logic without explanation
- **Inconsistencies**: Style violations, pattern deviations

### Low-Priority Issues (Nice to Have)
- **Minor optimizations**: Unnecessary object creation, redundant operations
- **Style improvements**: Better variable names, clearer comments
- **Refactoring opportunities**: Extractable methods, simplification potential

## Step 5: Suggest Improvements

Beyond fixing bugs, identify opportunities to enhance quality:

### Code Quality
- Simplification opportunities (reduce complexity)
- Better abstraction or encapsulation
- Improved naming for clarity
- Extracted reusable components
- Reduced coupling between modules

### Architecture
- Better separation of concerns
- More appropriate design patterns
- Clearer interfaces and boundaries
- Improved modularity
- Future extensibility considerations

### Performance
- Caching opportunities
- Batch operations instead of individual calls
- More efficient algorithms or data structures
- Lazy loading or pagination
- Database query optimization

### Testing
- Additional test scenarios to cover
- Better test organization
- More effective mocking strategies
- Integration vs unit test balance

### Documentation
- Code comments for complex logic
- API documentation updates
- README updates for new features
- Architecture decision records

## Step 6: Deliver Actionable Feedback

Structure the review output for maximum clarity and usefulness:

### Review Format

```markdown
# Code Review: [Branch Name]

## Summary
[2-3 sentence overview of what this branch does]

## Implementation Assessment
✅ **Correct**: [What works well]
⚠️ **Concerns**: [What needs attention]

## Critical Issues
[List blocking problems that must be fixed before merge]

## Bugs and Potential Issues
[List bugs found with severity and location]

## Security Concerns
[List security vulnerabilities if any]

## Performance Issues
[List performance problems if any]

## Code Quality Suggestions
[List improvements for maintainability]

## Testing Gaps
[List missing test coverage]

## Positive Highlights
[Acknowledge good practices and well-implemented solutions]

## Recommendations
[Prioritized list of actions to take]
```

### Feedback Guidelines
- Be specific: Include file names, line numbers, or code snippets
- Explain why: Don't just point out issues, explain the impact
- Suggest solutions: Provide concrete examples of better approaches
- Prioritize: Distinguish critical issues from nice-to-haves
- Be constructive: Balance criticism with recognition of good work
- Consider context: Account for project constraints and trade-offs

## Language-Specific Considerations

When reviewing, consider language-specific best practices:

- **Python**: Type hints, list comprehensions, context managers, PEP 8 style
- **JavaScript/TypeScript**: const/let usage, async/await patterns, TypeScript strict mode
- **Java**: Exception handling, streams API, resource management, generics
- **Go**: Error handling, goroutine safety, defer usage, interface patterns
- **Rust**: Ownership patterns, error handling, lifetime annotations
- **Others**: Consult `references/review_guidelines.md` for more patterns

## Common Pitfalls to Watch For

- **Incomplete changes**: Feature partially implemented
- **Broken builds**: Code doesn't compile or pass tests
- **Backward compatibility**: Breaking changes to existing APIs
- **Migration issues**: Database or config changes without migration scripts
- **Dependency problems**: New dependencies not documented or unnecessary
- **Performance regressions**: Changes that slow down critical paths
- **Security regressions**: Removing or weakening security measures

## When Not to Use This Skill

This skill is for reviewing code changes. Don't use it for:
- Writing code from scratch (no diff to review)
- General coding questions without specific changes
- Understanding existing code without recent changes
- Code formatting only (use automated linters instead)

## Resources

- `scripts/get_diff.py`: Python script to retrieve git diffs with statistics
- `references/review_guidelines.md`: Comprehensive bug patterns, code smells, and best practices
