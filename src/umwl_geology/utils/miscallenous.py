from pathlib import Path
from contextlib import contextmanager
from qgis.core import QgsApplication


def get_qgis_prefix_path() -> str:
    """
    Get the QGIS installation prefix path from the installed qgis package.
    Works with pixi, conda, and other local installations.
    """
    import qgis

    # Get qgis installation path
    qgis_path = Path(qgis.__file__).parent

    # For pixi/conda: .pixi/envs/dev/Library/python/qgis/__init__.py
    # Prefix path is:  .pixi/envs/dev/Library/

    # Navigate up from qgis package to Library directory
    if "Library" in qgis_path.parts:
        # Find the Library directory
        parts = qgis_path.parts
        library_index = parts.index("Library")
        prefix_path = Path(*parts[:library_index + 1])
    else:
        # Fallback: assume parent of 'python' directory
        prefix_path = qgis_path.parent.parent

    return str(prefix_path)


@contextmanager
def QGISEnvironment():
    QgsApplication.setPrefixPath(get_qgis_prefix_path(), True)
    qgs = QgsApplication([], False)
    qgs.initQgis()

    try:
        yield qgs
    finally:
        qgs.exitQgis()