#!/usr/bin/env python3
"""
Analyze git changes between commits to help determine what should be documented.

Usage:
    python analyze_git_changes.py <repo_path> [old_commit] [new_commit]
    
    If old_commit is not provided, uses the commit from Claude.md metadata
    If new_commit is not provided, uses current HEAD
"""

import subprocess
import sys
import os
import re
from pathlib import Path


def run_git_command(repo_path, *args):
    """Run a git command and return the output."""
    try:
        result = subprocess.run(
            ["git", "-C", repo_path, *args],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Git command failed: {e.stderr}", file=sys.stderr)
        return None


def get_current_commit(repo_path):
    """Get the current commit hash."""
    return run_git_command(repo_path, "rev-parse", "HEAD")


def get_commit_from_claude_md(repo_path):
    """Extract the last documented commit hash from Claude.md."""
    claude_md_path = Path(repo_path) / "Claude.md"
    if not claude_md_path.exists():
        return None
    
    with open(claude_md_path, 'r') as f:
        content = f.read()
    
    # Look for patterns like "Last updated: <commit>" or "<!-- commit: <hash> -->"
    patterns = [
        r'Last\s+updated\s*:\s*([0-9a-f]{7,40})',
        r'Last\s+commit\s*:\s*([0-9a-f]{7,40})',
        r'<!--\s*commit\s*:\s*([0-9a-f]{7,40})\s*-->',
        r'Commit\s*:\s*([0-9a-f]{7,40})',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            return match.group(1)
    
    return None


def get_changed_files(repo_path, old_commit, new_commit):
    """Get list of changed files between commits."""
    if not old_commit:
        return []
    
    output = run_git_command(repo_path, "diff", "--name-status", f"{old_commit}..{new_commit}")
    if not output:
        return []
    
    files = []
    for line in output.split('\n'):
        if line.strip():
            parts = line.split('\t', 1)
            if len(parts) == 2:
                status, filepath = parts
                files.append({'status': status, 'path': filepath})
    
    return files


def get_commit_messages(repo_path, old_commit, new_commit):
    """Get commit messages between two commits."""
    if not old_commit:
        return []
    
    output = run_git_command(
        repo_path, 
        "log", 
        f"{old_commit}..{new_commit}",
        "--pretty=format:%H|%s|%b",
        "--no-merges"
    )
    
    if not output:
        return []
    
    commits = []
    for line in output.split('\n'):
        if '|' in line:
            parts = line.split('|', 2)
            if len(parts) >= 2:
                commits.append({
                    'hash': parts[0][:7],
                    'subject': parts[1],
                    'body': parts[2] if len(parts) > 2 else ''
                })
    
    return commits


def get_diff_stats(repo_path, old_commit, new_commit):
    """Get diff statistics between commits."""
    if not old_commit:
        return None
    
    output = run_git_command(repo_path, "diff", "--stat", f"{old_commit}..{new_commit}")
    return output


def categorize_changes(files):
    """Categorize changed files into meaningful groups."""
    categories = {
        'features': [],
        'tests': [],
        'docs': [],
        'config': [],
        'other': []
    }
    
    for file_info in files:
        path = file_info['path'].lower()
        
        if 'test' in path or path.endswith('.test.py') or path.endswith('.spec.js'):
            categories['tests'].append(file_info)
        elif path.endswith('.md') or 'doc' in path or path.startswith('docs/'):
            categories['docs'].append(file_info)
        elif any(x in path for x in ['config', 'setup', '.json', '.yaml', '.toml', 'requirements', 'package.json']):
            categories['config'].append(file_info)
        elif file_info['status'] in ['A', 'M']:  # Added or Modified
            categories['features'].append(file_info)
        else:
            categories['other'].append(file_info)
    
    return categories


def main():
    if len(sys.argv) < 2:
        print("Usage: python analyze_git_changes.py <repo_path> [old_commit] [new_commit]")
        sys.exit(1)
    
    repo_path = sys.argv[1]
    
    # Determine old and new commits
    old_commit = sys.argv[2] if len(sys.argv) > 2 else get_commit_from_claude_md(repo_path)
    new_commit = sys.argv[3] if len(sys.argv) > 3 else get_current_commit(repo_path)
    
    if not new_commit:
        print("Error: Could not determine current commit", file=sys.stderr)
        sys.exit(1)
    
    print(f"Repository: {repo_path}")
    print(f"Old commit: {old_commit or 'None (first documentation)'}")
    print(f"New commit: {new_commit}")
    print()
    
    if old_commit and old_commit == new_commit:
        print("No changes: Old and new commits are the same")
        sys.exit(0)
    
    # Get changes
    changed_files = get_changed_files(repo_path, old_commit, new_commit)
    commits = get_commit_messages(repo_path, old_commit, new_commit)
    
    if not changed_files and not commits:
        print("No changes detected")
        sys.exit(0)
    
    print("=" * 60)
    print("CHANGE SUMMARY")
    print("=" * 60)
    print()
    
    # Categorize changes
    categories = categorize_changes(changed_files)
    
    print(f"Total files changed: {len(changed_files)}")
    print(f"Total commits: {len(commits)}")
    print()
    
    # Show categorized files
    for category, files in categories.items():
        if files:
            print(f"\n{category.upper()} ({len(files)} files):")
            for file_info in files[:10]:  # Limit to 10 per category
                status_symbol = {
                    'A': '[+]',
                    'M': '[~]',
                    'D': '[-]',
                    'R': '[→]'
                }.get(file_info['status'], '[?]')
                print(f"  {status_symbol} {file_info['path']}")
            if len(files) > 10:
                print(f"  ... and {len(files) - 10} more")
    
    # Show commit messages
    if commits:
        print(f"\n\nCOMMIT MESSAGES ({len(commits)} commits):")
        for commit in commits:
            print(f"\n  {commit['hash']}: {commit['subject']}")
            if commit['body']:
                body_lines = commit['body'].strip().split('\n')[:3]
                for line in body_lines:
                    if line.strip():
                        print(f"    {line.strip()}")
    
    # Show diff stats
    print("\n\nDIFF STATISTICS:")
    stats = get_diff_stats(repo_path, old_commit, new_commit)
    if stats:
        print(stats)
    
    print("\n" + "=" * 60)
    
    # Determine if changes are significant
    feature_count = len(categories['features'])
    config_count = len(categories['config'])
    
    if feature_count >= 3 or (feature_count >= 1 and len(commits) >= 3):
        print("\n✅ RECOMMENDATION: Significant changes detected - UPDATE Claude.md")
        print(f"   Reason: {feature_count} feature files changed across {len(commits)} commits")
    elif feature_count >= 1:
        print("\n⚠️  RECOMMENDATION: Minor changes detected - CONSIDER updating Claude.md")
        print(f"   Reason: {feature_count} feature file(s) changed")
    else:
        print("\n❌ RECOMMENDATION: No significant changes - SKIP update")
        print(f"   Reason: Only config/docs/tests changed ({config_count} config, {len(categories['docs'])} docs, {len(categories['tests'])} tests)")


if __name__ == "__main__":
    main()
