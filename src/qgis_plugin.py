from pathlib import Path
from qgis.PyQt.QtWidgets import QAction
from qgis.PyQt.QtGui import QIcon
from .processing_provider.provider import Provider
from


class UMWLGeologyPlugin:

    def __init__(self, iface):
        self.plugin_dir = Path(__file__).resolve().parent
        self.assets_dir = self.plugin_dir / "assets"
        self.iface = iface
        self.provider = None
        self.cleanup_callbacks = []
        self.plugin_menu_name = self.tr(u'&UMWL Geology')

    def tr(self, message):
        return QCoreApplication.translate('UMWL Geology', message)

    def _addPluginAction(self,
        icon_path,
        text,
        callback = None,
        add_to_menu = True,
        add_to_toolbar = True,
        status_tip = None,
        whats_this = None,
        parent = None,
        checkable = False,
        enabled = True
    ):

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled)
        action.setCheckable(checkable)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.iface.addToolBarIcon(action)
            self.cleanup_callbacks.append(lambda: self.iface.removeToolBarIcon(action))

        if add_to_menu:
            self.iface.addPluginToMenu(self.plugin_menu_name, action)
            self.cleanup_callbacks.append(lambda: self.iface.removePluginMenu(self.plugin_menu_name, action))

        return action

    def initProcessing(self):
        self.provider = Provider()
        qgs_processing_registry = QgsApplication.processingRegistry()
        qgs_processing_registry.addProvider(self.provider)
        self.cleanup_callbacks.append(lambda: qgs_processing_registry.removeProvider(self.provider))

    def initGui(self):
        self.initProcessing()
        self._addPluginAction(
            self.assets_dir / "coat_of_arms.png"
            'Dummy Action',
            parent = self.iface.mainWindow(),
            callback = self._initPluginGUI,
        )

    def _initPluginGUI(self):
        raise NotImplementedError

    def unload(self):
        for callback in self.cleanup_callbacks: callback()
        self.cleanup_callbacks.clear()

    def getPluginActionToolbar(self):
        raise NotImplementedError

    def getProcessingProvider(self):
        if self.provider is None:
            raise ValueError('Plugin processing was not initialized!')
        return self.provider
