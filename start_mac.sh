#!/usr/bin/env bash
# ============================================================================
#   Python for AI — macOS Starter Script
#   Just run this file and the course will start automatically!
#
#   Usage:
#     chmod +x start_mac.sh
#     ./start_mac.sh
#
#   Or right-click the file > Open With > Terminal
# ============================================================================

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color
BOLD='\033[1m'

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$SCRIPT_DIR/.venv"
REQUIREMENTS="$SCRIPT_DIR/requirements.txt"
RUNNER="$SCRIPT_DIR/course_runner.py"

# ── Banner ──────────────────────────────────────────────────────────────────
echo ""
echo -e "${PURPLE}${BOLD}"
echo "  ╔═══════════════════════════════════════════════╗"
echo "  ║                                               ║"
echo "  ║     🐍  Python for AI — Course Launcher  🤖   ║"
echo "  ║                                               ║"
echo "  ╚═══════════════════════════════════════════════╝"
echo -e "${NC}"

# ── Step 1: Check Python ────────────────────────────────────────────────────
echo -e "${CYAN}[1/4]${NC} Checking for Python..."

PYTHON_CMD=""

# Try python3 first (macOS convention)
if command -v python3 &>/dev/null; then
    PYTHON_CMD="python3"
elif command -v python &>/dev/null; then
    PY_VER=$(python --version 2>&1 | awk '{print $2}' | cut -d'.' -f1)
    if [ "$PY_VER" = "3" ]; then
        PYTHON_CMD="python"
    fi
fi

if [ -z "$PYTHON_CMD" ]; then
    echo ""
    echo -e "${RED}${BOLD}  ❌ Python 3 is not installed!${NC}"
    echo ""
    echo -e "  Please install Python 3 using one of these methods:"
    echo ""
    echo -e "  ${YELLOW}Option A — Official installer (easiest):${NC}"
    echo -e "    1. Go to ${BOLD}https://www.python.org/downloads/${NC}"
    echo -e "    2. Download the macOS installer (.pkg)"
    echo -e "    3. Run the installer"
    echo ""
    echo -e "  ${YELLOW}Option B — Homebrew (if you use the terminal):${NC}"
    if ! command -v brew &>/dev/null; then
        echo -e "    First install Homebrew:"
        echo -e "    ${BOLD}/bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\"${NC}"
        echo ""
    fi
    echo -e "    ${BOLD}brew install python3${NC}"
    echo ""
    echo -e "  After installing, run this script again."
    echo ""
    exit 1
fi

PY_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
echo -e "  ${GREEN}✅ Found $PYTHON_CMD ($PY_VERSION)${NC}"

# Check minimum version (3.8+)
PY_MAJOR=$($PYTHON_CMD -c "import sys; print(sys.version_info.major)")
PY_MINOR=$($PYTHON_CMD -c "import sys; print(sys.version_info.minor)")

if [ "$PY_MAJOR" -lt 3 ] || ([ "$PY_MAJOR" -eq 3 ] && [ "$PY_MINOR" -lt 8 ]); then
    echo -e "${RED}  ⚠️  Python 3.8 or higher is required. You have $PY_VERSION.${NC}"
    echo -e "  Please update Python and try again."
    exit 1
fi

# ── Step 2: Set up virtual environment ──────────────────────────────────────
echo -e "${CYAN}[2/4]${NC} Setting up virtual environment..."

if [ ! -d "$VENV_DIR" ]; then
    echo -e "  Creating virtual environment..."
    $PYTHON_CMD -m venv --system-site-packages "$VENV_DIR"
    echo -e "  ${GREEN}✅ Virtual environment created${NC}"
else
    echo -e "  ${GREEN}✅ Virtual environment exists${NC}"
fi

# Activate venv
source "$VENV_DIR/bin/activate"

# ── Step 3: Install dependencies ────────────────────────────────────────────
echo -e "${CYAN}[3/4]${NC} Installing dependencies..."

# Upgrade pip quietly
pip install --upgrade pip -q 2>/dev/null

if [ -f "$REQUIREMENTS" ]; then
    pip install -r "$REQUIREMENTS" -q 2>/dev/null
    echo -e "  ${GREEN}✅ Dependencies installed${NC}"
else
    pip install rich -q 2>/dev/null
    echo -e "  ${GREEN}✅ Core dependencies installed${NC}"
fi

# ── Step 4: Launch! ─────────────────────────────────────────────────────────
echo -e "${CYAN}[4/4]${NC} Launching Python for AI Course..."
echo ""
echo -e "${GREEN}${BOLD}  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Run the course
python "$RUNNER"

# Deactivate venv on exit
deactivate 2>/dev/null || true
