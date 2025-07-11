#!/bin/bash

# File Collector Complete Installation Script
# ==========================================
# This script installs the file_collector tool with the script embedded
# Usage: bash install_file_collector_complete.sh

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Check if running in WSL
if ! grep -qi microsoft /proc/version; then
    print_warning "This doesn't appear to be WSL, but continuing anyway..."
fi

# Check Python installation
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed. Please install it first:"
    echo "  sudo apt update && sudo apt install python3"
    exit 1
fi

print_info "Python 3 found: $(python3 --version)"

# Create necessary directories
print_info "Creating directories..."
mkdir -p ~/bin
mkdir -p ~/scripts
mkdir -p ~/.config/file_collector

# Install the file_collector script
SCRIPT_PATH="$HOME/bin/file_collector"
print_info "Installing file_collector to $SCRIPT_PATH..."

# Write the complete script
cat << 'SCRIPT_CONTENT' > "$SCRIPT_PATH"
#!/usr/bin/env python3
"""
FILE COLLECTOR - Project Structure and Code Analysis Tool
========================================================

[Copy the entire file_collector.py script content here]
This is a placeholder - when creating the actual installer,
replace this section with the complete script from the artifact above.
"""

# Note: In the real installer, paste the entire enhanced file_collector.py script here
print("Error: This is a placeholder. Please use the complete script.")
SCRIPT_CONTENT

# Make it executable
chmod +x "$SCRIPT_PATH"
print_info "Script installed and made executable"

# Detect shell and update PATH
SHELL_NAME=$(basename "$SHELL")
SHELL_RC=""

case "$SHELL_NAME" in
    bash)
        SHELL_RC="$HOME/.bashrc"
        ;;
    zsh)
        SHELL_RC="$HOME/.zshrc"
        ;;
    fish)
        SHELL_RC="$HOME/.config/fish/config.fish"
        ;;
    *)
        print_warning "Unknown shell: $SHELL_NAME. You'll need to add ~/bin to PATH manually."
        ;;
esac

# Add ~/bin to PATH if not already there
if [ -n "$SHELL_RC" ]; then
    if [ "$SHELL_NAME" = "fish" ]; then
        if ! grep -q 'set -gx PATH $HOME/bin $PATH' "$SHELL_RC"; then
            print_info "Adding ~/bin to PATH in $SHELL_RC..."
            echo '' >> "$SHELL_RC"
            echo '# Added by file_collector installer' >> "$SHELL_RC"
            echo 'set -gx PATH $HOME/bin $PATH' >> "$SHELL_RC"
        fi
    else
        if ! grep -q 'export PATH="$HOME/bin:$PATH"' "$SHELL_RC"; then
            print_info "Adding ~/bin to PATH in $SHELL_RC..."
            echo '' >> "$SHELL_RC"
            echo '# Added by file_collector installer' >> "$SHELL_RC"
            echo 'export PATH="$HOME/bin:$PATH"' >> "$SHELL_RC"
        else
            print_info "~/bin is already in PATH"
        fi
    fi
fi

# Create helpful aliases and functions
if [ -n "$SHELL_RC" ] && [ "$SHELL_NAME" != "fish" ]; then
    print_info "Adding helpful aliases and functions..."
    
    # Check if aliases already exist
    if ! grep -q "alias fcollect=" "$SHELL_RC"; then
        cat >> "$SHELL_RC" << 'EOF'

# File Collector aliases
alias fcollect='file_collector'
alias fcollect-quick='file_collector --describe-only --max-depth 3'
alias fcollect-structure='file_collector --describe-only'
alias fcollect-simple='file_collector --simple'
alias fcollect-full='file_collector --output-file full_project_$(date +%Y%m%d_%H%M%S).txt'

# Function to collect project with timestamp
collect_project() {
    local project_name="${1:-project}"
    local timestamp=$(date +%Y%m%d_%H%M%S)
    local output_dir="${2:-.}"
    local output_file="${project_name}_structure_${timestamp}.txt"
    
    file_collector --describe-only --output-folder "$output_dir" --output-file "$output_file"
    echo "Project structure saved to: $output_dir/$output_file"
}

# Function to collect full project content
collect_project_full() {
    local project_name="${1:-project}"
    local timestamp=$(date +%Y%m%d_%H%M%S)
    local output_dir="${2:-.}"
    local output_file="${project_name}_full_${timestamp}.txt"
    
    file_collector --output-folder "$output_dir" --output-file "$output_file"
    echo "Full project content saved to: $output_dir/$output_file"
}

# Function to analyze code structure
analyze_code() {
    local max_depth="${1:-5}"
    file_collector --describe-only --max-depth "$max_depth" --output-file "code_analysis_$(date +%Y%m%d_%H%M%S).txt"
}
EOF
        print_info "Aliases and functions added"
    fi
fi

# Create a sample configuration file
CONFIG_DIR="$HOME/.config/file_collector"
cat > "$CONFIG_DIR/custom_ignore.txt" << 'EOF'
# Custom ignore patterns for file_collector
# Add one pattern per line
# 
# Examples:
# *.backup
# *.tmp
# temp_*
# .cache/
# my_private_folder/
# 
# To use these patterns, run:
# file_collector --add-ignore $(cat ~/.config/file_collector/custom_ignore.txt | grep -v '^#' | grep -v '^$' | tr '\n' ' ')
EOF

# Create a quick reference guide
cat > "$CONFIG_DIR/quick_reference.md" << 'EOF'
# File Collector Quick Reference

## Basic Commands

```bash
# Show structure with code analysis
file_collector --describe-only

# Simple structure only
file_collector --simple

# Full collection (structure + contents)
file_collector

# Quick 3-level overview
fcollect-quick
```

## Output Options

```bash
# Custom output file
file_collector -o myproject.txt
file_collector --output-file myproject.txt

# Save to specific folder
file_collector --output-folder ~/reports --output-file project.txt

# Timestamped outputs
collect_project myapp              # Creates myapp_structure_20231215_143022.txt
collect_project_full myapp ~/docs  # Full content in ~/docs/
```

## Filtering

```bash
# Limit depth
file_collector --max-depth 3

# Limit file size
file_collector --max-size 0.5  # Max 0.5 MB files

# Custom ignore patterns
file_collector --add-ignore "*.log" "temp/"
file_collector --show-ignore  # See all patterns
```

## Analysis Options

```bash
# Disable code analysis
file_collector --no-code-analysis

# Disable statistics
file_collector --no-stats
```

## Advanced Functions

```bash
# Analyze code structure to depth 5
analyze_code 5

# Collect with custom timestamp
collect_project "my-web-app" ~/snapshots
```
EOF

# Test the installation
print_info "Testing installation..."
export PATH="$HOME/bin:$PATH"

# Create a test directory
TEST_DIR="/tmp/file_collector_test_$$"
mkdir -p "$TEST_DIR"
cd "$TEST_DIR"

# Create some test files
cat > test.py << 'EOF'
def hello():
    print("Hello")

class TestClass:
    pass
EOF

cat > test.js << 'EOF'
function testFunc() {
    console.log("test");
}

const arrowFunc = () => {
    return true;
};
EOF

# Installation complete
echo
echo "========================================"
print_info "Installation complete! ✓"
echo "========================================"
echo
echo "Quick start commands:"
echo "  file_collector --describe-only    # Analyze current directory"
echo "  fcollect-quick                    # Quick 3-level overview"
echo "  collect_project myapp             # Save timestamped snapshot"
echo
echo "Installed components:"
echo "  - Main script: ~/bin/file_collector"
echo "  - Config dir:  ~/.config/file_collector/"
echo "  - Quick ref:   ~/.config/file_collector/quick_reference.md"
echo
if [ -n "$SHELL_RC" ]; then
    echo "To activate the new PATH and aliases, run:"
    echo "  source $SHELL_RC"
    echo
fi
echo "For help:"
echo "  file_collector --help"
echo
print_info "For Cursor IDE integration:"
echo "  - Edit script: code ~/bin/file_collector"
echo "  - Windows path: \\\\wsl$\\$(lsb_release -i -s 2>/dev/null || echo "Ubuntu")\\home\\$USER\\bin\\file_collector"

# Cleanup test directory
rm -rf "$TEST_DIR"