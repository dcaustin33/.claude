---
name: claude-md-sync
description: Automatically maintain and update Claude.md project documentation based on git commit changes. Use this skill when the user requests to update Claude.md for a git repository, asks to sync documentation with latest changes, wants to document recent features or changes, or mentions updating project documentation to reflect new commits. The skill analyzes changes since the last documented commit, determines significance, and updates Claude.md with relevant information while tracking the commit hash.
---

# Claude.md Sync Skill

This skill automates the maintenance of Claude.md files by analyzing git repository changes and intelligently updating project documentation.

## Core Workflow

When triggered, follow this complete workflow:

### 1. Locate and Read Claude.md

First, determine the repository location:
- If user specifies a path or branch, navigate there
- If in a git repository, use current location
- Ask user for repository path if unclear

Read the existing Claude.md file to understand:
- Current documentation structure and detail level
- Last documented commit hash (if present)
- Documentation style and tone
- Key sections that exist

**Extract Last Commit Hash**: Look for these patterns in Claude.md:
- `Last updated: <commit-hash>`
- `<!-- commit: <commit-hash> -->`
- `Commit: <commit-hash>`
- Any similar pattern in the first 50 lines or last 20 lines of the file

### 2. Analyze Repository Changes

Use the analysis script to understand changes:

```bash
cd <repo_path>
python scripts/analyze_git_changes.py . [old_commit] [new_commit]
```

The script outputs:
- Changed files categorized by type (features, tests, docs, config)
- Commit messages between old and new commits
- Diff statistics
- Recommendation on whether to update

**Manual Analysis Alternative**: If the script fails or for additional context:

```bash
# Get current commit
git rev-parse HEAD

# Get changes since last documented commit
git diff --name-status <old_commit>..HEAD

# Get commit messages
git log <old_commit>..HEAD --oneline --no-merges

# Get file changes with context
git diff <old_commit>..HEAD --stat
```

### 3. Determine Significance of Changes

Evaluate whether changes warrant a Claude.md update using these criteria:

**HIGH SIGNIFICANCE (Always Update)**:
- New features or capabilities added (3+ feature files changed)
- Major architectural changes
- New APIs, modules, or core components
- Breaking changes or migrations
- New dependencies that change functionality
- User-facing behavior changes

**MEDIUM SIGNIFICANCE (Consider Updating)**:
- 1-2 feature files modified with substantial changes
- Bug fixes that clarify functionality
- Performance improvements worth noting
- Configuration changes that affect usage
- 2+ commits with meaningful feature work

**LOW SIGNIFICANCE (Skip Update)**:
- Only test file changes
- Documentation-only changes
- Code formatting or linting
- Dependency version bumps without functionality changes
- Config tweaks that don't affect core behavior
- Comments or logging additions

**SAME COMMIT (Skip Update)**:
- If old_commit == new_commit, no update needed
- Inform user that documentation is already up to date

### 4. Extract Relevant Information

When updates are warranted, gather details about significant changes:

**For New Features**:
- Feature name and purpose
- Core files involved
- New functions, classes, or modules
- Usage examples from code or commit messages
- Related configuration or setup changes

**For Bug Fixes** (if significant enough):
- What was fixed
- Impact on functionality
- Files affected

**For Architectural Changes**:
- What changed structurally
- Why the change matters
- New patterns or approaches

**Review Specific Changes**:
```bash
# View specific file changes
git diff <old_commit>..HEAD -- <file_path>

# View specific commit details
git show <commit_hash>
```

### 5. Update Claude.md

Update the Claude.md file following these principles:

**Maintain Existing Style**: Match the current documentation's:
- Level of technical detail
- Section organization
- Tone (formal vs casual)
- Use of code examples

**Common Section Patterns**:
- **Overview**: High-level project description
- **Architecture**: System design and components
- **Features**: Key capabilities
- **Setup/Installation**: How to get started
- **Usage**: How to use the system
- **API/Modules**: Code organization
- **Configuration**: Settings and options
- **Development**: Contributing guidelines

**Update Strategy**:

1. **Add New Features**: Create new entries or sections for significant additions
2. **Update Existing Sections**: Enhance descriptions when features evolve
3. **Maintain Brevity**: Keep updates concise but informative
4. **Use Clear Language**: Write for someone learning the project
5. **Include Context**: Explain why features exist, not just what they do

**Example Update Formats**:

For a new feature:
```markdown
### Tennis Ball Tracking

The system now includes real-time tennis ball tracking using stereo vision. The tracker processes synchronized camera feeds to compute 3D ball positions with sub-centimeter accuracy.

Key components:
- `tracker/stereo_vision.py`: Stereo camera calibration and 3D reconstruction
- `tracker/ball_detector.py`: YOLOv8-based ball detection
- `tracker/kalman_filter.py`: Motion prediction and smoothing
```

For architectural changes:
```markdown
## Architecture

Recent refactoring separated the inference pipeline from data collection. The system now uses a modular design:

- **Capture Module**: Handles camera input and synchronization
- **Processing Module**: Runs detection and tracking algorithms
- **Output Module**: Streams results to visualization or storage
```

### 6. Record New Commit Hash

**Critical Step**: Update the commit hash metadata so future runs can compare correctly.

Add or update the commit reference at the **end** of the Claude.md file:

```markdown
---

*Last updated: <new_commit_hash>*
```

Or use an HTML comment if preferred:
```markdown
<!-- commit: <new_commit_hash> -->
```

**Format Requirements**:
- Use full commit hash (40 characters) or abbreviated (7+ characters)
- Place after main content, before or after a separator line
- Use consistent format with existing style if one exists

### 7. Summarize Changes to User

After updating, provide a clear summary:

```
✅ Claude.md updated successfully

Changes documented:
- Added section on tennis ball tracking feature
- Updated architecture overview to reflect modular design
- Documented new configuration options for camera calibration

Files changed: 12 (8 feature files, 3 tests, 1 config)
Commits: 15 commits since last update
Updated from: abc123f to def456a
```

If no update was made:
```
ℹ️  Claude.md is up to date

No significant changes detected since last update (abc123f)
Changes were primarily: test files and documentation updates
```

## Decision Tree Summary

```
Is Claude.md present?
├─ No → Inform user, offer to create one
└─ Yes → Extract last commit hash
           │
           Is current commit == last documented commit?
           ├─ Yes → Skip update, inform user doc is current
           └─ No → Analyze changes
                   │
                   Are changes significant?
                   ├─ High significance (3+ features) → Update definitely
                   ├─ Medium significance (1-2 features) → Update probably
                   └─ Low significance (tests/docs only) → Skip update
```

## Edge Cases

**Claude.md Doesn't Exist**:
- Inform user
- Offer to create initial Claude.md by analyzing current repository state
- Include current commit hash in initial version

**No Commit Hash in Claude.md**:
- Treat as first documentation
- Ask user if they want to document from beginning or from recent changes only
- If documenting recent changes, ask for appropriate starting commit

**Multiple Commits with Conflicts**:
- Focus on net changes (final state vs old state)
- Don't document every individual commit
- Synthesize related changes into coherent updates

**Branch Switching**:
- Always verify you're on the correct branch
- Use `git rev-parse --abbrev-ref HEAD` to check current branch
- Switch if needed: `git checkout <branch>`

**User Wants Specific Commit Range**:
- Accept custom old_commit and new_commit parameters
- Override automatic detection
- Document changes in that specific range

## Helper Scripts

**scripts/analyze_git_changes.py**: Comprehensive change analysis tool

Usage:
```bash
# Analyze changes from Claude.md commit to HEAD
python scripts/analyze_git_changes.py /path/to/repo

# Analyze specific commit range
python scripts/analyze_git_changes.py /path/to/repo abc123 def456

# In current directory
python scripts/analyze_git_changes.py .
```

The script provides categorized change summary and update recommendations.

## Examples

**Example 1: Standard Update**
```
User: "Update the Claude.md for the poker-ai repo"

1. Read Claude.md, find last commit: a1b2c3d
2. Run: python scripts/analyze_git_changes.py ~/poker-ai
3. Script shows: 5 feature files changed, 8 commits, recommendation: UPDATE
4. Review changes: new RLVR training loop, entropy management updates
5. Update Claude.md:
   - Add section on RLVR training
   - Update training pipeline description
   - Document new entropy coefficient scheduling
6. Add commit hash: <!-- commit: e4f5g6h -->
7. Summarize changes to user
```

**Example 2: No Significant Changes**
```
User: "Sync the Claude.md with latest commits"

1. Read Claude.md, find last commit: x9y8z7w
2. Analyze changes: only test files and README updates
3. Inform user: "Claude.md is already up to date. Recent commits only modified tests and documentation."
```

**Example 3: First Time Documentation**
```
User: "Create documentation tracking for this project"

1. Claude.md exists but has no commit hash
2. Ask user: "Should I document from the beginning or focus on recent changes?"
3. User chooses recent: "Last 20 commits"
4. Get commit from 20 commits ago: git rev-parse HEAD~20
5. Analyze and document those changes
6. Record current commit hash
```

## Key Principles

1. **Be Selective**: Not every commit needs documentation
2. **Maintain Consistency**: Match existing documentation style
3. **Focus on Understanding**: Help future readers understand the project
4. **Track Commits Reliably**: Always update the commit hash when you update content
5. **Respect User Intent**: If they ask to update, lean toward updating even if borderline
6. **Be Informative**: Explain your decision whether updating or skipping
