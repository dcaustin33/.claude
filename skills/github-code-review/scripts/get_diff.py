#!/usr/bin/env python3
"""
Get git diff between current branch and a base branch (default: main).
"""
import subprocess
import sys
import argparse

def get_current_branch():
    """Get the name of the current branch."""
    result = subprocess.run(
        ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
        capture_output=True,
        text=True,
        check=True
    )
    return result.stdout.strip()

def get_diff(base_branch='main', show_stats=False):
    """
    Get the diff between current branch and base branch.
    
    Args:
        base_branch: The base branch to compare against (default: main)
        show_stats: Whether to show file statistics
    
    Returns:
        Dictionary with diff information
    """
    current_branch = get_current_branch()
    
    # Get the merge base (common ancestor)
    try:
        merge_base = subprocess.run(
            ['git', 'merge-base', base_branch, 'HEAD'],
            capture_output=True,
            text=True,
            check=True
        ).stdout.strip()
    except subprocess.CalledProcessError:
        print(f"Error: Could not find merge base with {base_branch}", file=sys.stderr)
        print(f"Make sure you have fetched the latest {base_branch} branch", file=sys.stderr)
        sys.exit(1)
    
    # Get the diff
    diff_result = subprocess.run(
        ['git', 'diff', merge_base, 'HEAD'],
        capture_output=True,
        text=True,
        check=True
    )
    
    # Get file statistics
    stats_result = subprocess.run(
        ['git', 'diff', '--stat', merge_base, 'HEAD'],
        capture_output=True,
        text=True,
        check=True
    )
    
    # Get list of changed files with their change type
    changed_files = subprocess.run(
        ['git', 'diff', '--name-status', merge_base, 'HEAD'],
        capture_output=True,
        text=True,
        check=True
    )
    
    return {
        'current_branch': current_branch,
        'base_branch': base_branch,
        'merge_base': merge_base,
        'diff': diff_result.stdout,
        'stats': stats_result.stdout,
        'changed_files': changed_files.stdout
    }

def main():
    parser = argparse.ArgumentParser(
        description='Get git diff between current branch and base branch'
    )
    parser.add_argument(
        '--base',
        default='main',
        help='Base branch to compare against (default: main)'
    )
    parser.add_argument(
        '--stats',
        action='store_true',
        help='Show file statistics'
    )
    parser.add_argument(
        '--files-only',
        action='store_true',
        help='Show only changed files with their status'
    )
    
    args = parser.parse_args()
    
    diff_info = get_diff(args.base, args.stats)
    
    print(f"Branch: {diff_info['current_branch']} → {diff_info['base_branch']}")
    print(f"Merge base: {diff_info['merge_base'][:8]}\n")
    
    if args.files_only:
        print("Changed files:")
        print(diff_info['changed_files'])
    elif args.stats:
        print("Statistics:")
        print(diff_info['stats'])
        print("\nFull diff:")
        print(diff_info['diff'])
    else:
        print(diff_info['diff'])

if __name__ == '__main__':
    main()
