#!/usr/bin/env python3
"""
Trace dependencies for a given focus file by analyzing import statements,
require calls, and other dependency patterns across multiple languages.
"""

import os
import re
import sys
from pathlib import Path
from typing import Set, Dict, List, Tuple


class DependencyTracer:
    """Trace dependencies across multiple programming languages."""
    
    def __init__(self, repo_root: str):
        self.repo_root = Path(repo_root).resolve()
        self.file_map: Dict[str, Path] = {}
        self._build_file_map()
        
    def _build_file_map(self):
        """Build a map of module names to file paths."""
        for root, dirs, files in os.walk(self.repo_root):
            # Skip common ignored directories
            dirs[:] = [d for d in dirs if d not in {'.git', '__pycache__', 'node_modules', 'venv', '.venv', 'dist', 'build'}]
            
            for file in files:
                if file.endswith(('.py', '.js', '.jsx', '.ts', '.tsx', '.go', '.java', '.cpp', '.c', '.h', '.hpp')):
                    file_path = Path(root) / file
                    rel_path = file_path.relative_to(self.repo_root)
                    self.file_map[str(rel_path)] = file_path
    
    def trace_dependencies(self, focus_file: str) -> Set[Path]:
        """
        Trace all dependencies for a given focus file.
        Returns a set of file paths that the focus file depends on.
        """
        focus_path = (self.repo_root / focus_file).resolve()
        if not focus_path.exists():
            raise FileNotFoundError(f"Focus file not found: {focus_file}")
        
        dependencies: Set[Path] = set()
        visited: Set[Path] = set()
        to_process = [focus_path]
        
        while to_process:
            current_file = to_process.pop()
            
            if current_file in visited:
                continue
            
            visited.add(current_file)
            
            # Get direct dependencies
            deps = self._get_direct_dependencies(current_file)
            
            for dep in deps:
                if dep not in dependencies and dep != focus_path:
                    dependencies.add(dep)
                    if dep not in visited:
                        to_process.append(dep)
        
        return dependencies
    
    def _get_direct_dependencies(self, file_path: Path) -> Set[Path]:
        """Extract direct dependencies from a file based on its language."""
        deps: Set[Path] = set()
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception:
            return deps
        
        ext = file_path.suffix
        
        if ext == '.py':
            deps.update(self._parse_python_imports(content, file_path))
        elif ext in {'.js', '.jsx', '.ts', '.tsx'}:
            deps.update(self._parse_js_imports(content, file_path))
        elif ext == '.go':
            deps.update(self._parse_go_imports(content, file_path))
        elif ext in {'.java'}:
            deps.update(self._parse_java_imports(content, file_path))
        elif ext in {'.c', '.cpp', '.h', '.hpp'}:
            deps.update(self._parse_c_includes(content, file_path))
        
        return deps
    
    def _parse_python_imports(self, content: str, file_path: Path) -> Set[Path]:
        """Parse Python import statements."""
        deps: Set[Path] = set()
        
        # Match: import module, from module import x, from . import x, from ..module import x
        patterns = [
            r'^\s*import\s+([a-zA-Z_][\w.]*)',
            r'^\s*from\s+([a-zA-Z_][\w.]*)\s+import',
            r'^\s*from\s+(\.+[\w.]*)\s+import',
        ]
        
        for pattern in patterns:
            for match in re.finditer(pattern, content, re.MULTILINE):
                module = match.group(1)
                resolved = self._resolve_python_module(module, file_path)
                if resolved:
                    deps.add(resolved)
        
        return deps
    
    def _resolve_python_module(self, module: str, current_file: Path) -> Path | None:
        """Resolve a Python module to a file path."""
        # Handle relative imports
        if module.startswith('.'):
            parts = module.split('.')
            level = len([p for p in parts if p == ''])
            module_parts = [p for p in parts if p]
            
            parent = current_file.parent
            for _ in range(level - 1):
                parent = parent.parent
            
            if module_parts:
                target = parent / '/'.join(module_parts)
            else:
                target = parent
            
            # Check for __init__.py or .py file
            if (target / '__init__.py').exists():
                return target / '__init__.py'
            if (target.parent / f'{target.name}.py').exists():
                return target.parent / f'{target.name}.py'
        
        # Handle absolute imports
        module_path = module.replace('.', '/')
        
        # Try as package
        package_init = self.repo_root / module_path / '__init__.py'
        if package_init.exists():
            return package_init
        
        # Try as module
        module_file = self.repo_root / f'{module_path}.py'
        if module_file.exists():
            return module_file
        
        return None
    
    def _parse_js_imports(self, content: str, file_path: Path) -> Set[Path]:
        """Parse JavaScript/TypeScript import statements."""
        deps: Set[Path] = set()
        
        # Match: import x from 'path', require('path'), import('path')
        patterns = [
            r'import\s+.*?\s+from\s+["\']([^"\']+)["\']',
            r'require\s*\(["\']([^"\']+)["\']\)',
            r'import\s*\(["\']([^"\']+)["\']\)',
        ]
        
        for pattern in patterns:
            for match in re.finditer(pattern, content):
                import_path = match.group(1)
                resolved = self._resolve_js_import(import_path, file_path)
                if resolved:
                    deps.add(resolved)
        
        return deps
    
    def _resolve_js_import(self, import_path: str, current_file: Path) -> Path | None:
        """Resolve a JavaScript import to a file path."""
        # Skip node_modules
        if import_path.startswith('.'):
            # Relative import
            base = current_file.parent
            target_path = (base / import_path).resolve()
            
            # Try different extensions
            for ext in ['', '.js', '.jsx', '.ts', '.tsx', '/index.js', '/index.jsx', '/index.ts', '/index.tsx']:
                check_path = Path(str(target_path) + ext)
                if check_path.exists() and check_path.is_relative_to(self.repo_root):
                    return check_path
        
        return None
    
    def _parse_go_imports(self, content: str, file_path: Path) -> Set[Path]:
        """Parse Go import statements."""
        deps: Set[Path] = set()
        
        # Match: import "path" and import ( "path1" "path2" )
        patterns = [
            r'import\s+"([^"]+)"',
            r'import\s+\([^)]*"([^"]+)"[^)]*\)',
        ]
        
        for pattern in patterns:
            for match in re.finditer(pattern, content, re.DOTALL):
                # Only handle local imports (relative paths)
                import_path = match.group(1)
                if import_path.startswith('.'):
                    resolved = self._resolve_go_import(import_path, file_path)
                    if resolved:
                        deps.add(resolved)
        
        return deps
    
    def _resolve_go_import(self, import_path: str, current_file: Path) -> Path | None:
        """Resolve a Go import to a file path."""
        if import_path.startswith('.'):
            base = current_file.parent
            target_dir = (base / import_path).resolve()
            
            if target_dir.is_dir() and target_dir.is_relative_to(self.repo_root):
                # Return the directory as Go packages are directories
                return target_dir
        
        return None
    
    def _parse_java_imports(self, content: str, file_path: Path) -> Set[Path]:
        """Parse Java import statements."""
        deps: Set[Path] = set()
        
        # Match: import package.Class;
        pattern = r'import\s+([\w.]+);'
        
        for match in re.finditer(pattern, content):
            import_path = match.group(1)
            resolved = self._resolve_java_import(import_path)
            if resolved:
                deps.add(resolved)
        
        return deps
    
    def _resolve_java_import(self, import_path: str) -> Path | None:
        """Resolve a Java import to a file path."""
        # Convert package.Class to package/Class.java
        file_path = import_path.replace('.', '/') + '.java'
        full_path = self.repo_root / file_path
        
        if full_path.exists():
            return full_path
        
        return None
    
    def _parse_c_includes(self, content: str, file_path: Path) -> Set[Path]:
        """Parse C/C++ include statements."""
        deps: Set[Path] = set()
        
        # Match: #include "file.h" and #include <file.h>
        patterns = [
            r'#include\s+"([^"]+)"',
            r'#include\s+<([^>]+)>',
        ]
        
        for pattern in patterns:
            for match in re.finditer(pattern, content):
                include_path = match.group(1)
                resolved = self._resolve_c_include(include_path, file_path)
                if resolved:
                    deps.add(resolved)
        
        return deps
    
    def _resolve_c_include(self, include_path: str, current_file: Path) -> Path | None:
        """Resolve a C/C++ include to a file path."""
        # Try relative to current file
        rel_path = (current_file.parent / include_path).resolve()
        if rel_path.exists() and rel_path.is_relative_to(self.repo_root):
            return rel_path
        
        # Try relative to repo root
        root_path = self.repo_root / include_path
        if root_path.exists():
            return root_path
        
        return None


def main():
    if len(sys.argv) < 3:
        print("Usage: python trace_dependencies.py <repo_root> <focus_file>")
        print("Example: python trace_dependencies.py /path/to/repo train.py")
        sys.exit(1)
    
    repo_root = sys.argv[1]
    focus_file = sys.argv[2]
    
    tracer = DependencyTracer(repo_root)
    
    try:
        dependencies = tracer.trace_dependencies(focus_file)
        
        print(f"Dependencies for {focus_file}:")
        print("-" * 60)
        
        if dependencies:
            for dep in sorted(dependencies):
                rel_path = dep.relative_to(tracer.repo_root)
                print(f"  {rel_path}")
        else:
            print("  No dependencies found")
        
        print("-" * 60)
        print(f"Total: {len(dependencies)} files")
        
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
