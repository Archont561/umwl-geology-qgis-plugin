from umwl_geology.settings import ASSETS_DIR
from pathlib import Path
from qgis.pyqt.Widgets import QAction
from qgis.pyqt.QtGui import QIcon

class UMWLGeologyPlugin:
    def __init__(self, iface):
        self.iface = iface

    def initGui(self):
        icon = QIcon(ASSETS_DIR / "coat_of_arms.png")
        self.action = QAction(icon, 'Dummy Action', self.iface.mainWindow())
        self.iface.addToolBarIcon(self.action)
        self.action.triggered.connect(self.run)

    def unload(self):
        self.iface.removeToolBarIcon(self.action)
        del self.action

    def run(self):
        self.iface.messageBar().pushMessage('Hello World from Plugin')