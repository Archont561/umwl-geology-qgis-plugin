import sys
import zipfile
from pathlib import Path


def main():
    """Packages the plugin into a zip file."""
    print("--- Packaging QGIS Plugin ---")
    project_root = Path(__file__).parent.parent
    plugin_name = sys.argv[1]
    print(plugin_name)
    source_dir = project_root / "src" / plugin_name
    zip_path = project_root / f"{plugin_name}.zip"

    if not source_dir.exists():
        print(f"ERROR: Source directory not found at {source_dir}")
        return

    if zip_path.exists():
        print(f"Removing old zip file: {zip_path}")
        zip_path.unlink()

    print(f"Creating zip file: {zip_path}")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for file in source_dir.rglob("*"):
            # Create a relative path for the file inside the zip
            archive_path = Path(plugin_name) / file.relative_to(source_dir)
            zf.write(file, archive_path)
            print(f"  + Adding {archive_path}")

    print(f"✅ Plugin successfully packaged at: {zip_path}")

if __name__ == "__main__":
    main()