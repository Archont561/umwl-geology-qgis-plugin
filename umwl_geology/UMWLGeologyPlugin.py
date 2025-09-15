from umwl_geology.settings import ASSETS_DIR
from pathlib import Path
from qgis.pyqt.Widgets import QAction
from qgis.pyqt.QtGui import QIcon
from umwl_geology.processing_provider.provider import Provider

class UMWLGeologyPlugin:
    def __init__(self, iface):
        self.iface = iface
        self.provider = None

    def initProcessing(self):
        self.provider = Provider()
        QgsApplication.processingRegistry().addProvider(self.provider)

    def initGui(self):
        self.initProcessing()
        icon = QIcon(ASSETS_DIR / "coat_of_arms.png")
        self.action = QAction(icon, 'Dummy Action', self.iface.mainWindow())
        self.iface.addToolBarIcon(self.action)
        self.action.triggered.connect(self.run)

    def unload(self):
        QgsApplication.processingRegistry().removeProvider(self.provider)
        self.iface.removeToolBarIcon(self.action)
        del self.action

    def run(self):
        self.iface.messageBar().pushMessage('Hello World from Plugin')