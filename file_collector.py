#!/usr/bin/env python3
"""
FILE COLLECTOR - Project Structure and Code Analysis Tool
========================================================

DESCRIPTION:
    This script recursively collects all text files from a directory and creates a 
    comprehensive report containing:
    - ASCII tree structure of files and folders
    - Code analysis showing functions and classes in source files
    - Token count estimates for each file
    - Optional full content of all collected files
    - Statistics about the collection process

    It's designed to work with modern web (Next.js, React) and Python projects,
    automatically ignoring common generated files like node_modules, __pycache__, etc.

INSTALLATION:
    1. Save this file to ~/scripts/file_collector.py (or any preferred location)
    2. Make it executable: chmod +x ~/scripts/file_collector.py
    3. Optional - Add to PATH:
       - Create ~/bin directory: mkdir -p ~/bin
       - Copy script there: cp ~/scripts/file_collector.py ~/bin/file_collector
       - Add to PATH in ~/.bashrc: export PATH="$HOME/bin:$PATH"
       - Reload: source ~/.bashrc

BASIC USAGE:
    python3 file_collector.py                    # Structure + code analysis (default)
    python3 file_collector.py --include-file-content  # Include full file contents
    python3 file_collector.py --simple           # Structure only, no code analysis
    
OUTPUT:
    Files are saved to .FILE_STATS/ directory in the current path with timestamp
    Default filename: YYYYMMDD_HHMMSS_FILE_STATS.md
    
OUTPUT OPTIONS:
    -o, --output FILE                # Specify output filename
    --output-file FILE               # Alternative way to specify output filename
    
FILTERING OPTIONS:
    --max-depth N                    # Limit directory traversal depth
    --max-size MB                    # Maximum file size to include (default: 1.0 MB)
    --add-ignore PATTERN [...]       # Add custom ignore patterns
    --clear-ignore                   # Clear default ignore patterns
    --show-ignore                    # Display current ignore patterns and exit
    
ANALYSIS OPTIONS:
    --no-code-analysis               # Disable function/class extraction
    --no-stats                       # Don't include collection statistics
    --no-token-count                 # Don't show token estimates
    --diff FILE1 FILE2               # Compare two FILE_STATS files

EXAMPLES:
    # Basic project snapshot
    python3 file_collector.py
    
    # Include all file contents
    python3 file_collector.py --include-file-content
    
    # Compare two snapshots
    python3 file_collector.py --diff .FILE_STATS/20240101_120000_FILE_STATS.md .FILE_STATS/20240102_120000_FILE_STATS.md
    
    # Quick overview of large project
    python3 file_collector.py --max-depth 3 --max-size 0.5
    
    # Custom output name
    python3 file_collector.py -o project_snapshot.md

CODE ANALYSIS SUPPORT:
    The script can extract functions and classes from:
    - Python (.py)
    - JavaScript/TypeScript (.js, .jsx, .ts, .tsx, .mjs, .cjs)
    - Java (.java)
    - C/C++ (.c, .cpp, .h, .hpp)
    - Go (.go)
    - Ruby (.rb)
    - PHP (.php)
    - Rust (.rs)
    - Swift (.swift)
    - Kotlin (.kt)
    - Vue (.vue)
    - Svelte (.svelte)

DEFAULT IGNORE PATTERNS:
    - Node.js: node_modules/, .next/, build/, dist/, package-lock.json, etc.
    - Python: __pycache__/, venv/, .pytest_cache/, *.pyc, etc.
    - Version Control: .git/, .svn/, .gitignore
    - IDEs: .vscode/, .idea/
    - OS: .DS_Store, Thumbs.db
    - File Collector: .FILE_STATS/
    - And many more (use --show-ignore to see full list)

AUTHOR: Stian Broen - CTO @ Kobben AS
CONTACT: stian@kobben.no
VERSION: 3.0
LICENSE: MIT
"""

import os
import argparse
import fnmatch
from pathlib import Path
from datetime import datetime
import sys
import re
import string

# Default ignore patterns for common project types
DEFAULT_IGNORE_PATTERNS = {
    # Next.js / React
    'node_modules/', '.next/', 'out/', 'build/', 'dist/', 'coverage/',
    '.cache/', '.parcel-cache/', '.vercel/', '.turbo/',
    '*.log', 'npm-debug.log*', 'yarn-debug.log*', 'yarn-error.log*',
    '.pnpm-debug.log*', '*.tsbuildinfo',
    
    # Python
    '__pycache__/', '*.py[cod]', '*$py.class', '.Python',
    'env/', 'venv/', 'ENV/', '.venv/', 'pip-log.txt',
    'pip-delete-this-directory.txt', '.tox/', '.coverage',
    '.coverage.*', '.pytest_cache/', 'htmlcov/', '*.egg-info/',
    '.eggs/', '*.egg', '.mypy_cache/', '.ruff_cache/',
    
    # Version Control
    '.git/', '.svn/', '.hg/', '.gitignore', '.gitattributes',
    
    # IDEs and Editors
    '.idea/', '.vscode/', '*.swp', '*.swo', '*~', '*.sublime-*',
    
    # OS
    '.DS_Store', 'Thumbs.db', 'desktop.ini',
    
    # Environment files
    '.env', '.env.*', '!.env.example',
    
    # Package managers
    'package-lock.json', 'yarn.lock', 'pnpm-lock.yaml',
    'poetry.lock', 'Pipfile.lock',
    
    # File Collector specific
    '.FILE_STATS/', '*_FILE_STATS.md',
    
    # Other
    '*.min.js', '*.min.css', '*.map', '.dockerignore',
    'filesCollection.txt'  # Legacy output file
}


def estimate_tokens(text):
    """
    Estimate token count for a text string.
    Rough approximation: 1 token ≈ 4 characters for English text
    """
    # More accurate estimation based on common patterns
    # Count words and special characters separately
    
    # Basic word count
    words = len(text.split())
    
    # Count special characters and numbers
    special_chars = sum(1 for c in text if c in string.punctuation or c.isdigit())
    
    # Rough estimation: words + (special_chars / 3)
    # This accounts for the fact that special characters often form their own tokens
    estimated_tokens = words + (special_chars // 3)
    
    # Alternative simple estimation
    char_based = len(text) // 4
    
    # Return average of both methods for better accuracy
    return (estimated_tokens + char_based) // 2


def parse_file_stats(filepath):
    """Parse a FILE_STATS file and extract structure information"""
    structure = {}
    current_path = []
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            in_structure = False
            for line in f:
                if line.strip() == "File Structure:":
                    in_structure = True
                    continue
                elif line.strip() == "Collection Statistics:" or line.strip() == "File Contents:":
                    break
                    
                if in_structure and line.strip():
                    # Parse tree structure
                    # This is a simplified parser - could be enhanced
                    if "├──" in line or "└──" in line:
                        level = (len(line) - len(line.lstrip()) - 4) // 4
                        filename = line.split("──", 1)[1].strip()
                        # Remove any code analysis info
                        if " -> " in filename:
                            filename = filename.split(" -> ")[0]
                        filename = filename.rstrip("/")
                        
                        # Update current path
                        current_path = current_path[:level]
                        current_path.append(filename)
                        
                        full_path = "/".join(current_path)
                        structure[full_path] = {
                            'exists': True,
                            'type': 'dir' if line.rstrip().endswith("/") else 'file'
                        }
    
    except Exception as e:
        print(f"Error parsing {filepath}: {e}")
        
    return structure


def compare_file_stats(file1, file2):
    """Compare two FILE_STATS files and show differences"""
    struct1 = parse_file_stats(file1)
    struct2 = parse_file_stats(file2)
    
    all_paths = set(struct1.keys()) | set(struct2.keys())
    
    added = []
    removed = []
    
    for path in sorted(all_paths):
        if path in struct2 and path not in struct1:
            added.append(path)
        elif path in struct1 and path not in struct2:
            removed.append(path)
    
    # Display results
    print(f"\nComparing FILE_STATS:")
    print(f"  Old: {file1}")
    print(f"  New: {file2}")
    print(f"{'=' * 60}\n")
    
    if added:
        print(f"Added ({len(added)} items):")
        for path in added:
            print(f"  + {path}")
        print()
    
    if removed:
        print(f"Removed ({len(removed)} items):")
        for path in removed:
            print(f"  - {path}")
        print()
    
    if not added and not removed:
        print("No structural changes detected.")
    
    print(f"\nSummary:")
    print(f"  Files/folders added: {len(added)}")
    print(f"  Files/folders removed: {len(removed)}")


class CodeAnalyzer:
    """Analyzes source code files to extract functions and classes"""
    
    # Regex patterns for different languages
    PATTERNS = {
        # Python
        '.py': {
            'functions': r'^\s*(?:async\s+)?def\s+(\w+)\s*\(',
            'classes': r'^\s*class\s+(\w+)\s*[\(:]'
        },
        # JavaScript/TypeScript
        '.js': {
            'functions': r'(?:^\s*(?:export\s+)?(?:async\s+)?function\s+(\w+)|^\s*(?:export\s+)?(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s+)?(?:\([^)]*\)\s*=>|function))',
            'classes': r'^\s*(?:export\s+)?class\s+(\w+)'
        },
        '.mjs': {
            'functions': r'(?:^\s*(?:export\s+)?(?:async\s+)?function\s+(\w+)|^\s*(?:export\s+)?(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s+)?(?:\([^)]*\)\s*=>|function))',
            'classes': r'^\s*(?:export\s+)?class\s+(\w+)'
        },
        '.cjs': {
            'functions': r'(?:^\s*(?:export\s+)?(?:async\s+)?function\s+(\w+)|^\s*(?:export\s+)?(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s+)?(?:\([^)]*\)\s*=>|function))',
            'classes': r'^\s*(?:export\s+)?class\s+(\w+)'
        },
        '.jsx': {
            'functions': r'(?:^\s*(?:export\s+)?(?:async\s+)?function\s+(\w+)|^\s*(?:export\s+)?(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s+)?(?:\([^)]*\)\s*=>|function))',
            'classes': r'^\s*(?:export\s+)?class\s+(\w+)'
        },
        '.ts': {
            'functions': r'(?:^\s*(?:export\s+)?(?:async\s+)?function\s+(\w+)|^\s*(?:export\s+)?(?:const|let|var)\s+(\w+)\s*[:=]\s*(?:async\s+)?(?:\([^)]*\)\s*=>|function))',
            'classes': r'^\s*(?:export\s+)?(?:abstract\s+)?class\s+(\w+)'
        },
        '.tsx': {
            'functions': r'(?:^\s*(?:export\s+)?(?:async\s+)?function\s+(\w+)|^\s*(?:export\s+)?(?:const|let|var)\s+(\w+)\s*[:=]\s*(?:async\s+)?(?:\([^)]*\)\s*=>|function))',
            'classes': r'^\s*(?:export\s+)?(?:abstract\s+)?class\s+(\w+)'
        },
        # Java
        '.java': {
            'functions': r'^\s*(?:public|private|protected|static|\s)+[\w\<\>\[\]]+\s+(\w+)\s*\([^)]*\)\s*(?:throws\s+[\w\s,]+)?\s*\{',
            'classes': r'^\s*(?:public|private|protected|abstract|final|\s)*\s*(?:class|interface|enum)\s+(\w+)'
        },
        # C/C++
        '.c': {
            'functions': r'^\s*(?:static\s+)?(?:inline\s+)?(?:const\s+)?[\w\*]+\s+[\*]*(\w+)\s*\([^)]*\)\s*\{',
            'classes': None  # C doesn't have classes
        },
        '.cpp': {
            'functions': r'^\s*(?:virtual\s+)?(?:static\s+)?(?:inline\s+)?(?:const\s+)?[\w\*\<\>]+\s+[\*]*(\w+)\s*\([^)]*\)(?:\s*const)?\s*(?:\{|;)',
            'classes': r'^\s*(?:template\s*<[^>]*>\s*)?(?:class|struct)\s+(\w+)'
        },
        '.h': {
            'functions': r'^\s*(?:virtual\s+)?(?:static\s+)?(?:inline\s+)?(?:const\s+)?[\w\*\<\>]+\s+[\*]*(\w+)\s*\([^)]*\)(?:\s*const)?\s*;',
            'classes': r'^\s*(?:template\s*<[^>]*>\s*)?(?:class|struct)\s+(\w+)'
        },
        '.hpp': {
            'functions': r'^\s*(?:virtual\s+)?(?:static\s+)?(?:inline\s+)?(?:const\s+)?[\w\*\<\>]+\s+[\*]*(\w+)\s*\([^)]*\)(?:\s*const)?\s*(?:\{|;)',
            'classes': r'^\s*(?:template\s*<[^>]*>\s*)?(?:class|struct)\s+(\w+)'
        },
        # Go
        '.go': {
            'functions': r'^\s*func\s+(?:\(\s*\w+\s+[\*]?\w+\s*\)\s+)?(\w+)\s*\(',
            'classes': r'^\s*type\s+(\w+)\s+struct\s*\{'
        },
        # Ruby
        '.rb': {
            'functions': r'^\s*def\s+(\w+)',
            'classes': r'^\s*class\s+(\w+)'
        },
        # PHP
        '.php': {
            'functions': r'^\s*(?:public|private|protected|static|\s)*\s*function\s+(\w+)\s*\(',
            'classes': r'^\s*(?:abstract\s+)?(?:final\s+)?class\s+(\w+)'
        },
        # Rust
        '.rs': {
            'functions': r'^\s*(?:pub\s+)?(?:async\s+)?fn\s+(\w+)',
            'classes': r'^\s*(?:pub\s+)?(?:struct|enum|trait)\s+(\w+)'
        },
        # Swift
        '.swift': {
            'functions': r'^\s*(?:public|private|internal|fileprivate|open|\s)*\s*func\s+(\w+)',
            'classes': r'^\s*(?:public|private|internal|fileprivate|open|\s)*\s*(?:class|struct|enum|protocol)\s+(\w+)'
        },
        # Kotlin
        '.kt': {
            'functions': r'^\s*(?:public|private|protected|internal|\s)*\s*fun\s+(\w+)',
            'classes': r'^\s*(?:public|private|protected|internal|abstract|final|open|\s)*\s*(?:class|interface|object|enum\s+class)\s+(\w+)'
        },
        # Vue.js
        '.vue': {
            'functions': r'(?:^\s*(?:export\s+)?(?:async\s+)?function\s+(\w+)|^\s*(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s+)?(?:\([^)]*\)\s*=>|function)|\s+(\w+)\s*\([^)]*\)\s*\{)',
            'classes': r'^\s*(?:export\s+)?class\s+(\w+)'
        },
        # Svelte
        '.svelte': {
            'functions': r'(?:^\s*(?:export\s+)?(?:async\s+)?function\s+(\w+)|^\s*(?:export\s+)?(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s+)?(?:\([^)]*\)\s*=>|function))',
            'classes': r'^\s*(?:export\s+)?class\s+(\w+)'
        }
    }
    
    @classmethod
    def analyze_file(cls, file_path):
        """Extract functions and classes from a source code file"""
        ext = Path(file_path).suffix.lower()
        if ext not in cls.PATTERNS:
            return None, None
        
        patterns = cls.PATTERNS[ext]
        functions = set()
        classes = set()
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    # Extract functions
                    if patterns.get('functions'):
                        try:
                            func_matches = re.finditer(patterns['functions'], line, re.MULTILINE)
                            for match in func_matches:
                                # Handle multiple groups (for JS/TS arrow functions)
                                func_name = None
                                for i in range(1, match.lastindex + 1 if match.lastindex else 1):
                                    if match.group(i):
                                        func_name = match.group(i)
                                        break
                                if func_name and not func_name.startswith('_'):  # Skip private functions in some languages
                                    # Additional check for common non-function names
                                    if func_name not in {'if', 'else', 'for', 'while', 'switch', 'case', 'try', 'catch'}:
                                        functions.add(func_name)
                        except re.error:
                            pass  # Skip if regex fails
                    
                    # Extract classes
                    if patterns.get('classes'):
                        try:
                            class_matches = re.finditer(patterns['classes'], line, re.MULTILINE)
                            for match in class_matches:
                                class_name = match.group(1)
                                if class_name:
                                    classes.add(class_name)
                        except re.error:
                            pass  # Skip if regex fails
        
        except Exception:
            # If we can't read the file, just return empty sets
            return None, None
        
        return sorted(functions) if functions else None, sorted(classes) if classes else None
    
    @classmethod
    def is_source_code_file(cls, file_path):
        """Check if a file is a source code file we can analyze"""
        ext = Path(file_path).suffix.lower()
        return ext in cls.PATTERNS


class FileCollector:
    def __init__(self, ignore_patterns=None, max_file_size=1024*1024, max_depth=None, analyze_code=True, show_tokens=True):
        self.ignore_patterns = ignore_patterns or DEFAULT_IGNORE_PATTERNS
        self.max_file_size = max_file_size  # Default 1MB
        self.max_depth = max_depth
        self.analyze_code = analyze_code
        self.show_tokens = show_tokens
        self.stats = {
            'total_files': 0,
            'collected_files': 0,
            'ignored_files': 0,
            'total_size': 0,
            'errors': 0,
            'total_tokens': 0
        }
    
    def should_ignore(self, path):
        """Check if a path should be ignored based on patterns"""
        path_str = str(path)
        name = os.path.basename(path_str)
        
        for pattern in self.ignore_patterns:
            # Handle directory patterns (ending with /)
            if pattern.endswith('/'):
                if os.path.isdir(path) and fnmatch.fnmatch(name, pattern[:-1]):
                    return True
            # Handle negation patterns (starting with !)
            elif pattern.startswith('!'):
                if fnmatch.fnmatch(name, pattern[1:]):
                    return False
            # Handle regular patterns
            elif fnmatch.fnmatch(name, pattern):
                return True
        
        return False
    
    def is_text_file(self, file_path):
        """Check if a file is likely to be a text file"""
        # Check file size first
        try:
            if os.path.getsize(file_path) > self.max_file_size:
                return False
        except OSError:
            return False
        
        # Common text file extensions
        text_extensions = {
            '.txt', '.md', '.py', '.js', '.jsx', '.ts', '.tsx', '.mjs', '.cjs',
            '.html', '.css', '.scss', '.sass', '.json', '.xml', '.yaml', '.yml',
            '.ini', '.cfg', '.conf', '.sh', '.bash', '.zsh', '.fish',
            '.c', '.cpp', '.h', '.hpp', '.java', '.rb', '.go', '.rs',
            '.php', '.sql', '.r', '.m', '.swift', '.kt', '.scala',
            '.clj', '.el', '.vim', '.lua', '.pl', '.pm', '.tcl',
            '.awk', '.sed', '.makefile', '.dockerfile', '.gitignore',
            '.env', '.properties', '.toml', '.lock', '.sum', '.mod',
            '.vue', '.svelte'
        }
        
        # Check by extension first
        ext = Path(file_path).suffix.lower()
        if ext in text_extensions:
            return True
        
        # No extension files that are commonly text
        base_name = os.path.basename(file_path).lower()
        text_files = {
            'readme', 'license', 'makefile', 'dockerfile',
            'jenkinsfile', 'rakefile', 'gemfile', 'procfile'
        }
        if base_name in text_files:
            return True
        
        # Try reading as text
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                f.read(1024)
            return True
        except (UnicodeDecodeError, OSError):
            return False
    
    def create_ascii_tree(self, path, prefix="", is_last=True, current_depth=0):
        """Generate ASCII tree structure for the given path"""
        if self.max_depth is not None and current_depth > self.max_depth:
            return ""
        
        base_name = os.path.basename(path) or os.path.basename(os.getcwd())
        
        if current_depth == 0:
            tree_str = base_name + "/\n"
        else:
            tree_str = prefix + ("└── " if is_last else "├── ") + base_name
            
            # Add code analysis and token count for files
            if os.path.isfile(path):
                info_parts = []
                
                # Add token count if enabled for text files (not in simple mode)
                if self.show_tokens and self.analyze_code and self.is_text_file(path):
                    try:
                        with open(path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            tokens = estimate_tokens(content)
                            info_parts.append(f"~{tokens} tokens")
                            self.stats['total_tokens'] += tokens
                    except:
                        pass
                
                # Add functions and classes for source code files
                if self.analyze_code and CodeAnalyzer.is_source_code_file(path):
                    functions, classes = CodeAnalyzer.analyze_file(path)
                    if functions:
                        func_list = [f[:20] + '...' if len(f) > 20 else f for f in functions[:5]]
                        info_parts.append(f"Functions: ({', '.join(func_list)}{', ...' if len(functions) > 5 else ''})")
                    if classes:
                        class_list = [c[:20] + '...' if len(c) > 20 else c for c in classes[:5]]
                        info_parts.append(f"Classes: ({', '.join(class_list)}{', ...' if len(classes) > 5 else ''})")
                
                if info_parts:
                    tree_str += " -> " + ", ".join(info_parts)
            
            elif os.path.isdir(path) and not self.should_ignore(path):
                tree_str += "/"
            
            tree_str += "\n"
        
        if current_depth > 0:
            prefix += "    " if is_last else "│   "
        
        if os.path.isdir(path) and not self.should_ignore(path):
            try:
                items = sorted(os.listdir(path))
                # Filter out ignored items
                items = [item for item in items if not self.should_ignore(os.path.join(path, item))]
                
                for i, item in enumerate(items):
                    item_path = os.path.join(path, item)
                    is_last_item = i == len(items) - 1
                    tree_str += self.create_ascii_tree(item_path, prefix, is_last_item, current_depth + 1)
            except PermissionError:
                self.stats['errors'] += 1
        
        return tree_str
    
    def collect_text_files(self, start_path):
        """Recursively collect all text files from the given path"""
        text_files = []
        
        for root, dirs, files in os.walk(start_path):
            # Calculate depth
            depth = root[len(start_path):].count(os.sep)
            if self.max_depth is not None and depth >= self.max_depth:
                dirs[:] = []  # Don't recurse deeper
                continue
            
            # Filter directories
            dirs[:] = [d for d in dirs if not self.should_ignore(os.path.join(root, d))]
            
            for file in files:
                self.stats['total_files'] += 1
                file_path = os.path.join(root, file)
                
                if self.should_ignore(file_path):
                    self.stats['ignored_files'] += 1
                    continue
                
                if self.is_text_file(file_path):
                    text_files.append(file_path)
                    self.stats['collected_files'] += 1
                    try:
                        self.stats['total_size'] += os.path.getsize(file_path)
                    except OSError:
                        pass
                else:
                    self.stats['ignored_files'] += 1
        
        return sorted(text_files)
    
    def format_size(self, size):
        """Format size in human-readable format"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.2f} {unit}"
            size /= 1024.0
        return f"{size:.2f} TB"
    
    def write_statistics(self, f):
        """Write collection statistics"""
        f.write("\nCollection Statistics:\n")
        f.write("=====================\n")
        f.write(f"Total files found: {self.stats['total_files']}\n")
        f.write(f"Files collected: {self.stats['collected_files']}\n")
        f.write(f"Files ignored: {self.stats['ignored_files']}\n")
        f.write(f"Total size: {self.format_size(self.stats['total_size'])}\n")
        if self.show_tokens:
            f.write(f"Estimated tokens: {self.stats['total_tokens']:,}\n")
        if self.stats['errors'] > 0:
            f.write(f"Errors encountered: {self.stats['errors']}\n")
        f.write(f"Collection date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("\n")


def main():
    parser = argparse.ArgumentParser(
        description='Recursively collect text files and create a structured ASCII representation',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                     # Create structure analysis in .FILE_STATS/
  %(prog)s --include-file-content  # Include full file contents
  %(prog)s --simple           # Only show file structure, no code analysis
  %(prog)s -o custom.md       # Specify custom output filename
  %(prog)s --diff file1.md file2.md  # Compare two FILE_STATS files
  %(prog)s --max-depth 3      # Limit directory depth to 3 levels
  %(prog)s --max-size 5       # Set max file size to 5MB
  %(prog)s --no-stats         # Don't include statistics
  %(prog)s --no-code-analysis # Don't analyze functions/classes in source files
  %(prog)s --no-token-count   # Don't show token estimates
  %(prog)s --add-ignore "*.tmp" "temp/"  # Add custom ignore patterns
        """
    )
    
    parser.add_argument('--include-file-content', action='store_true',
                       help='Include full file contents (default is structure and code analysis only)')
    parser.add_argument('-s', '--simple', action='store_true',
                       help='Output only the file structure, skip code analysis')
    parser.add_argument('-o', '--output', metavar='FILE',
                       help='Output file name (default: timestamp-based FILE_STATS.md)')
    parser.add_argument('--output-file', metavar='FILE',
                       help='Alternative way to specify output filename (overrides -o)')
    parser.add_argument('--max-depth', type=int, metavar='N',
                       help='Maximum directory depth to traverse')
    parser.add_argument('--max-size', type=float, default=1.0, metavar='MB',
                       help='Maximum file size in MB to include (default: 1.0)')
    parser.add_argument('--no-stats', action='store_true',
                       help="Don't include collection statistics")
    parser.add_argument('--no-code-analysis', action='store_true',
                       help="Don't analyze functions/classes in source files")
    parser.add_argument('--add-ignore', nargs='+', metavar='PATTERN',
                       help='Additional patterns to ignore')
    parser.add_argument('--clear-ignore', action='store_true',
                       help='Clear default ignore patterns (use only custom ones)')
    parser.add_argument('--show-ignore', action='store_true',
                       help='Show current ignore patterns and exit')
    parser.add_argument('--diff', nargs=2, metavar=('FILE1', 'FILE2'),
                       help='Compare two FILE_STATS files and show differences')
    parser.add_argument('--no-token-count', action='store_true',
                       help="Don't include token count estimates in the tree")
    
    args = parser.parse_args()
    
    # Handle diff mode
    if args.diff:
        compare_file_stats(args.diff[0], args.diff[1])
        return
    
    # Handle ignore patterns
    if args.clear_ignore:
        ignore_patterns = set()
    else:
        ignore_patterns = DEFAULT_IGNORE_PATTERNS.copy()
    
    if args.add_ignore:
        ignore_patterns.update(args.add_ignore)
    
    if args.show_ignore:
        print("Current ignore patterns:")
        for pattern in sorted(ignore_patterns):
            print(f"  {pattern}")
        return
    
    # Create .FILE_STATS directory
    current_path = os.getcwd()
    file_stats_dir = os.path.join(current_path, ".FILE_STATS")
    os.makedirs(file_stats_dir, exist_ok=True)
    
    # Handle output file
    if args.output_file:
        output_filename = args.output_file
    elif args.output:
        output_filename = args.output
    else:
        # Default timestamp-based filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"{timestamp}_FILE_STATS.md"
    
    output_path = os.path.join(file_stats_dir, output_filename)
    
    # Always ignore the .FILE_STATS directory
    ignore_patterns.add(".FILE_STATS/")
    ignore_patterns.add("FILE_STATS.md")
    
    # Create collector
    collector = FileCollector(
        ignore_patterns=ignore_patterns,
        max_file_size=int(args.max_size * 1024 * 1024),
        max_depth=args.max_depth,
        analyze_code=not args.no_code_analysis and not args.simple,
        show_tokens=not args.no_token_count and not args.simple
    )
    
    print(f"Collecting files from: {current_path}")
    print(f"Output file: {output_path}")
    print(f"Max file size: {args.max_size} MB")
    if args.max_depth:
        print(f"Max depth: {args.max_depth}")
    print(f"Code analysis: {'Enabled' if not args.no_code_analysis else 'Disabled'}")
    print(f"Token counting: {'Enabled' if not args.no_token_count else 'Disabled'}")
    print()
    
    # Collect all text files
    print("Scanning directory structure...")
    text_files = collector.collect_text_files(current_path)
    
    if args.include_file_content:
        print(f"Found {collector.stats['collected_files']} text files to collect")
    print(f"Writing to {output_path}...")
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            # Write header
            f.write(f"# File Collection Report\n")
            f.write(f"Generated from: {current_path}\n")
            f.write(f"{'=' * 50}\n\n")
            
            # Write ASCII tree structure
            f.write("## File Structure:\n")
            f.write("================\n\n")
            f.write("```\n")
            tree = collector.create_ascii_tree(current_path)
            f.write(tree)
            f.write("```\n\n")
            
            # Write statistics if requested
            if not args.no_stats:
                collector.write_statistics(f)
            
            if args.include_file_content:
                # Write file contents
                f.write("## File Contents:\n")
                f.write("================\n\n")
                
                for i, file_path in enumerate(text_files, 1):
                    rel_path = os.path.relpath(file_path, current_path)
                    
                    # Progress indicator
                    print(f"\rProcessing file {i}/{len(text_files)}: {rel_path[:50]:<50}", end='', flush=True)
                    
                    f.write(f"### [{rel_path}]\n")
                    f.write("=" * (len(rel_path) + 2) + "\n\n")
                    
                    try:
                        with open(file_path, 'r', encoding='utf-8') as file:
                            content = file.read()
                            f.write("```\n")
                            f.write(content)
                            if not content.endswith('\n'):
                                f.write('\n')
                            f.write("```\n")
                    except Exception as e:
                        f.write(f"Error reading file: {str(e)}\n")
                        collector.stats['errors'] += 1
                    
                    f.write("\n" + "-" * 80 + "\n\n")
        
        if args.include_file_content:
            print(f"\n\nCollection complete! Output written to {output_path}")
        else:
            print(f"\nStructure analysis complete! Output written to {output_path}")
        
        print(f"\nRemember to add '.FILE_STATS/' to your .gitignore file!")
        
        if args.include_file_content:
            print(f"Total size of collected files: {collector.format_size(collector.stats['total_size'])}")
        
    except Exception as e:
        print(f"\nError writing output file: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()