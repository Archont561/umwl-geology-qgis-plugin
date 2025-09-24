# Justfile for QGIS Plugin Development
set dotenv-load
set quiet := true

# Default: list all available tasks
_:
    just --list

# Configuration
PORT := env("PORT", "8000")  # Optional, if used for web tools

# Paths
SRC_DIR := "src"
DESIGNER_DIR := "designer"
BUILD_DIR := "build"

# Compile ui/resources/all
[group('chore')]
compile arg='all':
    if [[ -z {{ arg }} ]]; then \
        echo "Usage: just compile <ui|resources|all>"; \
        exit 1; \
    fi

    if [[ {{ arg }} == "ui" || {{ arg }} == "all" ]]; then \
        for file in {{ DESIGNER_DIR }}/ui/*.ui; do \
            base=$$(basename $$file .ui); \
            echo "Compiling $$file -> {{ SRC_DIR }}/ui/ui_$$base.py"; \
            pyuic5 "$$file" -o "{{ SRC_DIR }}/ui/ui_$$base.py"; \
        done
    fi

    if [[ {{ arg }} == "resources" || {{ arg }} == "all" ]]; then \
        for file in {{ DESIGNER_DIR }}/resources/*.qrc; do \
            base=$$(basename $$file .qrc); \
            echo "Compiling $$file -> {{ SRC_DIR }}/resources/$$base_rc.py"; \
            pyrcc5 "$$file" -o "{{ SRC_DIR }}/resources/$$base_rc.py"; \
        done
    fi

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
