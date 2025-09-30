# Justfile for QGIS Plugin Development
set dotenv-load
set quiet := true

# Default: list all available tasks
_:
    just --list

# Configuration
PORT := env("PORT", "8000")  # Optional, if used for web tools

# Paths
export SRC_DIR := "src"
export DESIGNER_DIR := "designer"
export BUILD_DIR := "build"

# Compile .ui file to .py
[group('chore')]
compile_ui src dest:
    echo "Compiling {{ src }} -> {{ dest }}"; \
    python -m PyQt5.uic.pyuic {{ src }} -o {{ dest }}

# Compile .qrc file to .py
[group('chore')]
compile_rc src dest:
    echo "Compiling {{ src }} -> {{ dest }}"; \
    python -m PyQt5.pyrcc_main {{ src }} -o {{ dest }}

# Build plugin
[group('chore')]
build:
    just compile all
    echo "UI and resources compiled."
    pb_tool zip
    echo "✅ Build complete"

# Clean compiled and temporary files
[group('chore')]
clean:
    echo "🧹 Cleaning unnessesary files..."
    find . -type f -name "*.pyc" -delete
    find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    find . -type f -name "*.db" -delete
    find . -type f -name "*.ini" -delete
    rm -rf {{ BUILD_DIR }}
    echo "✅ Clean complete."

# Run coverage test with coverage and pytest
[group('clean-code')]
test:
    coverage run -m pytest && coverage report --fail-under=80

# Format with black
[group('clean-code')]
format path='./src':
    black {{ path }}

# Lint and code analysis with flake8
[group('clean-code')]
lint_and_analyze path='./src':
    flake8 {{ path }} --count --show-source --statistics

# Check typing with mypy
[group('clean-code')]
check_type path='./src':
    mypy {{ path }}
