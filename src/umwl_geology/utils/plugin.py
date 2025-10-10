from typing import Optional
from pathlib import Path
from abc import ABC, abstractmethod

from qgis.core import QgsApplication
from qgis.gui import QgisInterface
from PyQt5.QtCore import QCoreApplication, QTranslator, QSettings, qVersion
from PyQt5.QtWidgets import QAction
from PyQt5.QtGui import QIcon

from .processing_provider import ProcessingProvider


class QGISPlugin(ABC):
    """
    Abstract base class for QGIS plugins.

    This class provides common functionality for QGIS plugins including:
    - Localization support
    - Processing provider registration
    - GUI initialization with menus and toolbars
    - Cleanup on unload

    Subclasses must:
    - Define PLUGIN_NAME and PLUGIN_DIR class attributes
    - Implement create_processing_provider() static method
    - Implement init_gui() method

    Attributes:
        PLUGIN_NAME: The display name of the plugin. Must be set by subclasses.
        PLUGIN_DIR: The plugin's installation directory. Must be set by subclasses.
        iface: The QGIS interface instance.
        provider: The processing provider instance (if any).
        cleanup_callbacks: List of callbacks to execute on plugin unload.
    """

    PLUGIN_NAME: Optional[str] = None
    PLUGIN_DIR: Optional[Path] = None

    def __init__(self, iface: QgisInterface):
        """
        Initialize the plugin.

        Args:
            iface: The QGIS interface instance.

        Raises:
            NotImplementedError: If PLUGIN_DIR or PLUGIN_NAME are not defined in the subclass.
        """
        if self.__class__.PLUGIN_DIR is None:
            raise NotImplementedError("QGISPlugin subclass must define PLUGIN_DIR.")
        if self.__class__.PLUGIN_NAME is None:
            raise NotImplementedError("QGISPlugin subclass must define PLUGIN_NAME.")

        self._gui_initialized = False
        self.iface = iface
        self.provider = None
        self.cleanup_callbacks = []
        self._localize()

    def _localize(self):
        """
        Set up localization for the plugin.

        Loads translation files from the plugin's i18n directory based on
        the user's locale setting in QGIS. Translation files should be named
        with the two-letter locale code (e.g., 'en.qm', 'fr.qm').
        """
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = self.__class__.PLUGIN_DIR / 'i18n' / f'{locale}.qm'

        if locale_path.exists():
            translator = QTranslator()
            translator.load(str(locale_path))

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(translator)

    def tr(self, message: str) -> str:
        """
        Translate a string using Qt translation API.

        Args:
            message: The string to translate.

        Returns:
            The translated string, or the original message if no translation exists.
        """
        return QCoreApplication.translate(self.__class__.PLUGIN_NAME, message)

    def initProcessing(self):
        """
        Initialize and register the plugin's processing provider.

        Creates the processing provider via create_processing_provider() and
        registers it with QGIS. If no provider is created or it's not a valid
        ProcessingProvider instance, registration is skipped.
        """
        provider = self.create_processing_provider()
        if not provider or not isinstance(provider, ProcessingProvider):
            return

        self.provider = provider
        QgsApplication.processingRegistry().addProvider(provider)

    def initGui(self):
        """
        Initialize the plugin's GUI elements.

        This method is called by QGIS when the plugin is loaded. It ensures
        initialization only happens once, then calls initProcessing() and
        the subclass's init_gui() method.
        """
        if self._gui_initialized:
            return
        self.initProcessing()
        self.init_gui()
        self._gui_initialized = True

    def unload(self):
        """
        Clean up plugin resources when unloading.

        Executes all registered cleanup callbacks (e.g., removing menus and
        toolbars) and clears the callback list.
        """
        for callback in self.cleanup_callbacks:
            callback()
        self.cleanup_callbacks.clear()

    def add_action(self,
                   icon_path: Path,
                   text: str,
                   callback=None,
                   add_to_menu=True,
                   add_to_toolbar=True,
                   status_tip=None,
                   whats_this=None,
                   parent=None,
                   checkable=False,
                   enabled=True
                   ):
        """
        Add an action to the QGIS interface with automatic cleanup.

        Creates a QAction and optionally adds it to the plugin menu and/or
        toolbar. Cleanup callbacks are automatically registered to remove
        the action when the plugin is unloaded.

        Args:
            icon_path: Path to the action's icon file.
            text: The action's display text.
            callback: Function to call when the action is triggered. Defaults to None.
            add_to_menu: Whether to add the action to the plugin menu. Defaults to True.
            add_to_toolbar: Whether to add the action to the toolbar. Defaults to True.
            status_tip: Status bar tip text. Defaults to None.
            whats_this: "What's This?" help text. Defaults to None.
            parent: Parent widget. Defaults to None (uses main window).
            checkable: Whether the action is checkable. Defaults to False.
            enabled: Whether the action is initially enabled. Defaults to True.

        Returns:
            The created QAction instance.
        """
        if not parent:  # Fixed: was 'if parent:'
            parent = self.iface.mainWindow()

        icon = QIcon(str(icon_path))
        action = QAction(icon, text, parent)

        if callback:
            action.triggered.connect(callback) # noqa

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
            plugin_menu_name = f"&{self.__class__.PLUGIN_NAME}"
            self.iface.addPluginToMenu(plugin_menu_name, action)
            self.cleanup_callbacks.append(lambda: self.iface.removePluginMenu(plugin_menu_name, action))

        return action

    def get_plugin_processing_provider(self):
        """
        Get the plugin's processing provider instance.

        Returns:
            The ProcessingProvider instance.

        Raises:
            ValueError: If the processing provider was not initialized.
        """
        if self.provider is None:
            raise ValueError('Plugin processing was not initialized!')
        return self.provider

    @staticmethod
    @abstractmethod
    def create_processing_provider() -> Optional[ProcessingProvider]:
        """
        Create and return the plugin's processing provider.

        This is a factory method that subclasses must implement to provide
        their custom processing algorithms. The returned provider will be
        registered with QGIS's processing framework.

        Returns:
            An instance of ProcessingProvider, or None if the plugin
            doesn't provide processing algorithms.

        Example:
            @staticmethod
            def create_processing_provider():
                return MyCustomProvider()
        """

    @abstractmethod
    def init_gui(self):
        """
        Initialize the plugin's GUI elements.

        Subclasses must implement this method to create their UI components
        such as menus, toolbars, and actions. This method is called after
        processing initialization.

        Example:
            def init_gui(self):
                self.add_action(
                    icon_path=self.PLUGIN_DIR / 'icon.png',
                    text='My Action',
                    callback=self.run
                )
        """
        ...