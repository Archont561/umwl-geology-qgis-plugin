from pathlib import Path
from qgis.core import QgsApplication
from qgis.gui import QgisInterface
from qgis.PyQt.QtCore import QCoreApplication, QTranslator, QSettings, qVersion
from qgis.PyQt.QtWidgets import QAction
from qgis.PyQt.QtGui import QIcon
from .processing_provider.provider import Provider

from .widgets import MainToolBox
from . import resources


class UMWLGeologyPlugin:

    ###################################### CORE ######################################

    def __init__(self, iface: QgisInterface):
        self.mainToolBox = None
        self._gui_initialized = False
        self.iface = iface
        self.plugin_dir = Path(__file__).resolve().parent
        self.provider = None
        self.cleanup_callbacks = []

        self._localize()
        self.plugin_menu_name = f"&{self.tr('UMWL Geology')}"

    # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
    def _localize(self):
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = self.plugin_dir / 'i18n' / f'umwl_geology_{locale}.qm'

        if locale_path.exists():
            translator = QTranslator()
            translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(translator)

    # noinspection PyMethodMayBeStatic
    def tr(self, message: str) -> str:
        """Get the translation for a string using Qt translation API.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('umwl_geology', message)

    def initProcessing(self):
        self.provider = Provider()
        qgs_processing_registry = QgsApplication.processingRegistry()
        qgs_processing_registry.addProvider(self.provider)
        self.cleanup_callbacks.append(lambda: qgs_processing_registry.removeProvider(self.provider))

    def initGui(self):
        if self._gui_initialized:
            return

        self.initProcessing()
        self.add_action(
            self.plugin_dir / "icon.png",
            self.tr('Start plugin'),
            parent = self.iface.mainWindow(),
            callback = self.mainToolBox.show,
        )
        self.mainToolBox = MainToolBox()
        self._gui_initialized = True

    def unload(self):
        for callback in self.cleanup_callbacks: callback()
        self.cleanup_callbacks.clear()

    ###################################### EXTRA ######################################

    def add_action(self,
        icon_path: Path,
        text: str,
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

    def get_plugin_processing_provider(self):
        if self.provider is None:
            raise ValueError('Plugin processing was not initialized!')
        return self.provider

    def get_main_widget(self):
        return self.mainToolBox