#!/usr/bin/env python3
"""
Code Analysis Tool for Refactoring

Analyzes code files to identify:
- Duplicate code blocks
- Function complexity
- Lines of code metrics
- Comment density
- Potential refactoring opportunities
"""

import os
import re
import sys
import argparse
from pathlib import Path
from collections import defaultdict, Counter
from typing import List, Dict, Tuple


class CodeAnalyzer:
    """Analyzes code files for refactoring opportunities"""
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.lines = []
        self.language = self._detect_language()
        self.load_file()
        
    def _detect_language(self) -> str:
        """Detect programming language from file extension"""
        ext = Path(self.file_path).suffix.lower()
        lang_map = {
            '.py': 'python',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.java': 'java',
            '.cpp': 'cpp',
            '.c': 'c',
            '.cs': 'csharp',
            '.go': 'go',
            '.rb': 'ruby',
            '.php': 'php',
            '.rs': 'rust',
        }
        return lang_map.get(ext, 'unknown')
    
    def load_file(self):
        """Load file contents"""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                self.lines = f.readlines()
        except Exception as e:
            print(f"Error reading {self.file_path}: {e}")
            self.lines = []
    
    def count_loc(self) -> Dict[str, int]:
        """Count lines of code, excluding comments and blank lines"""
        total = len(self.lines)
        blank = sum(1 for line in self.lines if line.strip() == '')
        
        # Simple comment detection (language-specific would be better)
        comment_patterns = {
            'python': r'^\s*#',
            'javascript': r'^\s*//',
            'typescript': r'^\s*//',
            'java': r'^\s*//',
            'cpp': r'^\s*//',
            'c': r'^\s*//',
            'csharp': r'^\s*//',
            'go': r'^\s*//',
            'ruby': r'^\s*#',
            'php': r'^\s*//',
            'rust': r'^\s*//',
        }
        
        pattern = comment_patterns.get(self.language, r'^\s*#|^\s*//')
        comments = sum(1 for line in self.lines if re.match(pattern, line))
        
        code = total - blank - comments
        
        return {
            'total': total,
            'code': code,
            'blank': blank,
            'comments': comments
        }
    
    def find_long_functions(self, threshold: int = 50) -> List[Dict]:
        """Find functions longer than threshold"""
        long_functions = []
        
        # Simple function detection patterns
        func_patterns = {
            'python': r'^\s*def\s+(\w+)',
            'javascript': r'^\s*(?:function\s+(\w+)|(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s+)?(?:function|\())',
            'typescript': r'^\s*(?:function\s+(\w+)|(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s+)?(?:function|\())',
            'java': r'^\s*(?:public|private|protected)?\s*(?:static)?\s*(?:\w+)\s+(\w+)\s*\(',
        }
        
        pattern = func_patterns.get(self.language)
        if not pattern:
            return long_functions
        
        current_func = None
        func_start = 0
        indent_level = 0
        initial_indent = 0
        
        for i, line in enumerate(self.lines, 1):
            # Detect function start
            match = re.search(pattern, line)
            if match:
                current_func = match.group(1) or match.group(2)
                func_start = i
                initial_indent = len(line) - len(line.lstrip())
                indent_level = initial_indent
                continue
            
            # Track function end by indentation
            if current_func:
                line_indent = len(line) - len(line.lstrip())
                if line.strip() and line_indent <= initial_indent and i > func_start:
                    func_length = i - func_start
                    if func_length > threshold:
                        long_functions.append({
                            'name': current_func,
                            'start': func_start,
                            'length': func_length
                        })
                    current_func = None
        
        return long_functions
    
    def find_duplicate_blocks(self, min_lines: int = 5) -> List[Dict]:
        """Find duplicate code blocks"""
        duplicates = []
        
        # Normalize lines (remove whitespace and comments for comparison)
        normalized = []
        for line in self.lines:
            stripped = line.strip()
            # Skip blank lines and simple comments
            if stripped and not stripped.startswith(('#', '//')):
                normalized.append(stripped)
        
        # Look for duplicate sequences
        seen_blocks = defaultdict(list)
        
        for i in range(len(normalized) - min_lines):
            block = tuple(normalized[i:i + min_lines])
            seen_blocks[block].append(i)
        
        # Find blocks that appear multiple times
        for block, positions in seen_blocks.items():
            if len(positions) > 1:
                duplicates.append({
                    'lines': min_lines,
                    'occurrences': len(positions),
                    'positions': positions,
                    'sample': '\n'.join(block[:3])  # First 3 lines as sample
                })
        
        return sorted(duplicates, key=lambda x: x['occurrences'] * x['lines'], reverse=True)
    
    def analyze_nesting(self) -> Dict:
        """Analyze nesting depth"""
        max_depth = 0
        current_depth = 0
        deep_lines = []
        
        indent_chars = {
            'python': 4,
            'javascript': 2,
            'typescript': 2,
        }
        
        indent_size = indent_chars.get(self.language, 4)
        
        for i, line in enumerate(self.lines, 1):
            if line.strip():
                indent = len(line) - len(line.lstrip())
                depth = indent // indent_size
                current_depth = depth
                
                if depth > max_depth:
                    max_depth = depth
                
                if depth >= 4:  # Deep nesting threshold
                    deep_lines.append(i)
        
        return {
            'max_depth': max_depth,
            'deep_nesting_lines': deep_lines[:10]  # First 10
        }
    
    def find_magic_numbers(self) -> List[Tuple[int, str]]:
        """Find magic numbers in code"""
        magic_numbers = []
        
        # Pattern for numeric literals (excluding 0, 1, -1)
        pattern = r'\b(?!0\b|1\b|-1\b)[-+]?\d+\.?\d*\b'
        
        for i, line in enumerate(self.lines, 1):
            # Skip comments
            if re.match(r'^\s*#|^\s*//', line):
                continue
            
            matches = re.finditer(pattern, line)
            for match in matches:
                magic_numbers.append((i, match.group()))
        
        return magic_numbers[:20]  # Return first 20
    
    def generate_report(self) -> str:
        """Generate comprehensive analysis report"""
        loc = self.count_loc()
        long_funcs = self.find_long_functions()
        duplicates = self.find_duplicate_blocks()
        nesting = self.analyze_nesting()
        magic_nums = self.find_magic_numbers()
        
        report = [
            f"\n{'='*60}",
            f"Code Analysis Report: {Path(self.file_path).name}",
            f"{'='*60}\n",
            
            "📊 Lines of Code:",
            f"  Total lines: {loc['total']}",
            f"  Code lines: {loc['code']}",
            f"  Blank lines: {loc['blank']}",
            f"  Comment lines: {loc['comments']}",
            f"  Comment ratio: {loc['comments']/max(loc['total'], 1)*100:.1f}%\n",
        ]
        
        if long_funcs:
            report.extend([
                "🔍 Long Functions (>50 lines):",
            ])
            for func in long_funcs[:5]:
                report.append(f"  - {func['name']}: {func['length']} lines (starts line {func['start']})")
            report.append("")
        
        if duplicates:
            report.extend([
                "🔄 Duplicate Code Blocks:",
            ])
            for dup in duplicates[:5]:
                report.append(f"  - {dup['lines']} lines repeated {dup['occurrences']} times")
                report.append(f"    Sample: {dup['sample'][:50]}...")
            report.append("")
        
        if nesting['max_depth'] >= 4:
            report.extend([
                f"⚠️  Deep Nesting Detected:",
                f"  Max depth: {nesting['max_depth']} levels",
                f"  Deep nesting on lines: {', '.join(map(str, nesting['deep_nesting_lines']))}",
                ""
            ])
        
        if magic_nums:
            report.extend([
                "🔢 Magic Numbers Found:",
            ])
            for line, num in magic_nums[:10]:
                report.append(f"  Line {line}: {num}")
            report.append("")
        
        # Recommendations
        report.extend([
            "💡 Refactoring Recommendations:",
        ])
        
        if long_funcs:
            report.append(f"  • Extract helper functions from {len(long_funcs)} long functions")
        if duplicates:
            total_dup_lines = sum(d['lines'] * (d['occurrences']-1) for d in duplicates)
            report.append(f"  • Consolidate duplicate code (potential savings: ~{total_dup_lines} lines)")
        if loc['comments'] / max(loc['total'], 1) > 0.3:
            report.append(f"  • Review comment density (30%+) for redundant comments")
        if nesting['max_depth'] >= 4:
            report.append(f"  • Reduce nesting depth using early returns or extracted functions")
        if magic_nums:
            report.append(f"  • Extract {len(magic_nums)} magic numbers to named constants")
        if not (long_funcs or duplicates or nesting['max_depth'] >= 4):
            report.append(f"  • Code looks well-structured! Minor cleanup opportunities may exist.")
        
        report.append("")
        
        return '\n'.join(report)


def analyze_directory(directory: str, recursive: bool = False):
    """Analyze all code files in a directory"""
    code_extensions = {'.py', '.js', '.ts', '.java', '.cpp', '.c', '.cs', '.go', '.rb', '.php', '.rs'}
    
    path = Path(directory)
    pattern = '**/*' if recursive else '*'
    
    results = []
    
    for file_path in path.glob(pattern):
        if file_path.is_file() and file_path.suffix in code_extensions:
            analyzer = CodeAnalyzer(str(file_path))
            if analyzer.lines:
                results.append((file_path, analyzer))
    
    # Summary report
    print(f"\n{'='*60}")
    print(f"Directory Analysis: {directory}")
    print(f"{'='*60}\n")
    print(f"Files analyzed: {len(results)}\n")
    
    # Individual reports
    for file_path, analyzer in results:
        print(analyzer.generate_report())


def main():
    parser = argparse.ArgumentParser(description='Analyze code for refactoring opportunities')
    parser.add_argument('path', help='Path to file or directory')
    parser.add_argument('-r', '--recursive', action='store_true', help='Recursively analyze directory')
    parser.add_argument('--report', action='store_true', help='Generate detailed report')
    
    args = parser.parse_args()
    
    if os.path.isfile(args.path):
        analyzer = CodeAnalyzer(args.path)
        print(analyzer.generate_report())
    elif os.path.isdir(args.path):
        analyze_directory(args.path, args.recursive)
    else:
        print(f"Error: {args.path} is not a valid file or directory")
        sys.exit(1)


if __name__ == '__main__':
    main()
