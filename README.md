# File Collector - Project Structure and Code Analysis Tool

A Python script that creates comprehensive snapshots of your project structure, analyzes source code to extract functions and classes, estimates token counts for AI context windows, and optionally includes full file contents. Perfect for documentation, code reviews, and sharing project context with AI assistants like Claude Code.

**Repository**: https://github.com/Stiander/filecollector  
**Issues**: https://github.com/Stiander/filecollector/issues  
**Author**: [@Stiander](https://github.com/Stiander) , Stian Broen - CTO @ Kobben AS
**Contact** stian@kobben.no
**Models used** v1 : Claude Sonnet 3.5 , v2,v3 : Claude Opus 4

[![GitHub](https://img.shields.io/github/license/Stiander/filecollector)](https://github.com/Stiander/filecollector/blob/main/LICENSE)
[![Python](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)

## Quick Start

```bash
# Clone and install
git clone https://github.com/Stiander/filecollector.git
cd filecollector && bash install_file_collector.sh && source ~/.bashrc

# Generate project snapshot (saved to .FILE_STATS/)
file_collector

# Include file contents
file_collector --include-file-content
```

## What's New in Version 3.0

### 🔄 Major Changes
- **Default behavior**: Now shows structure + code analysis only (no file contents)
- **Token counting**: Each file shows estimated tokens for AI context planning
- **Auto-organized output**: Files saved to `.FILE_STATS/` with timestamps
- **Diff feature**: Compare snapshots to track changes
- **Removed options**: `--describe-only` (now default), `--output-folder` (always `.FILE_STATS/`)

### 📊 Example Output
```
project/
├── src/
│   ├── main.py -> ~1,234 tokens, Functions: (main, setup_app), Classes: (App)
│   ├── utils.py -> ~567 tokens, Functions: (validate_email, hash_password)
│   └── models.py -> ~890 tokens, Classes: (User, Product, Order)
└── README.md -> ~234 tokens
```
  - [Basic Commands](#basic-commands)
  - [Output Options](#output-options)
  - [Filtering Options](#filtering-options)
  - [Code Analysis](#code-analysis)
- [Using with Claude Code](#using-with-claude-code)
  - [Common Use Cases](#common-use-cases-with-claude-code)
  - [Optimizing for Context Windows](#optimizing-for-context-windows)
  - [Quick Start for Claude Code](#quick-start-for-claude-code)
  - [Best Practices](#best-practices-for-claude-code)
  - [Recommended Workflow](#recommended-workflow)
  - [Integration Tips](#integration-tips)
- [Supported Languages](#supported-languages)
- [Default Ignore Patterns](#default-ignore-patterns)
- [Advanced Features](#advanced-features)
- [Troubleshooting](#troubleshooting)
- [Examples](#examples)

## Features

- 📂 **ASCII Tree Structure** - Visual representation of your project hierarchy
- 🔍 **Code Analysis** - Automatically extracts functions and classes from source files
- 📝 **Full Content Collection** - Optionally includes complete file contents
- 🚀 **Smart Filtering** - Automatically ignores common build artifacts and dependencies
- 📊 **Statistics** - Reports on files collected, ignored, and total size
- 🎯 **Flexible Output** - Save to any folder with custom filenames
- 🌐 **Multi-Language Support** - Analyzes Python, JavaScript, TypeScript, Java, Go, and more

## What It Does

The File Collector script scans your project directory and creates a comprehensive report containing:

1. **Project Structure**: An ASCII tree showing all files and folders
2. **Code Intelligence**: Functions and classes found in each source file
3. **File Contents**: Optional full text of all collected files
4. **Statistics**: Summary of what was collected and ignored

### Example Output

```
project/
├── src/
│   ├── main.py -> Functions: (main, setup_app, run_server), Classes: (Application)
│   ├── models.py -> Classes: (User, Product, Order)
│   └── utils.py -> Functions: (validate_email, hash_password)
├── components/
│   ├── Button.tsx -> Functions: (Button), Classes: (ButtonProps)
│   └── Card.tsx -> Functions: (Card, CardHeader)
└── tests/
    └── test_main.py -> Functions: (test_setup, test_server), Classes: (TestMain)
```

## Installation

### Quick Install (Recommended)
```bash
# Clone and install
git clone https://github.com/Stiander/filecollector.git
cd filecollector && bash install_file_collector.sh && source ~/.bashrc

# Verify it works
file_collector --help
```

### Alternative: Direct Download
```bash
# Download and install directly
mkdir -p ~/bin
curl -o ~/bin/file_collector https://raw.githubusercontent.com/Stiander/filecollector/main/file_collector.py
chmod +x ~/bin/file_collector

# Add to PATH if not already there
echo 'export PATH="$HOME/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Test it works
file_collector --help
```

### Troubleshooting Installation

**"file_collector: command not found"**

This usually means `~/bin` is not in your system's `PATH`.

```bash
# 1. Check if file exists
ls -la ~/bin/file_collector

# 2. Check if ~/bin is in PATH
echo $PATH | grep -q "$HOME/bin" && echo "✅ ~/bin in PATH" || echo "❌ ~/bin not in PATH"

# 3. If not in PATH, add it and reload your shell:
echo 'export PATH="$HOME/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# 4. If the file doesn't exist, the installation failed. Try again.
```

**"Error: Please replace this file with the actual file_collector.py script"**

This means the installer may have created a placeholder. Copy the real script:
```bash
# Navigate to the cloned repository
cd path/to/filecollector
# Copy the correct script
cp file_collector.py ~/bin/file_collector
chmod +x ~/bin/file_collector
```

### For Claude Code Users (WSL/Linux)

A clear, step-by-step workflow for getting started.

**Step 1: Install**
```bash
cd ~
git clone https://github.com/Stiander/filecollector.git
cd filecollector
bash install_file_collector.sh
source ~/.bashrc
```

**Step 2: Verify Installation**
```bash
file_collector --help
# You should see the help text, not "command not found" or "replace this file".
```

**Step 3: Test on Your Project**
```bash
# Navigate to your project directory
cd /path/to/your/project

# Run the collector
file_collector --max-depth 3

# Check for the output directory
ls .FILE_STATS/
# You should see a generated file inside.
```

**Step 4: Add Output Directory to .gitignore**
```bash
echo ".FILE_STATS/" >> .gitignore
```

## Usage

### Basic Commands

```bash
# Default: Structure + code analysis + token counts (NO file contents)
file_collector

# Include full file contents (old default behavior)
file_collector --include-file-content

# Simple structure only (no code analysis, no token counts)
file_collector --simple

# Compare two snapshots
file_collector --diff .FILE_STATS/20240115_120000_FILE_STATS.md .FILE_STATS/20240115_140000_FILE_STATS.md

# Show help
file_collector --help
```

### Output Management

All files are automatically saved to `.FILE_STATS/` directory with timestamp-based names:

```bash
# Default output: .FILE_STATS/YYYYMMDD_HHMMSS_FILE_STATS.md
file_collector

# Custom filename (still in .FILE_STATS/)
file_collector -o my_snapshot.md
file_collector --output-file my_snapshot.md

# List all snapshots
ls -la .FILE_STATS/

# Don't forget to add to .gitignore!
echo ".FILE_STATS/" >> .gitignore
```

### Filtering Options

```bash
# Limit directory depth
file_collector --max-depth 3

# Limit file size (in MB)
file_collector --max-size 0.5

# Add custom ignore patterns
file_collector --add-ignore "*.log" "*.tmp" "temp_*"

# Clear default ignore patterns (use only custom)
file_collector --clear-ignore --add-ignore "node_modules/" "*.pyc"

# Show current ignore patterns
file_collector --show-ignore
```

### Code Analysis

```bash
# Disable code analysis for faster processing
file_collector --no-code-analysis

# Disable token counting
file_collector --no-token-count

# Disable statistics
file_collector --no-stats

# Minimal output (structure only)
file_collector --simple --no-stats
```

### Diff Feature

Compare two FILE_STATS snapshots to see what changed:

```bash
# Compare two snapshots
file_collector --diff .FILE_STATS/20240115_120000_FILE_STATS.md .FILE_STATS/20240115_140000_FILE_STATS.md

# Example output:
# Comparing FILE_STATS:
#   Old: .FILE_STATS/20240115_120000_FILE_STATS.md
#   New: .FILE_STATS/20240115_140000_FILE_STATS.md
# ============================================================
# 
# Added (3 items):
#   + src/new_feature.py
#   + tests/test_new_feature.py
#   + docs/new_feature.md
# 
# Removed (1 items):
#   - src/deprecated.py
# 
# Summary:
#   Files/folders added: 3
#   Files/folders removed: 1
```

## Using with Claude Code

File Collector is particularly useful for sharing project context with Claude Code or other AI assistants. It helps Claude understand your project structure, identify key components, and provide more accurate assistance.

### Common Use Cases with Claude Code

- **Code Review**: Share your project structure for architectural feedback
- **Debugging Help**: Provide context about where issues might be occurring  
- **Feature Development**: Show existing patterns for Claude to follow
- **Documentation**: Get help documenting your code structure
- **Refactoring**: Analyze current structure before making changes

### Optimizing for Context Windows

When working with Claude Code, it's crucial to be strategic about context usage. Claude's context windows, while large, are not unlimited. The new token counting feature helps you plan your context usage effectively.

#### Context Window Considerations

- **Claude Opus 4**: Larger context window, but still benefits from strategic usage
- **Claude Sonnet 4**: More limited context, requires careful planning
- **Token Estimates**: Each file shows estimated tokens to help you budget context

#### Recommended Strategy for Large Projects

##### 1. **Create a CLAUDE.md Memory File**

Create a `CLAUDE.md` file in your project root that documents your File Collector strategy:

```markdown
# Project Context Strategy for Claude

## File Collector Usage Instructions

This project uses the File Collector tool strategically to manage context.
All outputs are saved to .FILE_STATS/ directory.

### Stage 1: Project Overview (5-20K tokens)
\```bash
file_collector --max-depth 3
# Check latest output in .FILE_STATS/
# Look for "Estimated tokens:" line
\```

### Stage 2: Component Deep Dives (10-50K tokens)
\```bash
# For specific component work
cd src/components/UserAuth
file_collector
# Still just structure - no code yet
\```

### Stage 3: Code Inclusion (50-150K tokens)
\```bash
# Include actual implementation
file_collector --include-file-content --max-size 0.1
# Now includes file contents
\```

### Stage 4: Focused Debugging (20-80K tokens)
\```bash
# Very targeted analysis
file_collector --max-depth 1 --include-file-content --add-ignore "*.test.js"
\```

## Token Budget Guidelines:
- Initial discussion: Use ~5-20K tokens (structure only)
- Feature work: Use ~20-50K tokens (detailed structure)
- Implementation: Use ~50-100K tokens (include code)
- Deep debugging: Use ~80-150K tokens (full context)
- Never exceed 150K tokens in one conversation

## Checking Token Count:
\```bash
# Quick check of latest snapshot
grep "Estimated tokens:" .FILE_STATS/$(ls -t .FILE_STATS/ | head -1)

# Or use the claude-check function
claude-check
\```

## DO NOT:
- Run file_collector --include-file-content on the entire project
- Include node_modules or build artifacts
- Combine multiple full component dumps in one conversation

## Project-Specific Token Estimates:
- Full project structure: ~25K tokens
- src/auth/: ~12K tokens (structure), ~45K (with code)
- src/api/: ~8K tokens (structure), ~35K (with code)  
- src/models/: ~5K tokens (structure), ~15K (with code)
- src/components/: ~30K tokens (structure), ~120K (with code)
```

##### 2. **Progressive Context Loading**

Use token counts to manage your context budget:

```bash
# First: Check project size
file_collector --max-depth 2
# Output shows: "Estimated tokens: 15,234"

# If under 20K tokens, get more detail
file_collector --max-depth 4
# Output shows: "Estimated tokens: 45,678"

# For specific work, include code
cd src/api
file_collector --include-file-content --max-size 0.05
# Output shows: "Estimated tokens: 89,123"
```

##### 3. **Token Budget Guidelines**

Based on the token estimates shown in each file:

| Context Level | Command | Token Range | Use Case |
|--------------|---------|-------------|-----------|
| Overview | `file_collector --max-depth 3` | 5-20K | Initial discussion |
| Component | `file_collector` in subdirectory | 10-30K | Feature planning |
| Code Review | `--include-file-content --max-size 0.1` | 30-100K | Implementation |
| Full Detail | `--include-file-content` | 100K+ | Deep debugging |

##### 4. **Smart Aliases for Context Management**

Add these to your `~/.bashrc`:

```bash
# Claude context management with token awareness
alias claude-overview='file_collector --max-depth 3 --no-code-analysis'
alias claude-detail='file_collector --max-depth 5'
alias claude-code='file_collector --include-file-content --max-size 0.1'

# Function to check token usage
claude-check() {
    local latest=$(ls -t .FILE_STATS/*_FILE_STATS.md 2>/dev/null | head -1)
    if [ -f "$latest" ]; then
        echo "Latest snapshot: $latest"
        grep "Estimated tokens:" "$latest" || echo "No token count found"
        echo ""
        local tokens=$(grep "Estimated tokens:" "$latest" | sed 's/[^0-9]//g')
        if [ -n "$tokens" ]; then
            if [ "$tokens" -gt 100000 ]; then
                echo "⚠️  Very large context ($tokens tokens) - consider filtering"
            elif [ "$tokens" -gt 50000 ]; then
                echo "⚡ Large context ($tokens tokens) - good for detailed work"
            else
                echo "✅ Optimal context size ($tokens tokens)"
            fi
        fi
    else
        echo "No snapshots found in .FILE_STATS/"
    fi
}

# Generate and check in one command
claude-snap() {
    file_collector "$@"
    claude-check
}
```

#### Example Workflow for Large Next.js Project

```bash
# 1. Initial exploration
file_collector --max-depth 3
claude-check  # Shows: "✅ Optimal context size (15,234 tokens)"

# 2. Component structure
cd src/components
file_collector
claude-check  # Shows: "⚡ Large context (45,678 tokens)"

# 3. Specific feature with code
cd src/features/auth
file_collector --include-file-content --max-size 0.05
claude-check  # Shows: "⚠️ Very large context (125,432 tokens)"

# 4. If too large, filter more
file_collector --add-ignore "*.test.js" "*.spec.js" --max-size 0.03
claude-check  # Shows: "⚡ Large context (67,890 tokens)"

# 5. Compare changes over time
# Work on feature...
file_collector -o after_refactor.md
file_collector --diff .FILE_STATS/*_FILE_STATS.md .FILE_STATS/after_refactor.md
```

#### Token-Aware Best Practices

1. **Start Small**: Begin with structure only, check tokens
2. **Gradually Expand**: Add detail based on available token budget
3. **Use Filters**: Exclude test files, large data files, generated code
4. **Monitor Size**: Always check token count before sharing with Claude
5. **Split Large Contexts**: Better to have multiple focused conversations

Don't forget to add to `.gitignore`:
```gitignore
# Claude Code context files
.FILE_STATS/
```

### Quick Start for Claude Code

1. **Install in your WSL environment:**
   ```bash
   git clone https://github.com/Stiander/filecollector.git
   cd filecollector && bash install_file_collector.sh
   source ~/.bashrc
   ```

2. **Generate context for Claude:**
   ```bash
   # Navigate to your project
   cd /path/to/your/project
   
   # Quick overview (structure only)
   file_collector
   
   # Check token count
   grep "Estimated tokens:" .FILE_STATS/$(ls -t .FILE_STATS/ | head -1)
   
   # If tokens are reasonable, share with Claude
   # If too many tokens, filter more:
   file_collector --max-depth 3 --add-ignore "test" "spec"
   ```

3. **Progressive Loading Based on Tokens:**
   ```bash
   # Start small (~5-20K tokens)
   file_collector --max-depth 3
   
   # Medium detail (~20-50K tokens)
   file_collector --max-depth 5
   
   # Include code for specific area (~50-150K tokens)
   cd src/components
   file_collector --include-file-content --max-size 0.05
   ```

### Best Practices for Claude Code

1. **Progressive Loading Strategy:**
   ```bash
   # Start: Structure only (5-20K tokens)
   file_collector --max-depth 3
   
   # Expand: More detail (20-50K tokens)  
   file_collector --max-depth 5
   
   # Focus: Specific area with code (50-150K tokens)
   cd src/features/auth
   file_collector --include-file-content --max-size 0.05
   ```

2. **Token Management:**
   - Always check token count before sharing with Claude
   - Start conversations with structure only
   - Add code content only when needed
   - Keep total context under 150K tokens

3. **Effective Filtering:**
   ```bash
   # Exclude test files for cleaner context
   file_collector --add-ignore "*.test.js" "*.spec.js" "__tests__/"
   
   # Focus on source code only
   file_collector --add-ignore "docs/" "examples/" "scripts/"
   
   # Exclude large generated files
   file_collector --add-ignore "*.min.js" "*.bundle.js" "dist/"
   ```

4. **Snapshot Management:**
   ```bash
   # Clean up old snapshots periodically
   ls -lt .FILE_STATS/ | tail -n +11 | awk '{print ".FILE_STATS/" $9}' | xargs rm -f
   
   # Keep important snapshots with descriptive names
   file_collector -o project_v1.0_release.md
   file_collector -o before_major_refactor.md
   ```

### Recommended Workflow

1. **Initial Setup** (one time):
   ```bash
   # Add to .gitignore
   echo ".FILE_STATS/" >> .gitignore
   
   # Add helpful function to ~/.bashrc
   echo 'claude_snapshot() {
     local name="${1:-snapshot}"
     file_collector -o "${name}.md"
     echo "Snapshot saved: .FILE_STATS/${name}.md"
     claude-check
   }' >> ~/.bashrc
   source ~/.bashrc
   ```

2. **Daily Workflow**:
   ```bash
   # Morning: Check project state
   file_collector
   claude-check  # See token count
   
   # Before feature work
   claude_snapshot before_feature
   
   # After feature work
   claude_snapshot after_feature
   
   # See what changed
   file_collector --diff .FILE_STATS/before_feature.md .FILE_STATS/after_feature.md
   ```

3. **Sharing with Claude**:
   ```bash
   # Check tokens first
   claude-check
   
   # If under 50K tokens: share whole file
   # If 50-100K tokens: share specific sections
   # If over 100K tokens: filter more or use subdirectories
   ```

### Integration Tips

- **For React/Next.js projects**: Focus on component structure
  ```bash
  file_collector --max-depth 3 --add-ignore "*.test.js" "*.spec.js" ".next/"
  ```

- **For Python projects**: Include docstrings but exclude cache
  ```bash
  file_collector --add-ignore "__pycache__" "*.pyc" ".pytest_cache/"
  ```

- **For full-stack projects**: Analyze separately
  ```bash
  # Frontend context
  cd frontend && file_collector -o frontend.md
  
  # Backend context  
  cd ../backend && file_collector -o backend.md
  
  # Combined overview
  cd .. && file_collector --max-depth 3 -o overview.md
  ```

- **For microservices**: Create per-service contexts
  ```bash
  for service in services/*; do
    cd "$service"
    file_collector -o "$(basename $service).md"
    cd ..
  done
  ```

## Supported Languages

The script can analyze functions and classes in:

- **Python** (.py) - Functions, async functions, classes
- **JavaScript** (.js, .mjs, .cjs) - Functions, arrow functions, classes
- **TypeScript** (.ts, .tsx) - Same as JS with type support
- **React** (.jsx, .tsx) - Component detection
- **Java** (.java) - Methods, classes, interfaces
- **C/C++** (.c, .cpp, .h, .hpp) - Functions, classes, structs
- **Go** (.go) - Functions, structs
- **Rust** (.rs) - Functions, structs, traits, enums
- **Ruby** (.rb) - Methods, classes
- **PHP** (.php) - Functions, classes
- **Swift** (.swift) - Functions, classes, structs
- **Kotlin** (.kt) - Functions, classes, interfaces
- **Vue** (.vue) - Methods, components
- **Svelte** (.svelte) - Functions, components

## Default Ignore Patterns

The script automatically ignores:

### Node.js/JavaScript
- `node_modules/`, `.next/`, `build/`, `dist/`
- `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`
- `*.min.js`, `*.min.css`, `*.map`

### Python
- `__pycache__/`, `*.pyc`, `*.pyo`
- `venv/`, `.env/`, `.venv/`
- `.pytest_cache/`, `.tox/`
- `*.egg-info/`, `*.egg`

### Version Control
- `.git/`, `.svn/`, `.hg/`

### IDEs
- `.vscode/`, `.idea/`
- `*.swp`, `*.swo`

### File Collector Specific
- `.FILE_STATS/` - Output directory
- `*_FILE_STATS.md` - Generated files

### Others
- `.DS_Store`, `Thumbs.db`
- `.env`, `.env.*`
- Build artifacts and caches

## Advanced Features

### Custom Ignore Patterns File

Create `~/.config/file_collector/custom_ignore.txt`:

```
# Project-specific ignores
my_temp_folder/
*.backup
private_*
secrets/
large_data_files/
```

Use it:
```bash
file_collector --add-ignore $(cat ~/.config/file_collector/custom_ignore.txt | grep -v '^#' | tr '\n' ' ')
```

### Tracking Project Evolution

```bash
# Create snapshot before major changes
file_collector -o before_refactor.md

# After changes
file_collector -o after_refactor.md

# See what changed
file_collector --diff .FILE_STATS/before_refactor.md .FILE_STATS/after_refactor.md

# Create weekly snapshots
crontab -e
# Add: 0 9 * * 1 cd /path/to/project && file_collector -o weekly_$(date +\%Y\%m\%d).md
```

### Integration with CI/CD

```yaml
# GitHub Actions example
- name: Generate Project Documentation
  run: |
    python3 file_collector.py -o project_structure.md
    
- name: Upload Documentation
  uses: actions/upload-artifact@v2
  with:
    name: project-structure
    path: .FILE_STATS/project_structure.md
```

### Git Pre-commit Hook

Create `.git/hooks/pre-commit`:

```bash
#!/bin/bash
# Update project structure documentation
file_collector -o project_structure_latest.md

# Optionally check if structure changed significantly
if [ -f .FILE_STATS/project_structure_latest.md ]; then
    echo "Project structure updated in .FILE_STATS/"
fi
```

### Automated Context Preparation

```bash
# Function to prepare context for specific work
prep_context() {
    local area="${1:-general}"
    local max_tokens="${2:-50000}"
    
    echo "Preparing context for: $area (max ~$max_tokens tokens)"
    
    case $area in
        "frontend")
            cd frontend && file_collector --max-depth 4
            ;;
        "backend")
            cd backend && file_collector --max-depth 4
            ;;
        "api")
            cd src/api && file_collector --include-file-content --max-size 0.05
            ;;
        *)
            file_collector --max-depth 3
            ;;
    esac
    
    claude-check
}

# Usage
prep_context frontend
prep_context api 100000
```

## Troubleshooting

### Common Issues

1. **"file_collector: command not found"**
   - Check if `~/bin` is in your PATH: `echo $PATH`
   - Reload your shell config: `source ~/.bashrc`

2. **"Permission denied"**
   - Make script executable: `chmod +x ~/bin/file_collector`

3. **No output files appearing**
   - Check `.FILE_STATS/` directory: `ls -la .FILE_STATS/`
   - Directory is created automatically in current working directory
   - Ensure you have write permissions in current directory

4. **Token count seems wrong**
   - Token estimation is approximate (based on word count and characters)
   - Actual tokens may vary by ±20% depending on content
   - Code typically has more tokens per character than prose

5. **Diff not showing expected changes**
   - Ensure both files are FILE_STATS format
   - Check file paths are correct: `ls .FILE_STATS/`
   - Diff only compares structure, not content

6. **Memory issues with large projects**
   - Use `--max-depth` to limit scanning
   - Use `--max-size` to skip large files
   - Process subdirectories separately
   - Disable token counting with `--no-token-count`

7. **".FILE_STATS directory not created"**
   - Ensure you're running from project root
   - Check write permissions: `touch .FILE_STATS/test.txt`
   - Try creating manually: `mkdir .FILE_STATS`

### Performance Tips

- Use default mode (no `--include-file-content`) for quick overviews
- Add `--no-code-analysis` for even faster processing
- Use `--simple` for minimal processing (no tokens, no code analysis)
- Increase `--max-size` carefully on large projects
- Use specific ignore patterns for your project type
- Token counting adds ~10-20% processing time

### Best Practices

1. **Regular Snapshots**: Run weekly to track project evolution
2. **Before Major Changes**: Create snapshot before refactoring
3. **Add to .gitignore**: Always exclude `.FILE_STATS/` from version control
4. **Clean Old Snapshots**: Periodically remove old files from `.FILE_STATS/`
5. **Custom Naming**: Use `-o` for meaningful snapshot names
6. **Check Tokens First**: Always verify token count before sharing with Claude

## Examples

### Web Development Project

```bash
# Next.js project overview
file_collector --describe-only --add-ignore "*.test.js" "*.spec.js" -o nextjs_structure.txt

# React component library
cd src/components
file_collector --max-depth 2 --output-file component_library.txt
```

### Python Project

```bash
# Django project
file_collector --describe-only --add-ignore "migrations/" "*.sqlite3" -o django_structure.txt

# Data science project
file_collector --add-ignore "*.ipynb_checkpoints" "*.csv" "data/" --max-size 0.5
```

### Full Stack Project

```bash
# Analyze frontend and backend separately
cd frontend && file_collector --describe-only -o ../docs/frontend_structure.txt
cd ../backend && file_collector --describe-only -o ../docs/backend_structure.txt
```

### Documentation Generation

```bash
# Generate multiple views
file_collector --simple -o docs/structure_simple.txt
file_collector --describe-only -o docs/structure_with_code.txt
file_collector --max-depth 2 -o docs/structure_overview.txt
```

---

## Contributing

We welcome contributions! Here's how you can help:

1. **Fork the repository**: https://github.com/Stiander/filecollector
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit your changes**: `git commit -m 'Add amazing feature'`
4. **Push to the branch**: `git push origin feature/amazing-feature`
5. **Open a Pull Request**

### Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/filecollector.git
cd filecollector

# Create a virtual environment for testing
python3 -m venv venv
source venv/bin/activate

# Link for testing
ln -s $(pwd)/file_collector.py ~/bin/file_collector-dev
```

### Areas for Contribution

- Add support for more programming languages
- Improve regex patterns for better function/class detection
- Add configuration file support
- Create GUI wrapper
- Add export formats (JSON, YAML, etc.)

## License

MIT License - See [LICENSE](https://github.com/Stiander/filecollector/blob/main/LICENSE) file for details.

---

## Quick Reference Card

```bash
# Installation
git clone https://github.com/Stiander/filecollector.git
cd filecollector && bash install_file_collector.sh

# Basic Commands
file_collector                      # Full collection
file_collector --describe-only      # Structure + code analysis
file_collector --simple             # Structure only

# Claude Code Integration (Progressive Context)
claude-overview                     # Project overview (5-20KB)
claude-component                    # Current directory detail (10-30KB)
claude-focus                        # Code with size limit (30-100KB)
claude-check .claude/overview.txt   # Check context size

# Common Options
--max-depth 3                       # Limit depth
--max-size 0.5                      # Max 0.5 MB files
--output-folder ~/reports           # Custom output location
--output-file custom_name.txt       # Custom filename
--add-ignore "*.log" "temp/"        # Additional ignore patterns
```

---

**Pro Tip**: Create a `.file-collector` config file in your project root with custom settings:

```bash
# .file-collector
--describe-only
--max-depth 5
--output-folder ./docs
--add-ignore "*.log" "temp/"
```

Then run: `file_collector $(cat .file-collector)`

**Claude Code Tip**: Always start with `--describe-only` for initial context, then progressively add detail as needed. See the [Optimizing for Context Windows](#optimizing-for-context-windows) section for a complete strategy.

---


