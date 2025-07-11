# File Collector - Project Structure and Code Analysis Tool

A powerful Python script that creates comprehensive snapshots of your project structure, analyzes source code to extract functions and classes, and optionally includes full file contents. Perfect for documentation, code reviews, and sharing project context with AI assistants like Claude Code.

## Table of Contents

- [Features](#features)
- [What It Does](#what-it-does)
- [Installation Requirements](#installation-requirements)
- [Installation](#installation)
  - [Quick Install (WSL/Linux)](#quick-install-wsllinux)
  - [Manual Installation](#manual-installation)
  - [Windows Integration](#windows-integration)
- [Usage](#usage)
  - [Basic Commands](#basic-commands)
  - [Output Options](#output-options)
  - [Filtering Options](#filtering-options)
  - [Code Analysis](#code-analysis)
- [Using with Claude Code](#using-with-claude-code)
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

## Installation Requirements

- **Python 3.6+** - The script is written in Python
- **Operating System** - Works on Linux, WSL, macOS, and Windows
- **No external dependencies** - Uses only Python standard library

### Check Requirements

```bash
# Check Python version
python3 --version

# If Python is not installed:
# Ubuntu/Debian/WSL:
sudo apt update && sudo apt install python3

# macOS:
brew install python3

# Windows:
# Download from https://www.python.org/downloads/
```

## Installation

### Quick Install (WSL/Linux)

1. **Download the installer and run it:**

```bash
# Download and run the installer
curl -o install_file_collector.sh https://raw.githubusercontent.com/YOUR_REPO/install_file_collector.sh
bash install_file_collector.sh
```

2. **Or use the one-liner:**

```bash
# Create bin directory and download script
mkdir -p ~/bin && \
curl -o ~/bin/file_collector https://raw.githubusercontent.com/YOUR_REPO/file_collector.py && \
chmod +x ~/bin/file_collector && \
echo 'export PATH="$HOME/bin:$PATH"' >> ~/.bashrc && \
source ~/.bashrc
```

### Manual Installation

1. **Create a directory for the script:**

```bash
mkdir -p ~/bin
```

2. **Create the script file:**

```bash
nano ~/bin/file_collector
```

3. **Copy the entire script content into the file**

4. **Make it executable:**

```bash
chmod +x ~/bin/file_collector
```

5. **Add to PATH (choose your shell):**

```bash
# For Bash
echo 'export PATH="$HOME/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# For Zsh
echo 'export PATH="$HOME/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# For Fish
echo 'set -gx PATH $HOME/bin $PATH' >> ~/.config/fish/config.fish
```

### Windows Integration

If you're using Windows with WSL:

1. **Access from Windows Explorer:**
   ```
   \\wsl$\Ubuntu\home\YOUR_USERNAME\bin\file_collector
   ```

2. **Edit with Cursor IDE:**
   ```bash
   # From WSL terminal
   code ~/bin/file_collector
   ```

3. **Create Windows shortcut:**
   ```batch
   wsl.exe -e bash -c "cd /mnt/c/YourProject && file_collector --describe-only"
   ```

## Usage

### Basic Commands

```bash
# Analyze current directory (structure + code analysis + contents)
file_collector

# Structure and code analysis only (no file contents)
file_collector --describe-only

# Simple structure only (no code analysis, no contents)
file_collector --simple

# Show help
file_collector --help
```

### Output Options

```bash
# Specify output filename
file_collector -o project_snapshot.txt
file_collector --output-file project_snapshot.txt

# Save to specific folder
file_collector --output-folder ~/reports
file_collector --output-folder /mnt/c/Users/YourName/Documents

# Combine both options
file_collector --output-folder ~/snapshots --output-file myproject_v1.txt

# Create timestamped files
file_collector --output-file "snapshot_$(date +%Y%m%d_%H%M%S).txt"
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
file_collector --describe-only --no-code-analysis

# Disable statistics
file_collector --no-stats
```

## Using with Claude Code

File Collector is particularly useful for sharing project context with Claude Code or other AI assistants.

### Best Practices for Claude Code

1. **Quick Project Overview:**
   ```bash
   # Get a quick structural overview
   file_collector --describe-only --max-depth 3 -o project_overview.txt
   ```

2. **Focused Component Analysis:**
   ```bash
   # Analyze specific directory
   cd src/components
   file_collector --describe-only -o components_structure.txt
   ```

3. **Full Context for Debugging:**
   ```bash
   # Include relevant code for debugging
   file_collector --max-size 0.1 -o debug_context.txt
   ```

4. **Share with Claude Code:**
   - Run the command in your project directory
   - Copy the output file path
   - In Claude Code, reference the file or paste relevant sections

### Recommended Aliases for Claude Code

Add these to your `~/.bashrc` or `~/.zshrc`:

```bash
# Quick snapshot for AI context
alias ai-snapshot='file_collector --describe-only --max-depth 4 -o ai_context_$(date +%Y%m%d_%H%M%S).txt'

# Component documentation
alias doc-components='file_collector --describe-only --output-folder ./docs --output-file components_structure.txt'

# Full project archive
alias archive-project='file_collector --output-folder ~/project-archives --output-file "$(basename $(pwd))_$(date +%Y%m%d).txt"'
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
```

Use it:
```bash
file_collector --add-ignore $(cat ~/.config/file_collector/custom_ignore.txt | grep -v '^#' | tr '\n' ' ')
```

### Integration with CI/CD

```yaml
# GitHub Actions example
- name: Generate Project Documentation
  run: |
    python3 file_collector.py --describe-only --output-folder ./docs --output-file project_structure.md
    
- name: Upload Documentation
  uses: actions/upload-artifact@v2
  with:
    name: project-docs
    path: docs/project_structure.md
```

### Git Pre-commit Hook

Create `.git/hooks/pre-commit`:

```bash
#!/bin/bash
# Update project structure documentation
file_collector --describe-only --output-file docs/PROJECT_STRUCTURE.md
git add docs/PROJECT_STRUCTURE.md
```

## Troubleshooting

### Common Issues

1. **"file_collector: command not found"**
   - Check if `~/bin` is in your PATH: `echo $PATH`
   - Reload your shell config: `source ~/.bashrc`

2. **"Permission denied"**
   - Make script executable: `chmod +x ~/bin/file_collector`

3. **Unicode errors**
   - The script handles UTF-8 by default
   - For other encodings, modify the script's encoding parameter

4. **Memory issues with large projects**
   - Use `--max-depth` to limit scanning
   - Use `--max-size` to skip large files
   - Process subdirectories separately

### Performance Tips

- Use `--describe-only` for quick overviews
- Add `--no-code-analysis` for faster processing
- Increase `--max-size` carefully on large projects
- Use specific ignore patterns for your project type

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

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## License

MIT License - feel free to use this tool in your projects!

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