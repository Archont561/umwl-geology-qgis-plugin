from typing import Callable

from qgis.gui import QgisInterface
from qgis.utils import iface

__all__ = [
    "iface",
    "run_in_project"
]

# noinspection PyTypeChecker,PyArgumentList,PyCallByClass
iface: QgisInterface = iface


def run_in_project(main: Callable[[], None]):
    import os
    from qgis.core import QgsApplication, QgsProject
    from umwl_geology.exceptions import QGISProjectNotFoundError

    qgis_path = os.getenv('QGIS_PATH')
    project_path = os.getenv('PROJECT_PATH')
    if qgis_path is None or project_path is None:
        raise ValueError('QGIS_PATH and PROJECT_PATH environment variables not set')

    QgsApplication.setPrefixPath(qgis_path, True)
    qgs = QgsApplication([], False)
    qgs.initQgis()

    print(project_path)
    if not QgsProject.instance().read(project_path):
        raise QGISProjectNotFoundError('Failed to load qgis project')

    try:
        main()
    except Exception as e:
        print(e)
    finally:
        qgs.exitQgis()