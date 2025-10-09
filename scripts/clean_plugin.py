import sys
import shutil
from pathlib import Path


def main():
    """Cleans up the project directory."""
    print("--- Cleaning Project ---")
    plugin_name = sys.argv[1]
    project_root = Path(__file__).parent.parent
    src_dir = project_root / "src"
    deleted_count = 0

    # Remove the packaged zip file
    zip_file = project_root / f"{plugin_name}.zip"
    if zip_file.exists():
        zip_file.unlink()
        print(f"- Deleted {zip_file}")
        deleted_count += 1

    # Remove __pycache__ directories
    for path in src_dir.rglob("__pycache__"):
        if path.is_dir():
            shutil.rmtree(path)
            print(f"- Deleted {path}")
            deleted_count += 1

    # Remove .pytest_cache
    pytest_cache = src_dir / ".pytest_cache"
    if pytest_cache.exists():
        shutil.rmtree(pytest_cache)
        print(f"- Deleted {pytest_cache}")
        deleted_count += 1

    # Remove .coverage file
    coverage_file = src_dir / ".coverage"
    if coverage_file.exists():
        coverage_file.unlink()
        print(f"- Deleted {coverage_file}")
        deleted_count += 1

    if deleted_count == 0:
        print("No files to clean.")
    else:
        print(f"✅ Cleaned {deleted_count} items.")


if __name__ == "__main__":
    main()