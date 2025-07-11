#!/bin/bash

# File Collector Installation Script
# ==================================
# This script installs the file_collector.py tool in your WSL environment
# Usage: bash install_file_collector.sh

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

# Download or create the file_collector.py script
SCRIPT_URL="https://raw.githubusercontent.com/your-repo/file_collector.py"
SCRIPT_PATH="$HOME/bin/file_collector"

print_info "Installing file_collector..."

# Since we can't download from a real URL, create a placeholder message
cat << 'EOF' > "$SCRIPT_PATH"
#!/usr/bin/env python3
# PLACEHOLDER: Replace this with the actual file_collector.py content
print("Error: Please replace this file with the actual file_collector.py script")
print("Location: ~/bin/file_collector")
EOF

# Make it executable
chmod +x "$SCRIPT_PATH"

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
    *)
        print_warning "Unknown shell: $SHELL_NAME. You'll need to add ~/bin to PATH manually."
        ;;
esac

# Add ~/bin to PATH if not already there
if [ -n "$SHELL_RC" ]; then
    if ! grep -q 'export PATH="$HOME/bin:$PATH"' "$SHELL_RC"; then
        print_info "Adding ~/bin to PATH in $SHELL_RC..."
        echo '' >> "$SHELL_RC"
        echo '# Added by file_collector installer' >> "$SHELL_RC"
        echo 'export PATH="$HOME/bin:$PATH"' >> "$SHELL_RC"
        print_info "PATH updated. Run 'source $SHELL_RC' to apply changes."
    else
        print_info "~/bin is already in PATH"
    fi
fi

# Create helpful aliases
if [ -n "$SHELL_RC" ]; then
    print_info "Adding helpful aliases..."
    
    # Check if aliases already exist
    if ! grep -q "alias fcollect=" "$SHELL_RC"; then
        cat >> "$SHELL_RC" << 'EOF'

# File Collector aliases
alias fcollect='file_collector'
alias fcollect-quick='file_collector --describe-only --max-depth 3'
alias fcollect-full='file_collector -o full_project_$(date +%Y%m%d_%H%M%S).txt'

# Function to collect and save to dated file
collect_project() {
    local project_name="${1:-project}"
    local timestamp=$(date +%Y%m%d_%H%M%S)
    local output_file="${project_name}_${timestamp}.txt"
    file_collector --describe-only -o "$output_file"
    echo "Project structure saved to: $output_file"
}
EOF
    fi
fi

# Create a sample configuration file
CONFIG_DIR="$HOME/.config/file_collector"
mkdir -p "$CONFIG_DIR"

cat > "$CONFIG_DIR/custom_ignore.txt" << 'EOF'
# Custom ignore patterns (one per line)
# Add your own patterns here
# Example:
# *.backup
# temp_*
# .cache/
EOF

# Installation complete message
echo
print_info "Installation complete!"
echo
echo "IMPORTANT: You need to replace the placeholder script with the actual file_collector.py"
echo "1. Copy the file_collector.py content"
echo "2. Edit the installed file: nano ~/bin/file_collector"
echo "3. Replace all content with the actual script"
echo "4. Save and exit (Ctrl+X, then Y, then Enter)"
echo
echo "After that, you can use:"
echo "  file_collector                    # Run the tool"
echo "  fcollect                         # Short alias"
echo "  fcollect-quick                   # Quick overview (depth 3, no contents)"
echo "  collect_project myapp            # Save timestamped snapshot"
echo
echo "To apply PATH changes now, run:"
echo "  source $SHELL_RC"
echo
print_info "For Windows integration:"
echo "  - Access the script from Windows at: \\\\wsl$\\Ubuntu\\home\\$USER\\bin\\file_collector"
echo "  - Edit with Cursor IDE: code ~/bin/file_collector"

# Create a quick test
if [ -f "$SCRIPT_PATH" ]; then
    print_info "Testing installation..."
    export PATH="$HOME/bin:$PATH"
    if command -v file_collector &> /dev/null; then
        print_info "file_collector is accessible from PATH ✓"
    else
        print_warning "file_collector not found in PATH. You may need to restart your shell."
    fi
fi