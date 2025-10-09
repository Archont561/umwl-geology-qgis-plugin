import os
import sys
from pathlib import Path


def get_qgis_plugins_path() -> Path:
    """Finds the path to the QGIS plugins directory for the default profile."""
    if sys.platform == "win32":
        qgis_path = Path(os.environ["APPDATA"]) / "QGIS/QGIS3/profiles/default"
    elif sys.platform == "darwin":  # macOS
        qgis_path = Path.home() / "Library/Application Support/QGIS/QGIS3/profiles/default"
    else:  # Linux
        qgis_path = Path.home() / ".local/share/QGIS/QGIS3/profiles/default"

    plugins_path = qgis_path / "python/plugins"
    if not plugins_path.exists():
        raise FileNotFoundError(
            f"QGIS plugins directory not found at: {plugins_path}\n"
            "Please ensure QGIS has been run at least once to create the default profile."
        )
    return plugins_path

def main():
    """Main function to create the symbolic link."""
    print("--- Linking QGIS Plugin for Development ---")
    try:
        plugins_dir = get_qgis_plugins_path()
        plugin_name = sys.argv[1]
        source_dir = Path(__file__).parent.parent / "src" / plugin_name
        link_path = plugins_dir / plugin_name

        if not source_dir.exists():
            print(f"ERROR: Source plugin directory does not exist: {source_dir}")
            sys.exit(1)

        print(f"Source: {source_dir}")
        print(f"Target: {link_path}")

        if link_path.exists() or link_path.is_symlink():
            print(f"Plugin already exists at target. Removing old link/directory...")
            if link_path.is_dir() and not link_path.is_symlink():
                import shutil
                shutil.rmtree(link_path)
            else:
                link_path.unlink()

        try:
            os.symlink(source_dir, link_path, target_is_directory=True)
            print(f"✅ Successfully created symbolic link.")
            print("You can now enable the plugin in QGIS. Changes will be reflected on plugin reload.")
        except OSError as e:
            print(f"\nERROR: Could not create symbolic link: {e}")
            print("On Windows, you may need to run this command in an Administrator terminal.")
            print("On Linux/macOS, you may need to use 'sudo'.")
            sys.exit(1)

    except FileNotFoundError as e:
        print(f"ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()