from __future__ import annotations

from dataclasses import dataclass
from typing import Optional
from pathlib import Path

from PyQt5.QtWidgets import QMessageBox

from .utils.plugin import QGISPlugin
from .utils.processing_provider import ProcessingProvider
from .widgets.dialogs import QGISLayerPickerDialog, ParcelFinderDialog
from .provider import Provider
from .exceptions import QGISPluginError


@dataclass
class UMWLGeologyPluginActionDialogs:
    qgisLayerPickerDialog: QGISLayerPickerDialog
    parcelFinderDialog: ParcelFinderDialog


class UMWLGeologyPlugin(QGISPlugin):
    PLUGIN_NAME = "UMWL Geology"
    PLUGIN_DIR = Path(__file__).parent
    dialogs: Optional[UMWLGeologyPluginActionDialogs] = None

    @staticmethod
    def create_processing_provider() -> Optional[ProcessingProvider]:
        return Provider()

    def init_gui(self):
        self.dialogs = UMWLGeologyPluginActionDialogs(
            qgisLayerPickerDialog=QGISLayerPickerDialog(parent=self.iface.mainWindow()),
            parcelFinderDialog=ParcelFinderDialog(parent=self.iface.mainWindow()),
        )
        self.add_action(
            icon_path=self.PLUGIN_DIR / "icon.png",
            text=self.tr('Set plugin settings'),
            add_to_toolbar=False,
            callback = self._handle_settings,
        )
        self.add_action(
            icon_path=self.PLUGIN_DIR / "icon.png",
            text=self.tr('Open parcel finder dialog'),
            add_to_toolbar=False,
            callback = self._handle_parcel_search,
        )

    def _handle_settings(self):
        if self.dialogs is None:
            QMessageBox.critical(
                self.iface.mainWindow(),
                self.PLUGIN_NAME,
                self.tr("Plugin dialogs not initialized!")
            )
            return

        try:
            self.dialogs.qgisLayerPickerDialog.exec_()
        except QGISPluginError as e:
            QMessageBox.warning(
                self.iface.mainWindow(),
                self.PLUGIN_NAME,
                self.tr(f"Something went wrong when picking administrative layers: {e}")
            )
        else:
            polish_administrative_layers = self.dialogs.qgisLayerPickerDialog.get_polish_administrative_layers()
            if not polish_administrative_layers:
                QMessageBox.warning(
                    self.iface.mainWindow(),
                    self.PLUGIN_NAME,
                    self.tr("Failed to load required layers for plugin!")
                )
                return

            self.dialogs.parcelFinderDialog.load_admin_layers(polish_administrative_layers)
            QMessageBox.information(
                self.iface.mainWindow(),
                self.PLUGIN_NAME,
                self.tr("Loaded required layers successfully")
            )

    def _handle_parcel_search(self):
        if self.dialogs is None:
            QMessageBox.critical(
                self.iface.mainWindow(),
                self.PLUGIN_NAME,
                self.tr("Plugin dialogs not initialized!")
            )
            return

        if not self.dialogs.parcelFinderDialog.are_administrative_layers_loaded():
            QMessageBox.warning(
                self.iface.mainWindow(),
                self.PLUGIN_NAME,
                self.tr("Please define layers in settings first!")
            )
            return

        try:
            self.dialogs.parcelFinderDialog.exec_()
        except QGISPluginError as e:
            QMessageBox.warning(
                self.iface.mainWindow(),
                self.PLUGIN_NAME,
                self.tr(f"Something went wrong during parcel search: {e}")
            )

    def unload(self):
        # Clean up dialogs
        if self.dialogs is not None:
            # Close dialogs if they're open
            if self.dialogs.qgisLayerPickerDialog.isVisible():
                self.dialogs.qgisLayerPickerDialog.close()
            if self.dialogs.parcelFinderDialog.isVisible():
                self.dialogs.parcelFinderDialog.close()
            self.dialogs = None

        # Call parent cleanup
        super().unload()